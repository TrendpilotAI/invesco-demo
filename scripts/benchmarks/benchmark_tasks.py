"""Benchmark task definitions for model comparison."""

TASKS = {
    "coding": {
        "name": "FastAPI CRUD App",
        "system": "You are an expert Python developer.",
        "prompt": "Build a complete FastAPI application with: 1) User model with id, name, email, created_at. 2) Full CRUD endpoints (POST /users, GET /users, GET /users/{id}, PUT /users/{id}, DELETE /users/{id}). 3) Pydantic schemas for request/response. 4) SQLAlchemy async with SQLite. 5) At least 5 pytest tests. Return all code in a single response.",
        "max_tokens": 4000,
    },
    "strategic": {
        "name": "GTM Strategy",
        "system": "You are a senior go-to-market strategist for B2B fintech.",
        "prompt": "Write a detailed GTM strategy for an AI-powered meeting prep tool for enterprise asset managers (think Invesco, BlackRock). The tool embeds in Salesforce and saves wholesalers 47 minutes per meeting. Cover: target segments, pricing model, channel strategy, competitive positioning, first 90-day plan, key metrics, and potential objections with responses. Be specific with numbers.",
        "max_tokens": 4000,
    },
    "debugging": {
        "name": "Bug Detection",
        "system": "You are a senior security engineer doing a code review.",
        "prompt": """Review this Python code and identify ALL security vulnerabilities, bugs, and improvements:

```python
import sqlite3
from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    query = f"SELECT * FROM users WHERE username='{username}' AND password='{password}'"
    cursor.execute(query)
    user = cursor.fetchone()
    if user:
        return jsonify({'token': username + ':' + password})
    return jsonify({'error': 'Invalid'}), 401

@app.route('/users/<id>')
def get_user(id):
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute(f"SELECT * FROM users WHERE id={id}")
    return jsonify(cursor.fetchone())

@app.route('/upload', methods=['POST'])
def upload():
    f = request.files['file']
    f.save('/uploads/' + f.filename)
    return 'ok'

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
```

For each issue: describe the vulnerability, show the fix, and rate severity (Critical/High/Medium/Low).""",
        "max_tokens": 4000,
    },
    "architecture": {
        "name": "System Design",
        "system": "You are a principal software architect.",
        "prompt": "Design a real-time financial signal processing system that: 1) Ingests 100K events/second from market data feeds. 2) Runs NL-to-SQL queries against a 200-column analytical database. 3) Generates personalized advisor alerts within 500ms. 4) Scales to 10,000 concurrent users. 5) Maintains 99.99% uptime. Include: component diagram (text), technology choices with justification, data flow, failure modes, and cost estimate for running on AWS/Railway.",
        "max_tokens": 4000,
    },
    "analysis": {
        "name": "Data Analysis",
        "system": "You are a quantitative analyst at a wealth management firm.",
        "prompt": """Given this portfolio data, provide a comprehensive analysis:

Portfolio: $2.3B AUM across 450 advisors
- 60% equities (40% US large cap, 15% international, 5% emerging)
- 25% fixed income (15% investment grade, 7% high yield, 3% munis)
- 10% alternatives (5% real estate, 3% private equity, 2% hedge funds)
- 5% cash

Market conditions: Fed holding rates at 4.25%, inflation 2.8%, S&P up 12% YTD, 10Y treasury at 4.1%, credit spreads widening 20bps.

Analyze: 1) Portfolio risk exposures. 2) Rebalancing recommendations with specific % changes. 3) Three scenarios (bull/base/bear) with portfolio impact. 4) Top 5 advisor actions to recommend. 5) Competitive positioning vs Vanguard/BlackRock model portfolios.""",
        "max_tokens": 4000,
    },
}
