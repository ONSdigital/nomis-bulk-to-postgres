import csv
import json
import psycopg2
import sys

def get_rows(table_code, geo_code, cur):
    cur.execute('''select long_nomis_code, category_name, metric
                    from geo_metric join nomis_category on geo_metric.category_id=nomis_category.id
                    where nomis_category.nomis_desc_id = (select id from nomis_desc where short_nomis_code = %s)
                    and geo_metric.geo_id = (select id from geo where geo_code = %s)''', (table_code, geo_code))
    return cur.fetchall()

def main():
    table_code = sys.argv[1]
    geo_code = sys.argv[2]

    with open('secrets.json', 'r') as f:
        credentials = json.load(f)
    con = psycopg2.connect(**credentials)
    cur = con.cursor()

    rows = get_rows(table_code, geo_code, cur)

    con.close()

    print("CODE,NAME,VALUE")
    csvwriter = csv.writer(sys.stdout)
    for row in rows:
        csvwriter.writerow(row)

if __name__ == "__main__":
    main()
