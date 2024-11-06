import json
from datetime import datetime
from models import Company, Trade, ResourceState
from trading_system import TradingSystem

def load_demo_data(trading_system: TradingSystem):
    # Load companies
    with open('demo_companies.json', 'r') as f:
        companies_data = json.load(f)
        
    for company_data in companies_data:
        company = Company(
            name=company_data['name'],
            location=company_data['location'],
            statuses=[ResourceState(**status) for status in company_data['statuses']],
            last_active=datetime.now()
        )
        trading_system.add_company(company)
    
    # Load historical trades
    with open('demo_trades.json', 'r') as f:
        trades_data = json.load(f)
        
    for trade_data in trades_data:
        trade_data['time'] = datetime.fromisoformat(trade_data['time'].replace('Z', '+00:00'))
        trade = Trade(**trade_data)
        trading_system.add_trade(trade)

    print(f"Loaded {len(companies_data)} companies")
    print(f"Loaded {len(trades_data)} historical trades")