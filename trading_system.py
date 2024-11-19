from typing import List, Dict, Optional
from models import Trade, Company, TradeType, TradeStatus, Commodity
from trading_logic import TradingLogic
from led_controller import LEDController

class TradingSystem:
    def __init__(self, led_controller: Optional[LEDController] = None):
        self.offers: List[Trade] = []
        self.requests: List[Trade] = []
        self.trade_history: List[Trade] = []
        self.companies: Dict[str, Company] = {}
        self.trading_logic = TradingLogic(led_controller=led_controller)

    def add_trade(self, trade: Trade) -> None:
        if trade.status == TradeStatus.PENDING:
            if trade.type == TradeType.SELL:
                self.offers.append(trade)
            else:
                self.requests.append(trade)
            # Check for compatible trades after adding a new one
            self.trading_logic.check_compatible_trades(self)
        else:
            self.trade_history.append(trade)

    def get_offers(self) -> List[Trade]:
        return self.offers

    def get_requests(self) -> List[Trade]:
        return self.requests

    def get_trade_history(self) -> List[Trade]:
        return self.trade_history

    def add_company(self, company: Company) -> None:
        self.companies[company.name] = company

    def get_company(self, name: str) -> Optional[Company]:
        return self.companies.get(name)

    def get_all_companies(self) -> List[Company]:
        return list(self.companies.values())

    def find_matching_trades(self, commodity: Commodity) -> dict:
        """
        Find the lowest offer price and highest request price for a given commodity
        """
        relevant_offers = [
            trade for trade in self.offers 
            if trade.commodity == commodity
        ]
        relevant_requests = [
            trade for trade in self.requests 
            if trade.commodity == commodity
        ]

        if not relevant_offers or not relevant_requests:
            return {
                "status": "no_match",
                "lowest_offer": None,
                "highest_request": None
            }

        lowest_offer = min(relevant_offers, key=lambda x: x.price.value)
        highest_request = max(relevant_requests, key=lambda x: x.price.value)

        return {
            "status": "match_found" if lowest_offer.price.value <= highest_request.price.value else "no_match",
            "lowest_offer": lowest_offer,
            "highest_request": highest_request
        }

    def remove_company(self, name: str) -> None:
        if name in self.companies:
            del self.companies[name]