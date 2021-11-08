import csv
import json
import psycopg2
import sys

def get_rows(table_code, place_code, cur):
    cur.execute('''select nomis_code_2011, category_name, count
                    from counts join categories on counts.category_id=categories.category_id
                    where categories.var_id = (select var_id from VARIABLES where nomis_table_code_2011 = %s)
                    and counts.place_id = (select place_id from PLACES where place_code = %s)''', (table_code, place_code))
    return cur.fetchall()

def main():
    table_code = sys.argv[1]
    place_code = sys.argv[2]

    with open('secrets.json', 'r') as f:
        credentials = json.load(f)
    con = psycopg2.connect(**credentials)
    cur = con.cursor()

    rows = get_rows(table_code, place_code, cur)

    con.close()

    print("CODE,NAME,VALUE")
    csvwriter = csv.writer(sys.stdout)
    for row in rows:
        csvwriter.writerow(row)

if __name__ == "__main__":
    main()
