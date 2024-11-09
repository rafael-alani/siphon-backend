from fastapi import FastAPI, HTTPException
from models import Trade, Company, Commodity, TimeFrame, SavingsResult
from trading_system import TradingSystem
from price_analytics import PriceAnalytics
from savings_calculator import SavingsCalculator
from load_demo_data import load_demo_data
from fastapi.middleware.cors import CORSMiddleware  
import uvicorn
import math
from led_controller import LEDController

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:5174"],  # Add your frontend URL
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

# Initialize LED controller
led_controller = LEDController()

# Initialize trading system with LED controller
trading_system = TradingSystem(led_controller=led_controller)

price_analytics = PriceAnalytics()
savings_calculator = SavingsCalculator(price_analytics)

# Load demo data on startup
load_demo_data(trading_system)

# After loading demo data, assign LEDs to companies
led_controller.assign_company_leds(trading_system.companies)

@app.post("/trades")
async def create_trade(trade: Trade):
    trading_system.add_trade(trade)
    return {"status": "success", "trade": trade}

@app.get("/trades/offers")
async def get_offers():
    return trading_system.get_offers()

@app.get("/trades/requests")
async def get_requests():
    return trading_system.get_requests()

@app.get("/trades/history")
async def get_trade_history():
    return trading_system.get_trade_history()

@app.post("/companies")
async def create_company(company: Company):
    trading_system.add_company(company)
    return {"status": "success", "company": company}

@app.get("/companies/{name}")
async def get_company(name: str):
    company = trading_system.get_company(name)
    if not company:
        raise HTTPException(status_code=404, detail="Company not found")
    return company

@app.get("/trades/matching/{commodity}")
async def find_matching_trades(commodity: Commodity):
    return trading_system.find_matching_trades(commodity)

# Price analytics endpoints for actual trade prices
@app.get("/analytics/prices/electricity/{timeframe}")
async def get_electricity_prices(timeframe: TimeFrame):
    return price_analytics.calculate_average_prices(
        trading_system.trade_history,
        Commodity.ELECTRICITY,
        timeframe
    )

@app.get("/analytics/prices/gas/{timeframe}")
async def get_gas_prices(timeframe: TimeFrame):
    return price_analytics.calculate_average_prices(
        trading_system.trade_history,
        Commodity.GAS,
        timeframe
    )

@app.get("/analytics/prices/heat/{timeframe}")
async def get_heat_prices(timeframe: TimeFrame):
    return price_analytics.calculate_average_prices(
        trading_system.trade_history,
        Commodity.HEAT,
        timeframe
    )

@app.get("/analytics/prices/hydrogen/{timeframe}")
async def get_hydrogen_prices(timeframe: TimeFrame):
    return price_analytics.calculate_average_prices(
        trading_system.trade_history,
        Commodity.HYDROGEN,
        timeframe
    )

# Market price endpoints
@app.get("/analytics/market-prices/electricity/{timeframe}")
async def get_electricity_market_prices(timeframe: TimeFrame):
    return price_analytics.get_market_prices(Commodity.ELECTRICITY, timeframe)

@app.get("/analytics/market-prices/gas/{timeframe}")
async def get_gas_market_prices(timeframe: TimeFrame):
    return price_analytics.get_market_prices(Commodity.GAS, timeframe)

@app.get("/analytics/market-prices/heat/{timeframe}")
async def get_heat_market_prices(timeframe: TimeFrame):
    return price_analytics.get_market_prices(Commodity.HEAT, timeframe)

@app.get("/analytics/market-prices/hydrogen/{timeframe}")
async def get_hydrogen_market_prices(timeframe: TimeFrame):
    return price_analytics.get_market_prices(Commodity.HYDROGEN, timeframe)

# Savings calculation endpoints
@app.get("/analytics/savings/{timeframe}", response_model=SavingsResult)
async def get_total_savings(timeframe: TimeFrame):
    return savings_calculator.calculate_savings(
        trading_system.trade_history,
        timeframe
    )

@app.get("/analytics/savings/company/{company_name}/{timeframe}", response_model=SavingsResult)
async def get_company_savings(company_name: str, timeframe: TimeFrame):
    if company_name not in trading_system.companies:
        raise HTTPException(status_code=404, detail="Company not found")
    
    return savings_calculator.calculate_savings(
        trading_system.trade_history,
        timeframe,
        company_name
    )

@app.post("/trades/offer")
async def create_offer(trade: Trade):
    if trade.type != TradeType.SELL:
        raise HTTPException(status_code=400, detail="Trade must be of type SELL for offers")
    trading_system.add_trade(trade)
    return {"status": "success", "trade": trade}

@app.post("/trades/request")
async def create_request(trade: Trade):
    if trade.type != TradeType.BUY:
        raise HTTPException(status_code=400, detail="Trade must be of type BUY for requests")
    trading_system.add_trade(trade)
    return {"status": "success", "trade": trade}

@app.get("/companies")
async def get_companies():
    return trading_system.get_all_companies()

@app.delete("/companies/{name}")
async def delete_company(name: str):
    if name not in trading_system.companies:
        raise HTTPException(status_code=404, detail="Company not found")
    del trading_system.companies[name]
    return {"status": "success", "message": f"Company {name} deleted"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)