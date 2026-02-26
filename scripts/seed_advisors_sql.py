#!/usr/bin/env python3
import random, datetime
ADVISOR_COUNT=500
NOW = datetime.date.today().isoformat()
random.seed(0)

lines=[]
for i in range(ADVISOR_COUNT):
    advisor_id=f"adv_{i+1:04d}"
    first=["Alex","Jordan","Taylor","Morgan","Casey","Riley","Quinn","Drew","Avery","Sam"]
    last=["Kim","Patel","Nguyen","Smith","Garcia","Lee","Brown","Chen","Khan","Singh"]
    name=f"{random.choice(first)} {random.choice(last)}"
    aum=random.randint(50_000_000, 2_000_000_000)
    holdings_symbols=",".join(random.sample(["SPY","IVV","VOO","AGG","IEI","QQQ"], k=3))
    holdings_names=",".join(h for h in ["SPY ETF","IVV ETF","VOO ETF"])
    last_flow=NOW
    lines.append(f"INSERT INTO advisors (advisor_id, name, aum, holding_symbol, holding_name, last_flow_date) VALUES ('{advisor_id}','{name}',{aum},'{holdings_symbols}','{holdings_names}','{last_flow}');")

with open("/data/workspace/seeds/advisors_seed.sql","w") as f:
    f.write("\n".join(lines))
print(f"Wrote {len(lines)} seed statements to /data/workspace/seeds/advisors_seed.sql")
