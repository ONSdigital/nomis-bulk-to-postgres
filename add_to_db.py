import csv
import glob
import json
import psycopg2
from psycopg2.extras import execute_values
from collections import namedtuple

CategoryInfo = namedtuple('CategoryInfo', ['id', 'measurement_unit'])

def csv_iter(filename):
    with open(filename, newline='') as f:
        yield from csv.DictReader(f)

def add_meta_tables(cur):
    meta_files = glob.glob("data/**/*META*.CSV", recursive=True)
    for filename in meta_files:
        for d in csv_iter(filename):
            print(d)
            sql = '''insert into nomis_desc (name,pop_stat,short_nomis_code,year) values (%s,%s,%s,2011);'''

            import q;
            q(d["DatasetTitle"])

            if "Cyfradd" not in d["DatasetTitle"] :
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

def add_counts(cur, rows, type_id, geo_code_to_id):
    for row in rows:
        if row[0] not in geo_code_to_id:
            # This geo code isn't in the geo table yet, so add it.
            sql = '''insert into geo (code,name,type_id)
                      values (%s,%s,%s)
                      returning id;
                    '''
            cur.execute(sql, (row[0], row[0] + " name TODO", type_id))
            geo_code_to_id[row[0]] = cur.fetchone()[0]
        row[0] = geo_code_to_id[row[0]]   # replace code with ID
    sql = 'insert into geo_metric (geo_id, data_ver_id, category_id, metric) values %s;'
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
                    rows.append([
                        geog_code,
                        1,
                        nomis_col_id_to_category_info[column_code].id,
                        float(d[column_code])
                    ])
            add_counts(cur, rows, int(data_file_num), geo_code_to_id)

def create_geo_types(cur):
    with open("geo_types.txt", "r") as f:
        for line in f:
            type_id, name = line.strip().split()
            import q
            q(type_id)
            q(name)
            sql = 'insert into geo_type (id,name) values (%s,%s)'
            cur.execute(sql, (int(type_id), name))

def add_lsoa_lad_lookup(cur):
    for d in csv_iter("lookup/lsoa2011_lad2020.csv"):
        lsoa = d["code"]
        lad = "best_fit_" + d["parent"]
        cur.execute('insert into LSOA2011_LAD2020_LOOKUP (lsoa2011code,lad2020code) values (%s,%s)', [lsoa, lad])

def add_best_fit_lad2020_rows(cur, geo_code_to_id):
    cur.execute(
        '''select lad2020code, data_ver_id, category_id, sum(metric) from (
                select lad2020code, data_ver_id, category_id, metric from LSOA2011_LAD2020_LOOKUP
                    join geo on LSOA2011_LAD2020_LOOKUP.lsoa2011code = geo.code
                    join geo_metric on geo.id = geo_metric.geo_id
            ) as A group by lad2020code, data_ver_id, category_id;''')
    new_rows = [list(item) for item in cur.fetchall()]
    add_counts(cur, new_rows, 99, geo_code_to_id)

def main():
    with open('secrets.json', 'r') as f:
        credentials = json.load(f)
    con = psycopg2.connect(**credentials)
    cur = con.cursor()

    geo_code_to_id = {}  # a map from geo code (e.g. "E09000001") to geo_id in the geo table

    create_geo_types(cur)
    add_meta_tables(cur)
    nomis_col_id_to_category_info = add_desc_tables(cur)
    add_data_tables(cur, nomis_col_id_to_category_info, geo_code_to_id)

    #cur.execute('create index if not exists idx_counts_geo_id on geo_metric(geo_id)')

    add_lsoa_lad_lookup(cur)

    add_best_fit_lad2020_rows(cur, geo_code_to_id)

    #cur.execute('create index if not exists idx_counts_category_id on geo_metric(category_id)')

    con.commit()
    con.close()

if __name__ == "__main__":
    main()
