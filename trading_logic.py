from datetime import datetime
from typing import List
from models import Trade, TradeStatus

class TradingLogic:
    def __init__(self, led_controller=None):
        self.led_controller = led_controller

    def sort_request_list(self, requests: List[Trade]) -> List[Trade]:
        """Sort requests by price in descending order (highest first)"""
        return sorted(requests, key=lambda x: x.price.value, reverse=True)

    def sort_offer_list(self, offers: List[Trade]) -> List[Trade]:
        """Sort offers by price in ascending order (lowest first)"""
        return sorted(offers, key=lambda x: x.price.value)

    def check_compatible_trades(self, trading_system) -> None:
        """Match compatible trades and update their status"""
        sorted_requests = self.sort_request_list(trading_system.requests)
        sorted_offers = self.sort_offer_list(trading_system.offers)

        # Update the main lists with sorted versions
        trading_system.requests = sorted_requests
        trading_system.offers = sorted_offers

        offers_to_remove = set()
        requests_to_remove = set()


        for offer in sorted_offers:
            if offer in offers_to_remove:
                continue

            for request in sorted_requests:
                if request in requests_to_remove:
                    continue

                # Check if commodities match
                if offer.commodity != request.commodity:
                    continue

                # Check if price is compatible
                if request.price.value / request.amount.value < offer.price.value / offer.amount.value:
                    continue

                if offer.requester_company == request.requester_company:
                    continue

                if offer.status == TradeStatus.COMPLETED or request.status == TradeStatus.COMPLETED:
                    continue

                current_time = datetime.now()

                # Handle matching based on amounts
                if offer.amount.value > request.amount.value:
                    # Complete the request
                    request.status = TradeStatus.COMPLETED
                    request.time = current_time
                    trading_system.trade_history.append(request)
                    requests_to_remove.add(request)
                    
                    # Update offer amount
                    offer.amount.value -= request.amount.value
                    # offer.price.value = offer.price.value * (offer.amount.value - request.amount.value) / offer.amount.value

                    # Visualize the trade
                    if self.led_controller:
                        self.led_controller.visualize_trade(offer, request)

                elif request.amount.value > offer.amount.value:
                    # Complete the offer
                    offer.status = TradeStatus.COMPLETED
                    offer.time = current_time
                    trading_system.trade_history.append(offer)
                    offers_to_remove.add(offer)
                    
                    # Update request amount
                    request.amount.value -= offer.amount.value
                    # request.price.value = request.price.value * (request.amount.value - offer.amount.value) / request.amount.value

                    # Visualize the trade
                    if self.led_controller:
                        self.led_controller.visualize_trade(offer, request)

                else:  # Equal amounts
                    # Complete both trades
                    offer.status = TradeStatus.COMPLETED
                    request.status = TradeStatus.COMPLETED
                    offer.time = current_time
                    request.time = current_time
                    trading_system.trade_history.extend([offer, request])
                    offers_to_remove.add(offer)
                    requests_to_remove.add(request)

                    # Visualize the trade
                    if self.led_controller:
                        self.led_controller.visualize_trade(offer, request)

        # Remove completed trades from original lists
        trading_system.offers = [
            offer for offer in trading_system.offers 
            if offer not in offers_to_remove
        ]
        trading_system.requests = [
            request for request in trading_system.requests 
            if request not in requests_to_remove
        ]