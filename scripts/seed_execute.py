#!/usr/bin/env python3
import os, sys
import psycopg2
from psycopg2.extras import execute_values
import pathlib

DB_URL = os.environ.get('ANALYTICAL_DB_URL') or os.environ.get('ANALYTICAL_POSTGRES_URL')
SQL_FILE = pathlib.Path('/data/workspace/seeds/advisors_seed.sql')

if not DB_URL:
    print('NO ANALYTICAL DB URL set; skipping seed.')
    sys.exit(0)

if not SQL_FILE.exists():
    print('SQL seed file not found:', SQL_FILE)
    sys.exit(1)

conn = psycopg2.connect(DB_URL)
cur = conn.cursor()
with open(SQL_FILE, 'r') as f:
    sql = f.read()
try:
    cur.execute(sql)
    conn.commit()
    print('Seed executed.')
except Exception as e:
    conn.rollback()
    print('Seed failed:', e)
    sys.exit(2)
finally:
    cur.close(); conn.close()
