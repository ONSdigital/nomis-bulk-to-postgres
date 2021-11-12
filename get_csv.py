import csv
import json
import psycopg2
import sys

def get_rows(code, cur):
    cur.execute('''select geo_code, metric
                    from geo_metric join geo on geo_metric.geo_id=geo.id
                    where category_id = (select id from nomis_category where long_nomis_code = %s)''', (code,))
    rows = cur.fetchall()
    result = []
    for row in rows:
        if row[0].startswith("K04"):
            result.append(("EW", int(row[1])))
        elif row[0].startswith("E01") or row[0].startswith("W01"):
            result.append((row[0], int(row[1])))
        elif row[0].startswith("best_fit_"):
            result.append((row[0][9:], int(row[1])))
    return result

def main():
    code = sys.argv[1]

    with open('secrets.json', 'r') as f:
        credentials = json.load(f)
    con = psycopg2.connect(**credentials)
    cur = con.cursor()

    table = code[:5]
    column = int(code[-3:]) + 1
    code1 = "{}EW{:04}".format(table, column)
    code2 = "{}EW{:04}".format(table, 1)
    rows = get_rows(code1, cur)
    total_rows = dict(get_rows(code2, cur))

    con.close()

    print("GEOGRAPHY_CODE,TOTAL,COUNT")
    for row in rows:
        print("{},{},{}".format(row[0], total_rows[row[0]], row[1]))

if __name__ == "__main__":
    main()
