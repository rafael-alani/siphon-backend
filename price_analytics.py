from datetime import datetime, timedelta, timezone
from typing import List, Dict
from collections import defaultdict
import statistics
from models import Trade, PricePoint, Commodity, TimeFrame
import json
from pathlib import Path

class PriceAnalytics:
    def __init__(self):
        json_path = Path(__file__).parent / "demo_trades.json"
        with open(json_path, 'r') as f:
            self.trades = json.load(f)

    def _get_trades_in_timeframe(self, commodity: Commodity, timeframe: TimeFrame) -> List[Dict]:
        end_time = datetime.now(timezone.utc)
        start_time = end_time - self.get_time_delta(timeframe)
        
        filtered_trades = [
            trade for trade in self.trades
            if (trade['commodity'].lower() == commodity.value.lower() and
                datetime.fromisoformat(trade['time'].replace('Z', '+00:00')) >= start_time)
        ]
        
        return filtered_trades

    def calculate_average_prices(
        self,
        trades: List[Trade],
        commodity: Commodity,
        timeframe: TimeFrame
    ) -> List[PricePoint]:
        relevant_trades = self._get_trades_in_timeframe(commodity, timeframe)
        
        # Group trades by hour
        hourly_prices = defaultdict(list)
        for trade in relevant_trades:
            timestamp = datetime.fromisoformat(trade['time'].replace('Z', '+00:00'))
            # Round to nearest hour, preserving timezone
            timestamp = timestamp.replace(minute=0, second=0, microsecond=0)
            hourly_prices[timestamp].append(trade['price']['value'])
        
        # Calculate average price for each hour
        price_points = [
            PricePoint(
                timestamp=timestamp,
                price=statistics.mean(prices) if prices else 0
            )
            for timestamp, prices in sorted(hourly_prices.items())
        ]
        
        return price_points

    def get_market_prices(
        self,
        commodity: Commodity,
        timeframe: TimeFrame
    ) -> List[PricePoint]:
        return self.calculate_average_prices([], commodity, timeframe)

    @staticmethod
    def get_time_delta(timeframe: TimeFrame) -> timedelta:
        return {
            TimeFrame.DAY: timedelta(hours=24),
            TimeFrame.WEEK: timedelta(days=7),
            TimeFrame.MONTH: timedelta(days=30),
            TimeFrame.YEAR: timedelta(days=365)
        }[timeframe]