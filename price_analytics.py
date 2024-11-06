from datetime import datetime, timedelta
from typing import List
import random
import math
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
                # Use the raw price values from trades
                avg_price = sum(t.price.value for t in period_trades) / len(period_trades)
                price_points.append(PricePoint(
                    timestamp=current_time,
                    price=avg_price
                ))

            current_time = next_time

        return price_points