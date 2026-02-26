#!/usr/bin/env python3
"""
generate_full_seed.py — Generates realistic seed data for the Invesco Signal Studio demo.

Output: /data/workspace/seeds/full_seed.sql

500 advisors + holdings (3-8 each) + 12 months of flows + 10 interesting advisors with signals.
"""

import random
import math
import json
from datetime import date, timedelta


def add_months(d, months):
    """Add months to a date without dateutil."""
    month = d.month - 1 + months
    year = d.year + month // 12
    month = month % 12 + 1
    import calendar
    day = min(d.day, calendar.monthrange(year, month)[1])
    return date(year, month, day)

random.seed(42)  # reproducible

OUT_FILE = "/data/workspace/seeds/full_seed.sql"

# ─── Reference data ───────────────────────────────────────────────────────────

FIRST_NAMES = [
    "James", "Michael", "Robert", "David", "William", "Richard", "Joseph", "Thomas",
    "Charles", "Christopher", "Daniel", "Matthew", "Anthony", "Donald", "Mark",
    "Mary", "Patricia", "Jennifer", "Linda", "Barbara", "Elizabeth", "Susan",
    "Jessica", "Sarah", "Karen", "Lisa", "Nancy", "Betty", "Margaret", "Sandra",
    "Ashley", "Emily", "Donna", "Michelle", "Carol", "Amanda", "Dorothy", "Melissa",
    "Deborah", "Stephanie", "Rebecca", "Sharon", "Laura", "Cynthia", "Kathleen",
    "Raj", "Priya", "Arjun", "Deepa", "Wei", "Mei", "Chen", "Li", "Juan", "Maria",
    "Carlos", "Ana", "Luis", "Sofia", "Miguel", "Isabella", "Andre", "Fatima",
    "Omar", "Aisha", "Yusuf", "Amara", "Kenji", "Yuki", "Hiroshi", "Akira",
    "Patrick", "Colleen", "Sean", "Brigid", "Dmitri", "Natasha", "Vladimir", "Elena",
]

LAST_NAMES = [
    "Smith", "Johnson", "Williams", "Brown", "Jones", "Garcia", "Miller", "Davis",
    "Rodriguez", "Martinez", "Hernandez", "Lopez", "Gonzalez", "Wilson", "Anderson",
    "Thomas", "Taylor", "Moore", "Jackson", "Martin", "Lee", "Perez", "Thompson",
    "White", "Harris", "Sanchez", "Clark", "Ramirez", "Lewis", "Robinson",
    "Walker", "Young", "Allen", "King", "Wright", "Scott", "Torres", "Nguyen",
    "Hill", "Flores", "Green", "Adams", "Nelson", "Baker", "Hall", "Rivera",
    "Campbell", "Mitchell", "Carter", "Roberts", "Patel", "Shah", "Kumar",
    "Singh", "Chen", "Wang", "Zhang", "Liu", "Kim", "Park", "Choi",
    "O'Brien", "Murphy", "Sullivan", "McCarthy", "Kowalski", "Nowak", "Weber",
    "Fischer", "Muller", "Okonkwo", "Mensah", "Diallo", "Tremblay", "Bouchard",
]

FIRMS = [
    ("Raymond James", "BD"), ("Raymond James", "BD"),
    ("Edward Jones", "BD"), ("Edward Jones", "BD"), ("Edward Jones", "BD"),
    ("Merrill Lynch", "BD"), ("Merrill Lynch", "BD"),
    ("Wells Fargo Advisors", "BD"), ("Wells Fargo Advisors", "BD"),
    ("LPL Financial", "BD"), ("LPL Financial", "BD"),
    ("Morgan Stanley", "BD"), ("Morgan Stanley", "BD"),
    ("UBS Financial Services", "BD"),
    ("Ameriprise Financial", "BD"), ("Ameriprise Financial", "BD"),
    ("Stifel Financial", "BD"),
    ("Baird", "BD"),
    ("Northwestern Mutual", "BD"),
    ("Principal Financial", "BD"),
    ("Fidelity Brokerage", "BD"),
    ("Beacon Wealth Management", "RIA"),
    ("Cornerstone Capital Advisors", "RIA"),
    ("Pinnacle Wealth Partners", "RIA"),
    ("Summit Financial Group", "RIA"),
    ("Horizon Investment Advisors", "RIA"),
    ("Patriot Wealth Advisors", "RIA"),
    ("BlueSky Financial Planning", "RIA"),
    ("Pacific Crest Advisors", "RIA"),
    ("Strategic Wealth Management", "RIA"),
    ("Keystone Advisors", "RIA"),
    ("Liberty Wealth Partners", "RIA"),
    ("Meridian Capital Group", "RIA"),
    ("Apex Financial Partners", "RIA"),
    ("Castle Rock Wealth", "RIA"),
    ("JP Morgan Private Bank", "Bank"),
    ("Bank of America Private Bank", "Bank"),
    ("Citibank Private Clients", "Bank"),
    ("US Bank Wealth Management", "Bank"),
    ("PNC Wealth Management", "Bank"),
    ("Regions Bank Wealth", "Bank"),
    ("Fifth Third Private Bank", "Bank"),
    ("Truist Wealth", "Bank"),
    ("KeyBank Private Banking", "Bank"),
    ("Huntington Private Client", "Bank"),
    ("Northwestern Mutual Life", "Insurance"),
    ("New York Life Investments", "Insurance"),
    ("MassMutual", "Insurance"),
    ("Guardian Life", "Insurance"),
    ("Pacific Life", "Insurance"),
    ("Lincoln Financial", "Insurance"),
    ("Transamerica", "Insurance"),
    ("Nationwide Financial", "Insurance"),
]

REGIONS = {
    "NE": [
        ("New York", "NY"), ("Boston", "MA"), ("Philadelphia", "PA"),
        ("Hartford", "CT"), ("Providence", "RI"), ("Albany", "NY"),
        ("Newark", "NJ"), ("Pittsburgh", "PA"), ("Buffalo", "NY"),
        ("Baltimore", "MD"), ("Washington", "DC"), ("Stamford", "CT"),
    ],
    "SE": [
        ("Atlanta", "GA"), ("Charlotte", "NC"), ("Miami", "FL"),
        ("Tampa", "FL"), ("Orlando", "FL"), ("Nashville", "TN"),
        ("Raleigh", "NC"), ("Richmond", "VA"), ("Jacksonville", "FL"),
        ("Louisville", "KY"), ("Birmingham", "AL"), ("Memphis", "TN"),
        ("New Orleans", "LA"), ("Columbia", "SC"), ("Greenville", "SC"),
    ],
    "MW": [
        ("Chicago", "IL"), ("Minneapolis", "MN"), ("Detroit", "MI"),
        ("Columbus", "OH"), ("Indianapolis", "IN"), ("Cleveland", "OH"),
        ("Milwaukee", "WI"), ("St. Louis", "MO"), ("Kansas City", "MO"),
        ("Cincinnati", "OH"), ("Omaha", "NE"), ("Des Moines", "IA"),
        ("Grand Rapids", "MI"), ("Madison", "WI"),
    ],
    "SW": [
        ("Dallas", "TX"), ("Houston", "TX"), ("Phoenix", "AZ"),
        ("San Antonio", "TX"), ("Austin", "TX"), ("Denver", "CO"),
        ("Las Vegas", "NV"), ("Albuquerque", "NM"), ("Tucson", "AZ"),
        ("El Paso", "TX"), ("Fort Worth", "TX"), ("Oklahoma City", "OK"),
        ("Salt Lake City", "UT"), ("Colorado Springs", "CO"),
    ],
    "W": [
        ("Los Angeles", "CA"), ("San Francisco", "CA"), ("Seattle", "WA"),
        ("San Diego", "CA"), ("Portland", "OR"), ("Sacramento", "CA"),
        ("San Jose", "CA"), ("Oakland", "CA"), ("Honolulu", "HI"),
        ("Anchorage", "AK"), ("Boise", "ID"), ("Spokane", "WA"),
        ("Fresno", "CA"), ("Long Beach", "CA"),
    ],
}

# Region weights matching real-world advisor distribution
REGION_WEIGHTS = {"NE": 0.25, "SE": 0.22, "MW": 0.20, "SW": 0.18, "W": 0.15}

# ─── Fund universe ─────────────────────────────────────────────────────────────

INVESCO_FUNDS = {
    "QQQ":  ("Invesco QQQ Trust", "ETF", "Invesco"),
    "IVVB": ("Invesco S&P 500 UCITS ETF", "ETF", "Invesco"),
    "IVOO": ("Invesco S&P MidCap 400 ETF", "ETF", "Invesco"),
    "IVOV": ("Invesco S&P MidCap 400 Value ETF", "ETF", "Invesco"),
    "BKAG": ("Invesco BulletShares 2026 Corp Bond ETF", "ETF", "Invesco"),
    "BKLC": ("Invesco BulletShares 2027 Corp Bond ETF", "ETF", "Invesco"),
    "OFIN": ("Invesco Oppenheimer Developing Markets", "MF", "Invesco"),
    "PGX":  ("Invesco Preferred ETF", "ETF", "Invesco"),
    "BAB":  ("Invesco Build America Bond ETF", "ETF", "Invesco"),
    "KBWB": ("Invesco KBW Bank ETF", "ETF", "Invesco"),
    "IQQU": ("Invesco NASDAQ 100 Index Mutual Fund", "MF", "Invesco"),
    "OIGAX":("Invesco Growth and Income Fund", "MF", "Invesco"),
}

COMPETITOR_FUNDS = {
    "VOO":  ("Vanguard S&P 500 ETF", "ETF", "Vanguard"),
    "IVV":  ("iShares Core S&P 500 ETF", "ETF", "iShares"),
    "SPY":  ("SPDR S&P 500 ETF Trust", "ETF", "State Street"),
    "GLD":  ("SPDR Gold Shares", "ETF", "State Street"),
    "AGG":  ("iShares Core U.S. Aggregate Bond ETF", "ETF", "iShares"),
    "BND":  ("Vanguard Total Bond Market ETF", "ETF", "Vanguard"),
    "VTI":  ("Vanguard Total Stock Market ETF", "ETF", "Vanguard"),
    "VEA":  ("Vanguard FTSE Developed Markets ETF", "ETF", "Vanguard"),
    "VWO":  ("Vanguard FTSE Emerging Markets ETF", "ETF", "Vanguard"),
    "EFA":  ("iShares MSCI EAFE ETF", "ETF", "iShares"),
    "LQD":  ("iShares iBoxx $ IG Corp Bond ETF", "ETF", "iShares"),
    "TLT":  ("iShares 20+ Year Treasury Bond ETF", "ETF", "iShares"),
    "ACWI": ("iShares MSCI ACWI ETF", "ETF", "iShares"),
    "SCHB": ("Schwab U.S. Broad Market ETF", "ETF", "Schwab"),
    "FXAIX":("Fidelity 500 Index Fund", "MF", "Fidelity"),
    "VTSAX":("Vanguard Total Stock Market Index Fund", "MF", "Vanguard"),
    "VFIAX":("Vanguard 500 Index Fund Admiral Shares", "MF", "Vanguard"),
    "PIMCO":("PIMCO Total Return Fund", "MF", "PIMCO"),
    "DODGX":("Dodge & Cox Stock Fund", "MF", "Dodge & Cox"),
    "AMCAP":("American Funds AMCAP Fund", "MF", "American Funds"),
    "AGTHX":("American Funds Growth Fund of America", "MF", "American Funds"),
    "AIVSX":("American Funds Investment Co of America", "MF", "American Funds"),
    "CAIBX":("American Funds Capital Income Builder", "MF", "American Funds"),
}

ALL_FUNDS = {**INVESCO_FUNDS, **COMPETITOR_FUNDS}

INVESCO_SYMBOLS = list(INVESCO_FUNDS.keys())
COMPETITOR_SYMBOLS = list(COMPETITOR_FUNDS.keys())

# ─── Helper functions ──────────────────────────────────────────────────────────

def rand_aum():
    """Log-normal distribution: most $100M-$500M, range $50M-$2B"""
    mu = math.log(250_000_000)
    sigma = 0.7
    val = random.lognormvariate(mu, sigma)
    return int(max(50_000_000, min(2_000_000_000, val)) / 1_000_000) * 1_000_000


def rand_aum_12m_ago(current_aum):
    """12m ago: mostly ±15%, but some big movers"""
    r = random.random()
    if r < 0.05:   # big decline -20 to -40%
        factor = random.uniform(0.60, 0.80)
    elif r < 0.10: # big growth +20 to +50%
        factor = random.uniform(1.20, 1.50)
    elif r < 0.20: # moderate decline -10 to -20%
        factor = random.uniform(0.80, 0.90)
    elif r < 0.35: # moderate growth +10 to +20%
        factor = random.uniform(1.10, 1.20)
    else:          # normal ±10%
        factor = random.uniform(0.90, 1.10)
    return int(current_aum * factor / 1_000_000) * 1_000_000


def rand_client_count(aum):
    """Realistic client count: avg $1-3M per client"""
    avg_size = random.randint(800_000, 3_000_000)
    count = max(20, int(aum / avg_size) + random.randint(-20, 20))
    return count


def rand_phone():
    area = random.randint(201, 999)
    prefix = random.randint(200, 999)
    line = random.randint(1000, 9999)
    return f"({area}) {prefix}-{line}"


def rand_email(name, firm):
    first, *rest = name.split()
    last = rest[-1] if rest else "advisor"
    domain = firm.lower().replace(" ", "").replace(".", "")[:12] + ".com"
    return f"{first.lower()}.{last.lower()}@{domain}"


def pick_region():
    regions = list(REGION_WEIGHTS.keys())
    weights = list(REGION_WEIGHTS.values())
    return random.choices(regions, weights=weights, k=1)[0]


def pick_location(region):
    return random.choice(REGIONS[region])


def generate_holdings(advisor_id, aum_current, invesco_pct=0.30, n_holdings=None):
    """Generate 3-8 holdings summing to ~100% of AUM."""
    if n_holdings is None:
        n_holdings = random.randint(3, 8)

    # Decide how many will be Invesco vs competitors
    n_invesco = max(1, round(n_holdings * invesco_pct + random.uniform(-0.5, 0.5)))
    n_invesco = min(n_invesco, len(INVESCO_SYMBOLS), n_holdings - 1)
    n_comp = n_holdings - n_invesco

    selected_invesco = random.sample(INVESCO_SYMBOLS, n_invesco)
    selected_comp = random.sample(COMPETITOR_SYMBOLS, min(n_comp, len(COMPETITOR_SYMBOLS)))
    all_selected = selected_invesco + selected_comp

    # Generate random weights that sum to 1
    weights = [random.uniform(0.05, 0.40) for _ in all_selected]
    total = sum(weights)
    weights = [w / total for w in weights]

    holdings = []
    as_of = date(2026, 1, 31)
    for symbol, pct in zip(all_selected, weights):
        fund_name, fund_type, fund_family = ALL_FUNDS[symbol]
        aum_in_fund = int(aum_current * pct / 1_000_000) * 1_000_000
        holdings.append({
            "advisor_id": advisor_id,
            "symbol": symbol,
            "fund_name": fund_name,
            "fund_type": fund_type,
            "fund_family": fund_family,
            "aum_in_fund": aum_in_fund,
            "pct_of_aum": round(pct * 100, 2),
            "as_of_date": as_of.isoformat(),
        })
    return holdings


def generate_flows(advisor_id, symbol, aum_in_fund, flow_pattern="normal"):
    """Generate 12 months of flows for one holding."""
    flows = []
    base_date = date(2025, 2, 1)  # 12 months ago from Feb 2026

    for i in range(12):
        flow_month = add_months(base_date, i)

        if flow_pattern == "heavy_outflow":
            gross_in = int(random.uniform(0.005, 0.015) * aum_in_fund)
            gross_out = int(random.uniform(0.03, 0.08) * aum_in_fund)
        elif flow_pattern == "heavy_inflow":
            gross_in = int(random.uniform(0.03, 0.08) * aum_in_fund)
            gross_out = int(random.uniform(0.005, 0.015) * aum_in_fund)
        elif flow_pattern == "dormant":
            # Was active, then stopped ~6 months ago
            if i < 6:
                gross_in = int(random.uniform(0.01, 0.03) * aum_in_fund)
                gross_out = int(random.uniform(0.005, 0.015) * aum_in_fund)
            else:
                gross_in = 0
                gross_out = 0
        else:  # normal: seasonal pattern
            # Q1 is usually slower, Q4 is stronger
            season = [0.7, 0.8, 0.9, 1.0, 1.1, 1.0, 0.9, 0.9, 1.0, 1.1, 1.2, 1.1]
            s = season[i % 12]
            gross_in = int(s * random.uniform(0.01, 0.025) * aum_in_fund)
            gross_out = int(s * random.uniform(0.008, 0.02) * aum_in_fund)

        net_flow = gross_in - gross_out
        flows.append({
            "advisor_id": advisor_id,
            "symbol": symbol,
            "flow_month": flow_month.isoformat(),
            "net_flow": net_flow,
            "gross_inflow": gross_in,
            "gross_outflow": gross_out,
        })
    return flows


def esc(s):
    """Escape single quotes for SQL."""
    if s is None:
        return "NULL"
    return "'" + str(s).replace("'", "''") + "'"


# ─── Build the 10 interesting advisors ────────────────────────────────────────

def build_interesting_advisors():
    advisors = []
    holdings_all = []
    flows_all = []
    signals_all = []
    as_of = date(2026, 1, 31)

    # ── 001: CHAMPION — $450M, grew 25% YoY, 60% Invesco ──────────────────
    adv = {
        "advisor_id": "adv_interesting_001",
        "full_name": "Sarah Whitmore",
        "firm_name": "Pinnacle Wealth Partners",
        "region": "NE",
        "channel": "RIA",
        "aum_current": 450_000_000,
        "aum_12m_ago": 360_000_000,
        "client_count": 185,
        "email": "sarah.whitmore@pinnaclewealth.com",
        "phone": "(617) 555-0191",
        "city": "Boston",
        "state": "MA",
    }
    advisors.append(adv)
    holdings_001 = [
        ("QQQ",   "Invesco QQQ Trust",               "ETF",         "Invesco", 135_000_000, 30.0),
        ("IVOO",  "Invesco S&P MidCap 400 ETF",       "ETF",         "Invesco",  72_000_000, 16.0),
        ("BKAG",  "Invesco BulletShares 2026 Corp",   "ETF",         "Invesco",  54_000_000, 12.0),
        ("VOO",   "Vanguard S&P 500 ETF",             "ETF",         "Vanguard", 90_000_000, 20.0),
        ("AGG",   "iShares Core U.S. Aggregate Bond", "ETF",         "iShares",  67_500_000, 15.0),
        ("GLD",   "SPDR Gold Shares",                 "ETF",         "State Street", 31_500_000, 7.0),
    ]
    for sym, fn, ft, ff, amt, pct in holdings_001:
        holdings_all.append({"advisor_id": "adv_interesting_001", "symbol": sym,
            "fund_name": fn, "fund_type": ft, "fund_family": ff,
            "aum_in_fund": amt, "pct_of_aum": pct, "as_of_date": as_of.isoformat()})
        flows_all.extend(generate_flows("adv_interesting_001", sym, amt, "heavy_inflow"))
    signals_all.append({
        "advisor_id": "adv_interesting_001",
        "signal_type": "CHAMPION",
        "signal_score": 9.2,
        "signal_data": json.dumps({
            "summary": "Champion advisor: 25% AUM growth YoY, 58% Invesco allocation",
            "aum_growth_pct": 25.0,
            "invesco_pct": 58.0,
            "action": "Schedule QBR, offer exclusivity on new Invesco product launches",
            "priority": "HIGH",
            "next_step": "Executive relationship review Q1 2026",
        }),
    })

    # ── 002: AUM_DECLINE — $800M→$640M (-20%), flows leaving ───────────────
    adv = {
        "advisor_id": "adv_interesting_002",
        "full_name": "Robert Caldwell",
        "firm_name": "Morgan Stanley",
        "region": "SE",
        "channel": "BD",
        "aum_current": 640_000_000,
        "aum_12m_ago": 800_000_000,
        "client_count": 312,
        "email": "robert.caldwell@morganstanley.com",
        "phone": "(404) 555-0247",
        "city": "Atlanta",
        "state": "GA",
    }
    advisors.append(adv)
    holdings_002 = [
        ("QQQ",  "Invesco QQQ Trust",               "ETF", "Invesco",   64_000_000, 10.0),
        ("IVV",  "iShares Core S&P 500 ETF",         "ETF", "iShares",  192_000_000, 30.0),
        ("VOO",  "Vanguard S&P 500 ETF",             "ETF", "Vanguard", 128_000_000, 20.0),
        ("AGG",  "iShares Core U.S. Aggregate Bond", "ETF", "iShares",  128_000_000, 20.0),
        ("BND",  "Vanguard Total Bond Market ETF",   "ETF", "Vanguard",  64_000_000, 10.0),
        ("EFA",  "iShares MSCI EAFE ETF",             "ETF", "iShares",   64_000_000, 10.0),
    ]
    for sym, fn, ft, ff, amt, pct in holdings_002:
        holdings_all.append({"advisor_id": "adv_interesting_002", "symbol": sym,
            "fund_name": fn, "fund_type": ft, "fund_family": ff,
            "aum_in_fund": amt, "pct_of_aum": pct, "as_of_date": as_of.isoformat()})
        flows_all.extend(generate_flows("adv_interesting_002", sym, amt, "heavy_outflow"))
    signals_all.append({
        "advisor_id": "adv_interesting_002",
        "signal_type": "AUM_DECLINE",
        "signal_score": 9.5,
        "signal_data": json.dumps({
            "summary": "CRITICAL: $160M AUM decline in 12 months (-20%), heavy outflows to competitors",
            "aum_decline_pct": -20.0,
            "aum_lost": 160_000_000,
            "primary_outflow_destination": "Vanguard direct",
            "action": "Immediate outreach — understand drivers, offer fee review",
            "priority": "CRITICAL",
            "risk_rating": "HIGH",
        }),
    })

    # ── 003: CROSS_SELL_ETF — $600M all MF, zero ETFs ──────────────────────
    adv = {
        "advisor_id": "adv_interesting_003",
        "full_name": "Margaret Holloway",
        "firm_name": "Edward Jones",
        "region": "MW",
        "channel": "BD",
        "aum_current": 600_000_000,
        "aum_12m_ago": 582_000_000,
        "client_count": 490,
        "email": "margaret.holloway@edwardjones.com",
        "phone": "(314) 555-0338",
        "city": "St. Louis",
        "state": "MO",
    }
    advisors.append(adv)
    holdings_003 = [
        ("FXAIX", "Fidelity 500 Index Fund",             "MF", "Fidelity",      120_000_000, 20.0),
        ("VTSAX", "Vanguard Total Stock Market Index",    "MF", "Vanguard",      120_000_000, 20.0),
        ("VFIAX", "Vanguard 500 Index Fund Admiral",      "MF", "Vanguard",       90_000_000, 15.0),
        ("AGTHX", "American Funds Growth Fund of America","MF", "American Funds",  90_000_000, 15.0),
        ("AIVSX", "American Funds Investment Co of Am",  "MF", "American Funds",  60_000_000, 10.0),
        ("CAIBX", "American Funds Capital Income Builder","MF", "American Funds",  60_000_000, 10.0),
        ("PIMCO", "PIMCO Total Return Fund",              "MF", "PIMCO",           60_000_000, 10.0),
    ]
    for sym, fn, ft, ff, amt, pct in holdings_003:
        holdings_all.append({"advisor_id": "adv_interesting_003", "symbol": sym,
            "fund_name": fn, "fund_type": ft, "fund_family": ff,
            "aum_in_fund": amt, "pct_of_aum": pct, "as_of_date": as_of.isoformat()})
        flows_all.extend(generate_flows("adv_interesting_003", sym, amt, "normal"))
    signals_all.append({
        "advisor_id": "adv_interesting_003",
        "signal_type": "CROSS_SELL_ETF",
        "signal_score": 8.7,
        "signal_data": json.dumps({
            "summary": "100% mutual fund allocation, zero ETF exposure — prime QQQ cross-sell",
            "etf_allocation_pct": 0.0,
            "mf_allocation_pct": 100.0,
            "invesco_allocation_pct": 0.0,
            "recommended_product": "QQQ",
            "pitch": "Tax efficiency + liquidity upgrade: Convert $120M FXAIX → QQQ",
            "estimated_revenue_opportunity": "$360K annually at avg fee",
            "action": "Schedule ETF education webinar, provide cost comparison",
            "priority": "HIGH",
        }),
    })

    # ── 004: REVENUE_DEFENSE — was $1.2B, now $980M ─────────────────────────
    adv = {
        "advisor_id": "adv_interesting_004",
        "full_name": "Thomas Bergeron",
        "firm_name": "Merrill Lynch",
        "region": "NE",
        "channel": "BD",
        "aum_current": 980_000_000,
        "aum_12m_ago": 1_200_000_000,
        "client_count": 423,
        "email": "thomas.bergeron@ml.com",
        "phone": "(212) 555-0419",
        "city": "New York",
        "state": "NY",
    }
    advisors.append(adv)
    holdings_004 = [
        ("QQQ",  "Invesco QQQ Trust",               "ETF", "Invesco",  147_000_000, 15.0),
        ("IVVB", "Invesco S&P 500 UCITS ETF",        "ETF", "Invesco",   98_000_000, 10.0),
        ("VOO",  "Vanguard S&P 500 ETF",             "ETF", "Vanguard", 294_000_000, 30.0),
        ("IVV",  "iShares Core S&P 500 ETF",         "ETF", "iShares",  196_000_000, 20.0),
        ("VTI",  "Vanguard Total Stock Market ETF",  "ETF", "Vanguard", 147_000_000, 15.0),
        ("BND",  "Vanguard Total Bond Market ETF",   "ETF", "Vanguard",  98_000_000, 10.0),
    ]
    for sym, fn, ft, ff, amt, pct in holdings_004:
        holdings_all.append({"advisor_id": "adv_interesting_004", "symbol": sym,
            "fund_name": fn, "fund_type": ft, "fund_family": ff,
            "aum_in_fund": amt, "pct_of_aum": pct, "as_of_date": as_of.isoformat()})
        pattern = "heavy_outflow" if ff == "Vanguard" else "normal"
        flows_all.extend(generate_flows("adv_interesting_004", sym, amt, pattern))
    signals_all.append({
        "advisor_id": "adv_interesting_004",
        "signal_type": "REVENUE_DEFENSE",
        "signal_score": 9.0,
        "signal_data": json.dumps({
            "summary": "$220M AUM loss to Vanguard direct; Invesco share at risk",
            "aum_decline_pct": -18.3,
            "outflow_destination": "Vanguard",
            "invesco_at_risk_aum": 245_000_000,
            "action": "Immediate retention play — Invesco factor ETF vs Vanguard comparison",
            "retention_strategy": "Cost+performance comparison, smart beta pitch",
            "priority": "CRITICAL",
        }),
    })

    # ── 005: RIA_CONVERSION — BD, $750M, model portfolios ──────────────────
    adv = {
        "advisor_id": "adv_interesting_005",
        "full_name": "Jennifer Castillo",
        "firm_name": "Ameriprise Financial",
        "region": "W",
        "channel": "BD",
        "aum_current": 750_000_000,
        "aum_12m_ago": 720_000_000,
        "client_count": 285,
        "email": "jennifer.castillo@ameriprise.com",
        "phone": "(310) 555-0512",
        "city": "Los Angeles",
        "state": "CA",
    }
    advisors.append(adv)
    holdings_005 = [
        ("AMCAP", "American Funds AMCAP Fund",           "ModelPortfolio", "American Funds", 225_000_000, 30.0),
        ("AGTHX", "American Funds Growth Fund of America","ModelPortfolio", "American Funds", 187_500_000, 25.0),
        ("CAIBX", "American Funds Capital Income Builder","ModelPortfolio", "American Funds", 150_000_000, 20.0),
        ("AIVSX", "American Funds Investment Co of Am",  "ModelPortfolio", "American Funds", 112_500_000, 15.0),
        ("PIMCO", "PIMCO Total Return Fund",              "ModelPortfolio", "PIMCO",           75_000_000, 10.0),
    ]
    for sym, fn, ft, ff, amt, pct in holdings_005:
        holdings_all.append({"advisor_id": "adv_interesting_005", "symbol": sym,
            "fund_name": fn, "fund_type": ft, "fund_family": ff,
            "aum_in_fund": amt, "pct_of_aum": pct, "as_of_date": as_of.isoformat()})
        flows_all.extend(generate_flows("adv_interesting_005", sym, amt, "normal"))
    signals_all.append({
        "advisor_id": "adv_interesting_005",
        "signal_type": "RIA_CONVERSION",
        "signal_score": 7.8,
        "signal_data": json.dumps({
            "summary": "BD advisor with $750M in captive model portfolios — likely evaluating RIA independence",
            "channel": "BD",
            "model_portfolio_pct": 100.0,
            "proprietary_exposure_pct": 90.0,
            "indicators": ["Has attended 2 RIA conferences", "Searching for RIA custody solutions"],
            "action": "Present Invesco model portfolio solutions for RIA transition",
            "opportunity": "If converts to RIA, could reallocate $375M to open architecture",
            "priority": "MEDIUM",
        }),
    })

    # ── 006: DORMANT — $300M, no flows in 6 months ─────────────────────────
    adv = {
        "advisor_id": "adv_interesting_006",
        "full_name": "William Nakamura",
        "firm_name": "Raymond James",
        "region": "SW",
        "channel": "BD",
        "aum_current": 300_000_000,
        "aum_12m_ago": 295_000_000,
        "client_count": 178,
        "email": "william.nakamura@raymondjames.com",
        "phone": "(602) 555-0621",
        "city": "Phoenix",
        "state": "AZ",
    }
    advisors.append(adv)
    holdings_006 = [
        ("QQQ",  "Invesco QQQ Trust",               "ETF", "Invesco",   60_000_000, 20.0),
        ("IVOO", "Invesco S&P MidCap 400 ETF",       "ETF", "Invesco",   45_000_000, 15.0),
        ("VOO",  "Vanguard S&P 500 ETF",             "ETF", "Vanguard",  75_000_000, 25.0),
        ("IVV",  "iShares Core S&P 500 ETF",         "ETF", "iShares",   60_000_000, 20.0),
        ("AGG",  "iShares Core U.S. Aggregate Bond", "ETF", "iShares",   60_000_000, 20.0),
    ]
    for sym, fn, ft, ff, amt, pct in holdings_006:
        holdings_all.append({"advisor_id": "adv_interesting_006", "symbol": sym,
            "fund_name": fn, "fund_type": ft, "fund_family": ff,
            "aum_in_fund": amt, "pct_of_aum": pct, "as_of_date": as_of.isoformat()})
        flows_all.extend(generate_flows("adv_interesting_006", sym, amt, "dormant"))
    signals_all.append({
        "advisor_id": "adv_interesting_006",
        "signal_type": "DORMANT",
        "signal_score": 6.5,
        "signal_data": json.dumps({
            "summary": "Previously active advisor — zero flows for 6 consecutive months",
            "last_active_month": "2025-08-01",
            "months_dormant": 6,
            "prior_monthly_avg_flow": 1_200_000,
            "action": "Re-engagement call, check if advisor is leaving firm or shifting strategy",
            "risk": "May be consolidating to single custodian, losing Invesco exposure",
            "priority": "MEDIUM",
        }),
    })

    # ── 007: GROWTH_STAR — $200M→$320M (+60%), mostly QQQ + IVOO ──────────
    adv = {
        "advisor_id": "adv_interesting_007",
        "full_name": "Priya Menon",
        "firm_name": "Apex Financial Partners",
        "region": "W",
        "channel": "RIA",
        "aum_current": 320_000_000,
        "aum_12m_ago": 200_000_000,
        "client_count": 112,
        "email": "priya.menon@apexfp.com",
        "phone": "(415) 555-0732",
        "city": "San Francisco",
        "state": "CA",
    }
    advisors.append(adv)
    holdings_007 = [
        ("QQQ",  "Invesco QQQ Trust",         "ETF", "Invesco",  128_000_000, 40.0),
        ("IVOO", "Invesco S&P MidCap 400 ETF","ETF", "Invesco",   64_000_000, 20.0),
        ("KBWB", "Invesco KBW Bank ETF",       "ETF", "Invesco",   32_000_000, 10.0),
        ("VOO",  "Vanguard S&P 500 ETF",       "ETF", "Vanguard",  64_000_000, 20.0),
        ("VWO",  "Vanguard FTSE Emerging Markets","ETF","Vanguard", 32_000_000, 10.0),
    ]
    for sym, fn, ft, ff, amt, pct in holdings_007:
        holdings_all.append({"advisor_id": "adv_interesting_007", "symbol": sym,
            "fund_name": fn, "fund_type": ft, "fund_family": ff,
            "aum_in_fund": amt, "pct_of_aum": pct, "as_of_date": as_of.isoformat()})
        flows_all.extend(generate_flows("adv_interesting_007", sym, amt, "heavy_inflow"))
    signals_all.append({
        "advisor_id": "adv_interesting_007",
        "signal_type": "GROWTH_STAR",
        "signal_score": 9.1,
        "signal_data": json.dumps({
            "summary": "Explosive 60% AUM growth, 70% Invesco — accelerate this relationship",
            "aum_growth_pct": 60.0,
            "aum_added": 120_000_000,
            "invesco_pct": 70.0,
            "fastest_growing_fund": "QQQ",
            "action": "Offer VIP access to Invesco market insights, dedicated sales coverage",
            "expand_opportunity": ["IVOV (value tilt)", "BAB (muni bonds)", "PGX (income)"],
            "priority": "HIGH",
        }),
    })

    # ── 008: CONCENTRATED — $500M, 85% in single Invesco fund ──────────────
    adv = {
        "advisor_id": "adv_interesting_008",
        "full_name": "Charles Pemberton",
        "firm_name": "Wells Fargo Advisors",
        "region": "NE",
        "channel": "BD",
        "aum_current": 500_000_000,
        "aum_12m_ago": 488_000_000,
        "client_count": 205,
        "email": "charles.pemberton@wellsfargoadvisors.com",
        "phone": "(203) 555-0883",
        "city": "Stamford",
        "state": "CT",
    }
    advisors.append(adv)
    holdings_008 = [
        ("QQQ",  "Invesco QQQ Trust",               "ETF", "Invesco", 425_000_000, 85.0),
        ("AGG",  "iShares Core U.S. Aggregate Bond", "ETF", "iShares",  50_000_000, 10.0),
        ("GLD",  "SPDR Gold Shares",                 "ETF", "State Street", 25_000_000, 5.0),
    ]
    for sym, fn, ft, ff, amt, pct in holdings_008:
        holdings_all.append({"advisor_id": "adv_interesting_008", "symbol": sym,
            "fund_name": fn, "fund_type": ft, "fund_family": ff,
            "aum_in_fund": amt, "pct_of_aum": pct, "as_of_date": as_of.isoformat()})
        flows_all.extend(generate_flows("adv_interesting_008", sym, amt, "normal"))
    signals_all.append({
        "advisor_id": "adv_interesting_008",
        "signal_type": "CONCENTRATED",
        "signal_score": 7.2,
        "signal_data": json.dumps({
            "summary": "85% concentrated in QQQ — diversification conversation opportunity",
            "concentrated_fund": "QQQ",
            "concentration_pct": 85.0,
            "concentration_aum": 425_000_000,
            "risk": "Single position concentration creates fee compression and redemption risk",
            "action": "Present factor diversification: IVOO, IVOV, KBWB to complement QQQ",
            "diversification_opportunity": 150_000_000,
            "priority": "MEDIUM",
        }),
    })

    # ── 009: COMPETITOR_HEAVY — $900M, 90% iShares, zero Invesco ───────────
    adv = {
        "advisor_id": "adv_interesting_009",
        "full_name": "Donald Richardson",
        "firm_name": "LPL Financial",
        "region": "SE",
        "channel": "BD",
        "aum_current": 900_000_000,
        "aum_12m_ago": 875_000_000,
        "client_count": 380,
        "email": "donald.richardson@lplfinancial.com",
        "phone": "(704) 555-0942",
        "city": "Charlotte",
        "state": "NC",
    }
    advisors.append(adv)
    holdings_009 = [
        ("IVV",  "iShares Core S&P 500 ETF",          "ETF", "iShares", 270_000_000, 30.0),
        ("AGG",  "iShares Core U.S. Aggregate Bond",   "ETF", "iShares", 180_000_000, 20.0),
        ("EFA",  "iShares MSCI EAFE ETF",               "ETF", "iShares", 135_000_000, 15.0),
        ("LQD",  "iShares iBoxx $ IG Corp Bond ETF",    "ETF", "iShares", 135_000_000, 15.0),
        ("ACWI", "iShares MSCI ACWI ETF",               "ETF", "iShares",  90_000_000, 10.0),
        ("TLT",  "iShares 20+ Year Treasury Bond ETF",  "ETF", "iShares",  45_000_000,  5.0),
        ("VTI",  "Vanguard Total Stock Market ETF",     "ETF", "Vanguard",  45_000_000,  5.0),
    ]
    for sym, fn, ft, ff, amt, pct in holdings_009:
        holdings_all.append({"advisor_id": "adv_interesting_009", "symbol": sym,
            "fund_name": fn, "fund_type": ft, "fund_family": ff,
            "aum_in_fund": amt, "pct_of_aum": pct, "as_of_date": as_of.isoformat()})
        flows_all.extend(generate_flows("adv_interesting_009", sym, amt, "normal"))
    signals_all.append({
        "advisor_id": "adv_interesting_009",
        "signal_type": "COMPETITOR_HEAVY",
        "signal_score": 8.4,
        "signal_data": json.dumps({
            "summary": "$900M advisor with ZERO Invesco exposure — 90% iShares/Vanguard",
            "invesco_allocation_pct": 0.0,
            "ishares_allocation_pct": 90.0,
            "total_aum": 900_000_000,
            "largest_position": {"symbol": "IVV", "aum": 270_000_000},
            "action": "QQQ vs IVV performance pitch — $270M IVV position is the entry point",
            "potential_conversion": 450_000_000,
            "pitch_angle": "QQQ outperformance over 10yr, IVV overlap with VOO — consolidate to QQQ",
            "priority": "HIGH",
        }),
    })

    # ── 010: MEETING_SOON — large advisor, calendar note ───────────────────
    adv = {
        "advisor_id": "adv_interesting_010",
        "full_name": "Elizabeth Fontaine",
        "firm_name": "JP Morgan Private Bank",
        "region": "NE",
        "channel": "Bank",
        "aum_current": 1_400_000_000,
        "aum_12m_ago": 1_350_000_000,
        "client_count": 520,
        "email": "elizabeth.fontaine@jpmorgan.com",
        "phone": "(212) 555-1001",
        "city": "New York",
        "state": "NY",
    }
    advisors.append(adv)
    holdings_010 = [
        ("QQQ",  "Invesco QQQ Trust",               "ETF",  "Invesco",  280_000_000, 20.0),
        ("BKAG", "Invesco BulletShares 2026 Corp",   "ETF",  "Invesco",  140_000_000, 10.0),
        ("IVV",  "iShares Core S&P 500 ETF",         "ETF",  "iShares",  280_000_000, 20.0),
        ("LQD",  "iShares iBoxx $ IG Corp Bond ETF", "ETF",  "iShares",  140_000_000, 10.0),
        ("VOO",  "Vanguard S&P 500 ETF",             "ETF",  "Vanguard", 280_000_000, 20.0),
        ("VEA",  "Vanguard FTSE Developed Markets",  "ETF",  "Vanguard", 140_000_000, 10.0),
        ("GLD",  "SPDR Gold Shares",                 "ETF",  "State Street", 140_000_000, 10.0),
    ]
    for sym, fn, ft, ff, amt, pct in holdings_010:
        holdings_all.append({"advisor_id": "adv_interesting_010", "symbol": sym,
            "fund_name": fn, "fund_type": ft, "fund_family": ff,
            "aum_in_fund": amt, "pct_of_aum": pct, "as_of_date": as_of.isoformat()})
        flows_all.extend(generate_flows("adv_interesting_010", sym, amt, "normal"))
    signals_all.append({
        "advisor_id": "adv_interesting_010",
        "signal_type": "MEETING_SOON",
        "signal_score": 8.8,
        "signal_data": json.dumps({
            "summary": "$1.4B JP Morgan advisor — annual review meeting scheduled March 15",
            "meeting_date": "2026-03-15",
            "meeting_type": "Annual Portfolio Review",
            "meeting_location": "JP Morgan HQ, 383 Madison Ave, New York",
            "invesco_allocation_pct": 30.0,
            "invesco_aum": 420_000_000,
            "agenda_items": [
                "Q1 2026 performance review",
                "Fixed income strategy refresh — pitch BKLC ladder",
                "ESG overlay discussion — Invesco ESG products",
            ],
            "key_contact": "Craig Lieb, Invesco Regional Sales Director",
            "action": "Prepare QQQ + BulletShares laddering pitch deck",
            "priority": "HIGH",
        }),
    })

    return advisors, holdings_all, flows_all, signals_all


# ─── Main generation ───────────────────────────────────────────────────────────

def main():
    print("Generating seed data...")

    interesting_advisors, interesting_holdings, interesting_flows, signals = build_interesting_advisors()
    interesting_ids = {a["advisor_id"] for a in interesting_advisors}

    # ── Generate 490 random advisors (+ 10 interesting = 500 total) ─────────
    all_advisors = list(interesting_advisors)
    all_holdings = list(interesting_holdings)
    all_flows = list(interesting_flows)

    used_names = set()
    for i in range(490):
        advisor_id = f"adv_{i+1:05d}"

        # Name
        for _ in range(100):
            fn = random.choice(FIRST_NAMES)
            ln = random.choice(LAST_NAMES)
            name = f"{fn} {ln}"
            if name not in used_names:
                used_names.add(name)
                break

        # Firm & channel
        firm_data = random.choice(FIRMS)
        firm_name, channel = firm_data

        # Location
        region = pick_region()
        city, state = pick_location(region)

        # AUM
        aum_current = rand_aum()
        aum_12m_ago = rand_aum_12m_ago(aum_current)
        client_count = rand_client_count(aum_current)

        advisor = {
            "advisor_id": advisor_id,
            "full_name": name,
            "firm_name": firm_name,
            "region": region,
            "channel": channel,
            "aum_current": aum_current,
            "aum_12m_ago": aum_12m_ago,
            "client_count": client_count,
            "email": rand_email(name, firm_name),
            "phone": rand_phone(),
            "city": city,
            "state": state,
        }
        all_advisors.append(advisor)

        # Holdings
        n_holdings = random.randint(3, 8)
        holdings = generate_holdings(advisor_id, aum_current, invesco_pct=0.30, n_holdings=n_holdings)
        all_holdings.extend(holdings)

        # Flows
        r = random.random()
        if r < 0.10:
            pattern = "heavy_outflow"
        elif r < 0.20:
            pattern = "heavy_inflow"
        else:
            pattern = "normal"

        for h in holdings:
            all_flows.extend(generate_flows(advisor_id, h["symbol"], h["aum_in_fund"], pattern))

    print(f"  Advisors: {len(all_advisors)}")
    print(f"  Holdings: {len(all_holdings)}")
    print(f"  Flows:    {len(all_flows)}")
    print(f"  Signals:  {len(signals)}")

    # ── Write SQL ────────────────────────────────────────────────────────────
    with open(OUT_FILE, "w") as f:
        f.write("-- Full seed data for Invesco Signal Studio analytical DB\n")
        f.write("-- Generated by generate_full_seed.py\n")
        f.write("-- Run: psql $ANALYTICAL_DATABASE_URL < full_seed.sql\n\n")

        # Schema
        with open("/data/workspace/seeds/advisors_schema.sql") as schema_f:
            f.write(schema_f.read())
        f.write("\n\n")

        # Advisors
        f.write("-- ─── ADVISORS ────────────────────────────────────────────────────────────\n")
        for a in all_advisors:
            f.write(
                f"INSERT INTO advisors "
                f"(advisor_id, full_name, firm_name, region, channel, aum_current, aum_12m_ago, "
                f"client_count, email, phone, city, state) VALUES ("
                f"{esc(a['advisor_id'])}, {esc(a['full_name'])}, {esc(a['firm_name'])}, "
                f"{esc(a['region'])}, {esc(a['channel'])}, {a['aum_current']}, {a['aum_12m_ago']}, "
                f"{a['client_count']}, {esc(a['email'])}, {esc(a['phone'])}, "
                f"{esc(a['city'])}, {esc(a['state'])});\n"
            )

        f.write("\n-- ─── HOLDINGS ───────────────────────────────────────────────────────────\n")
        for h in all_holdings:
            f.write(
                f"INSERT INTO holdings "
                f"(advisor_id, symbol, fund_name, fund_type, fund_family, aum_in_fund, pct_of_aum, as_of_date) "
                f"VALUES ({esc(h['advisor_id'])}, {esc(h['symbol'])}, {esc(h['fund_name'])}, "
                f"{esc(h['fund_type'])}, {esc(h['fund_family'])}, {h['aum_in_fund']}, "
                f"{h['pct_of_aum']}, '{h['as_of_date']}');\n"
            )

        f.write("\n-- ─── FLOWS ──────────────────────────────────────────────────────────────\n")
        for fl in all_flows:
            f.write(
                f"INSERT INTO flows "
                f"(advisor_id, symbol, flow_month, net_flow, gross_inflow, gross_outflow) "
                f"VALUES ({esc(fl['advisor_id'])}, {esc(fl['symbol'])}, '{fl['flow_month']}', "
                f"{fl['net_flow']}, {fl['gross_inflow']}, {fl['gross_outflow']});\n"
            )

        f.write("\n-- ─── SIGNALS ────────────────────────────────────────────────────────────\n")
        for s in signals:
            f.write(
                f"INSERT INTO signals "
                f"(advisor_id, signal_type, signal_score, signal_data, status) "
                f"VALUES ({esc(s['advisor_id'])}, {esc(s['signal_type'])}, "
                f"{s['signal_score']}, {esc(s['signal_data'])}::jsonb, 'active');\n"
            )

    print(f"\nOutput: {OUT_FILE}")
    print("Done!")
    return len(all_advisors), len(all_holdings), len(all_flows), len(signals)


if __name__ == "__main__":
    main()
