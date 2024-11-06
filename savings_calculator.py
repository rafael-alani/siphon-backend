from datetime import datetime
from typing import List, Optional
from models import Trade, TimeFrame, SavingsResult, Commodity, PricePoint
from price_analytics import PriceAnalytics

class SavingsCalculator:
    def __init__(self, price_analytics: PriceAnalytics):
        self.price_analytics = price_analytics

    def _get_market_price_at_time(self, commodity: Commodity, trade_time: datetime, market_prices: List[PricePoint]) -> float:
        # Find the closest market price point to the trade time
        closest_price_point = min(
            market_prices,
            key=lambda x: abs((x.timestamp - trade_time).total_seconds()),
            default=None
        )
        return closest_price_point.price if closest_price_point else 0

    def calculate_savings(
        self,
        trades: List[Trade],
        timeframe: TimeFrame,
        company_name: Optional[str] = None
    ) -> SavingsResult:
        cutoff_time = datetime.now() - self.price_analytics.get_time_delta(timeframe)
        
        # Filter trades by time and company if specified
        relevant_trades = [
            trade for trade in trades
            if trade.status == TradeStatus.COMPLETED
            and trade.time and trade.time >= cutoff_time
            and (not company_name or 
                 trade.requester_company == company_name or 
                 trade.fulfiller_company == company_name)
        ]

        total_savings = 0
        savings_by_commodity = {commodity: 0 for commodity in Commodity}
        currency = relevant_trades[0].price.currency if relevant_trades else "EUR"

        # Calculate savings for each commodity
        for commodity in Commodity:
            commodity_trades = [t for t in relevant_trades if t.commodity == commodity]
            if not commodity_trades:
                continue

            # Get market prices for the timeframe
            market_prices = self.price_analytics.get_market_prices(commodity, timeframe)

            # Calculate savings for each trade
            for trade in commodity_trades:
                market_price = self._get_market_price_at_time(
                    commodity,
                    trade.time,
                    market_prices
                )
                
                # Calculate savings (market price - actual price) * amount
                trade_savings = (market_price - trade.price.value) * trade.amount.value
                savings_by_commodity[commodity] += trade_savings
                total_savings += trade_savings

        return SavingsResult(
            total_savings=total_savings,
            savings_by_commodity=savings_by_commodity,
            currency=currency,
            timeframe=timeframe
        )