#!/usr/bin/env python3
import os
import random
import datetime
import json
try:
    import psycopg2
    from psycopg2.extras import execute_values
except Exception:
    psycopg2 = None

DB_URL = os.environ.get("ANALYTICAL_DB_URL") or os.environ.get("ANALYTICAL_POSTGRES_URL")

 ADVISOR_COUNT = 500

HEADERS = (
    "advisor_id",
    "name",
    "aum",
    "holding_symbol",
    "holding_name",
    "last_flow_date"
)

FIELDS = []


def rand_name():
    first = ["Alex","Jordan","Taylor","Morgan","Casey","Riley","Quinn","Drew","Avery","Sam"]
    last = ["Kim","Patel","Nguyen","Smith","Garcia","Lee","Brown","Chen","Khan","Singh"]
    return f"{random.choice(first)} {random.choice(last)}"


def gen_holdings():
    # generate 2-4 holdings per advisor
    holdings = []
    for _ in range(random.randint(2,4)):
        sym = random.choice(["SPY","IVV","VOO","AGG","IEI","QQQ"])
        name = f"{sym} ETF"
        holdings.append((sym, name))
    return holdings


def main():
    if not DB_URL:
        print("NO ANALYTICAL DB URL set; skipping DB write.")
        return
    if psycopg2 is None:
        print("psycopg2 not installed; cannot run DB seed.")
        return
    conn = psycopg2.connect(DB_URL)
    cur = conn.cursor()
    now = datetime.date.today()
    advisors = []
    for i in range(ADVISOR_COUNT):
        advisor_id = f"adv_{i+1:04d}"
        name = rand_name()
        aum = random.randrange(50_000_000, 2_000_000_000)
        holdings = gen_holdings()
        holding_symbol = ",".join(h[0] for h in holdings)
        holding_name = ",".join(h[1] for h in holdings)
        last_flow = now - datetime.timedelta(days=random.randint(0,365))
        advisors.append((advisor_id, name, aum, holding_symbol, holding_name, last_flow))

    insert_query = "INSERT INTO advisors (advisor_id, name, aum, holding_symbol, holding_name, last_flow_date) VALUES %s"
    execute_values(cur, insert_query, advisors)
    conn.commit()
    cur.close()
    conn.close()
    print(f"Seeded {ADVISOR_COUNT} advisors into analytical DB.")

if __name__ == '__main__':
    main()
