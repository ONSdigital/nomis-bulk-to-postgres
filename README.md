# A script for getting lots of bulk data from Nomis

## Installation

```
python3 -m venv bulk
. ./bulk/bin/activate
pip install --upgrade pip
pip install psycopg2-binary
pip install q
```

## Config

DSN details for Postgres should be in `secrets.json`, eg.

```
{
  "host":"localhost",
  "database":"census",
  "user":"steve",
  "password":"steve"
}
```

## Useage

`./download-data.sh` gets lots of bulk data from Nomis, and `python add_to_db.py` puts it all in a Postgres database.
(To get more data, remove the second `grep` from download-data.sh)

## Example scripts

### Get data for a single column and its corresponding total column, for lots of places

```
python3 get_csv.py KS101EW001
```

Note that the column number given to this script should be 0-based (like the Nomis API)
rather than 1-based (like the Nomis bulk data).

### Get all data from a Nomis table for a single place

```
python3 get_table_for_one_place.py KS101EW K04000001
```
