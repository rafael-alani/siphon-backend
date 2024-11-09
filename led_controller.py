import board
import p9813
import time
from threading import Thread
from typing import Dict
from models import Trade, Company

class LEDController:
    def __init__(self, pin_clk=board.D13, pin_data=board.D10):
        self.pin_clk = pin_clk
        self.pin_data = pin_data
        self.company_to_led_map: Dict[str, int] = {}
        self.current_led = 0
        
        # Initialize LED strip
        self.num_leds = 0  # Will be set when companies are added
        self.leds = None
        
    def assign_company_leds(self, companies: Dict[str, Company]):
        """Assign each company to a pair of LEDs"""
        self.num_leds = len(companies) * 2  # Each company gets 2 LEDs
        self.leds = p9813.P9813(self.pin_clk, self.pin_data, self.num_leds)
        self.leds.reset()
        
        # Assign LED pairs to companies
        for company_name in companies:
            self.company_to_led_map[company_name] = self.current_led
            self.current_led += 2
            
    def _animate_trade(self, offer_led: int, request_led: int):
        """Create trail effect for a trade"""
        # Offer company animation (red trail towards pi)
        for intensity in range(255, 0, -5):
            self.leds[offer_led] = (intensity, 0, 0)
            self.leds.write()
            time.sleep(0.01)
            
        # Request company animation (green trail from pi)
        for intensity in range(0, 255, 5):
            self.leds[request_led] = (0, intensity, 0)
            self.leds.write()
            time.sleep(0.01)
            
        # Reset LEDs
        self.leds[offer_led] = (0, 0, 0)
        self.leds[request_led] = (0, 0, 0)
        self.leds.write()

    def visualize_trade(self, offer: Trade, request: Trade):
        """Trigger LED animation for a trade in a non-blocking way"""
        offer_led = self.company_to_led_map[offer.requester_company]
        request_led = self.company_to_led_map[request.requester_company] + 1
        
        # Run animation in a separate thread to not block the main process
        Thread(target=self._animate_trade, args=(offer_led, request_led)).start() 