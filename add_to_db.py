import csv
import glob
import json
import psycopg2
from psycopg2.extras import execute_values
from collections import namedtuple

TABLES = [
    '''geo_metric(
        id SERIAL PRIMARY KEY,
        geo_id INTEGER NOT NULL,
        year INTEGER NOT NULL,
        category_id INTEGER NOT NULL,
        metric INTEGER NOT NULL
    )''',
    '''nomis_desc(
        id SERIAL PRIMARY KEY NOT NULL,
        short_desc TEXT NOT NULL,
        long_desc TEXT NOT NULL,
        short_nomis_code TEXT NOT NULL,
        year INTEGER NOT NULL
    )''',
    '''nomis_category(
        id SERIAL PRIMARY KEY,
        nomis_desc_id INTEGER NOT NULL,
        category_name TEXT NOT NULL,
        measurement_unit TEXT NOT NULL,
        stat_unit TEXT NOT NULL,
        long_nomis_code TEXT NOT NULL,
        year INTEGER NOT NULL
    )''',
    '''LSOA2011_LAD2020_LOOKUP(
        id SERIAL PRIMARY KEY,
        lsoa2011code TEXT NOT NULL,
        lad2020code TEXT NOT NULL
    )''',
    '''geo_type(
        id INTEGER PRIMARY KEY,
        geo_type_name TEXT NOT NULL
    )''',
    '''geo(
        id SERIAL PRIMARY KEY,
        geo_code TEXT NOT NULL,
        geo_name TEXT NOT NULL,
        geo_type_id INTEGER NOT NULL
    )'''
]

FOREIGN_KEY_CONSTRAINTS = [
    "ALTER TABLE geo_metric ADD CONSTRAINT fk_geo FOREIGN KEY (geo_id) REFERENCES geo(id);",
    "ALTER TABLE geo_metric ADD CONSTRAINT fk_nomis_category FOREIGN KEY (category_id) REFERENCES nomis_category(id);",
    "ALTER TABLE geo ADD CONSTRAINT fk_geo_type FOREIGN KEY (geo_type_id) REFERENCES geo_type(id);",
    "ALTER TABLE nomis_category ADD CONSTRAINT fk_nomis_desc  FOREIGN KEY (nomis_desc_id) REFERENCES nomis_desc(id);"
]

CategoryInfo = namedtuple('CategoryInfo', ['id', 'measurement_unit'])

def csv_iter(filename):
    with open(filename, newline='') as f:
        yield from csv.DictReader(f)

def create_tables(cur):
    cur.execute('DROP SCHEMA public CASCADE;')
    cur.execute('CREATE SCHEMA public;')
    for table in TABLES:
        cur.execute('DROP TABLE IF EXISTS {}'.format(table[:table.find("(")]))
    for table in TABLES:
        cur.execute('CREATE TABLE IF NOT EXISTS {}'.format(table))
    for constraint in FOREIGN_KEY_CONSTRAINTS:
        cur.execute(constraint)

def add_meta_tables(cur):
    meta_files = glob.glob("data/**/*META*.CSV", recursive=True)
    for filename in meta_files:
        for d in csv_iter(filename):
            print(d)
            sql = '''insert into nomis_desc (short_desc,long_desc,short_nomis_code,year) values (%s,%s,%s,2011);'''
            cur.execute(sql, [d["DatasetTitle"], d["StatisticalPopulations"], d["DatasetId"]])
        print()

def add_desc_tables(cur):
    nomis_col_id_to_category_info = {}
    desc_files = glob.glob("data/**/*DESC*.CSV", recursive=True)
    print(desc_files)
    for filename in desc_files:
        for d in csv_iter(filename):
            print(d)
            col_code = d["ColumnVariableCode"]
            pos = col_code.rfind("EW")
            if pos == -1:
                continue
            table_code = col_code[:pos+2]
            print("TABLECODE", table_code)
            sql = '''insert into nomis_category (nomis_desc_id,category_name,measurement_unit,stat_unit,long_nomis_code,year)
                     values ((select id from nomis_desc where short_nomis_code = %s),%s,%s,%s,%s,2011)
                     returning id;
                  '''
            cur.execute(sql, [
                table_code,
                d["ColumnVariableDescription"],
                d["ColumnVariableMeasurementUnit"],
                d["ColumnVariableStatisticalUnit"],
                d["ColumnVariableCode"]
            ])
            nomis_col_id_to_category_info[d["ColumnVariableCode"]] = CategoryInfo(
                cur.fetchone()[0],
                d["ColumnVariableMeasurementUnit"]
            )
        print()
    return nomis_col_id_to_category_info

def add_counts(cur, rows, geo_type_id, geo_code_to_id):
    for row in rows:
        if row[0] not in geo_code_to_id:
            # This geo code isn't in the geo table yet, so add it.
            sql = '''insert into geo (geo_code,geo_name,geo_type_id)
                      values (%s,%s,%s)
                      returning id;
                    '''
            cur.execute(sql, (row[0], row[0] + " name TODO", geo_type_id))
            geo_code_to_id[row[0]] = cur.fetchone()[0]
        row[0] = geo_code_to_id[row[0]]   # replace code with ID
    sql = 'insert into geo_metric (geo_id, year, category_id, metric) values %s;'
    execute_values(cur, sql, rows)   # Much faster than executemany

def add_data_tables(cur, nomis_col_id_to_category_info, geo_code_to_id):
    for data_file_num in ["01", "02", "03", "04", "05", "06"]:
        data_files = glob.glob("data/**/*DATA{}.CSV".format(data_file_num), recursive=True)
        print(data_files)
        for filename in data_files:
            print(filename)
            rows = []
            for d in csv_iter(filename):
                geog_code = d["GeographyCode"]
                for column_code in d:
                    if column_code == "GeographyCode":
                        continue
                    if column_code not in nomis_col_id_to_category_info:
                        continue
                    if nomis_col_id_to_category_info[column_code].measurement_unit != 'Count':
                        continue
                    rows.append([
                        geog_code,
                        2011,
                        nomis_col_id_to_category_info[column_code].id,
                        float(d[column_code])
                    ])
            add_counts(cur, rows, int(data_file_num), geo_code_to_id)

def create_geo_types(cur):
    with open("geo_types.txt", "r") as f:
        for line in f:
            geo_type_id, geo_type_name = line.strip().split()
            sql = 'insert into geo_type (id,geo_type_name) values (%s,%s)'
            cur.execute(sql, (int(geo_type_id), geo_type_name))

def add_lsoa_lad_lookup(cur):
    for d in csv_iter("lookup/lsoa2011_lad2020.csv"):
        lsoa = d["code"]
        lad = "best_fit_" + d["parent"]
        cur.execute('insert into LSOA2011_LAD2020_LOOKUP (lsoa2011code,lad2020code) values (%s,%s)', [lsoa, lad])

def add_best_fit_lad2020_rows(cur, geo_code_to_id):
    cur.execute(
        '''select lad2020code, year, category_id, sum(metric) from (
                select lad2020code, year, category_id, metric from LSOA2011_LAD2020_LOOKUP
                    join geo on LSOA2011_LAD2020_LOOKUP.lsoa2011code = geo.geo_code
                    join geo_metric on geo.id = geo_metric.geo_id
            ) as A group by lad2020code, year, category_id;''')
    new_rows = [list(item) for item in cur.fetchall()]
    add_counts(cur, new_rows, 99, geo_code_to_id)

def main():
    with open('secrets.json', 'r') as f:
        credentials = json.load(f)
    con = psycopg2.connect(**credentials)
    cur = con.cursor()

    geo_code_to_id = {}  # a map from geo code (e.g. "E09000001") to geo_id in the geo table

    create_tables(cur)
    create_geo_types(cur)
    add_meta_tables(cur)
    nomis_col_id_to_category_info = add_desc_tables(cur)
    add_data_tables(cur, nomis_col_id_to_category_info, geo_code_to_id)

    cur.execute('create index if not exists idx_counts_geo_id on geo_metric(geo_id)')

    add_lsoa_lad_lookup(cur)

    add_best_fit_lad2020_rows(cur, geo_code_to_id)

    cur.execute('create index if not exists idx_counts_category_id on geo_metric(category_id)')

    con.commit()
    con.close()

if __name__ == "__main__":
    main()
