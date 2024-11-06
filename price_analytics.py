from datetime import datetime, timedelta
from typing import List
import random
from models import Trade, PricePoint, Commodity, TimeFrame

class PriceAnalytics:
    MARKET_MULTIPLIERS = {
        Commodity.ELECTRICITY: 1.25,
        Commodity.GAS: 1.15,
        Commodity.HEAT: 1.1,
        Commodity.HYDROGEN: 1.35
    }

    @staticmethod
    def get_time_delta(timeframe: TimeFrame) -> timedelta:
        return {
            TimeFrame.DAY: timedelta(hours=24),
            TimeFrame.WEEK: timedelta(days=7),
            TimeFrame.MONTH: timedelta(days=30),
            TimeFrame.YEAR: timedelta(days=365)
        }[timeframe]

    def calculate_average_prices(
        self,
        trades: List[Trade],
        commodity: Commodity,
        timeframe: TimeFrame
    ) -> List[PricePoint]:
        cutoff_time = datetime.now() - self.get_time_delta(timeframe)
        
        # Filter trades by commodity and time
        relevant_trades = [
            trade for trade in trades
            if trade.commodity == commodity
            and trade.time and trade.time >= cutoff_time
        ]

        if not relevant_trades:
            return []

        # Group trades by hour and calculate averages
        price_points = []
        current_time = min(trade.time for trade in relevant_trades)
        end_time = datetime.now()

        while current_time <= end_time:
            next_time = current_time + timedelta(hours=3)  # 3-hour intervals
            period_trades = [
                trade for trade in relevant_trades
                if trade.time and current_time <= trade.time < next_time
            ]

            if period_trades:
                avg_price = sum(t.price.value for t in period_trades) / len(period_trades)
                price_points.append(PricePoint(
                    timestamp=current_time,
                    price=avg_price
                ))

            current_time = next_time

        return price_points

    def get_market_prices(
        self,
        commodity: Commodity,
        timeframe: TimeFrame
    ) -> List[PricePoint]:
        cutoff_time = datetime.now() - self.get_time_delta(timeframe)
        current_time = cutoff_time
        price_points = []
        base_price = 100  # Starting base price

        while current_time <= datetime.now():
            # Create some price volatility using sine wave and random factors
            hours_passed = (current_time - cutoff_time).total_seconds() / 3600
            volatility = (1 + 0.1 * random.random()) * (1 + 0.05 * 
                        math.sin(hours_passed * math.pi / 12))  # 12-hour cycle
            
            market_price = base_price * volatility * self.MARKET_MULTIPLIERS[commodity]
            
            price_points.append(PricePoint(
                timestamp=current_time,
                price=market_price
            ))
            
            current_time += timedelta(hours=3)  # 3-hour intervals

        return price_points