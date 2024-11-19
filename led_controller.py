import time
from threading import Thread
from typing import Dict
from models import Trade, Company
import serial

class MockLEDStrip:
    def __init__(self, num_leds):
        self.num_leds = num_leds
        self.leds = [(0,0,0)] * num_leds
    
    def write(self):
        # In development, just print the LED states
        print("LED States:", self.leds)
    
    def reset(self):
        self.leds = [(0,0,0)] * self.num_leds
    
    def __setitem__(self, key, value):
        self.leds[key] = value

class LEDController:
    def __init__(self, is_dev_mode=True):
        self.is_dev_mode = is_dev_mode
        self.company_to_led_map: Dict[str, int] = {}
        self.current_led = 0
        self.num_leds = 0
        self.leds = None
        
        if not is_dev_mode:
            try:
                import board
                self.pin_clk = board.D13
                self.pin_data = board.D10
                self.serial = serial.Serial('/dev/ttyACM0', 9600)  # Adjust port as needed
                time.sleep(2)  # Wait for Arduino to reset
          
            except ImportError:
                print("Warning: Running in production mode but hardware libraries not found")
                self.is_dev_mode = True
        
    def assign_company_leds(self, companies: Dict[str, Company]):
        """Assign each company to a pair of LEDs"""
        self.num_leds = len(companies) * 2  # Each company gets 2 LEDs
        
        if self.is_dev_mode:
            self.leds = MockLEDStrip(self.num_leds)
        else:
            # import micropython-p9813
            # self.leds = p9813.P9813(self.pin_clk, self.pin_data, self.num_leds)
            console.log("goofed")
        
        self.leds.reset()
        
        # Assign LED pairs to companies
        for company_name in companies:
            self.company_to_led_map[company_name] = self.current_led
            self.current_led += 2
            
    def _animate_trade(self, offer_led: int, request_led: int):
        """Create trail effect for a trade"""
        if self.is_dev_mode:
            print(f"Animating trade: Offer LED {offer_led} -> Request LED {request_led}")
            return
            
        # Offer company animation (red trail towards pi)
        # for intensity in range(255, 0, -5):
        #     self.leds[offer_led] = (intensity, 0, 0)
        #     self.leds.write()
        #     time.sleep(0.01)
            
        # # Request company animation (green trail from pi)
        # for intensity in range(0, 255, 5):
        #     self.leds[request_led] = (0, intensity, 0)
        #     self.leds.write()
        #     time.sleep(0.01)
            
        # # Reset LEDs
        # self.leds[offer_led] = (0, 0, 0)
        # self.leds[request_led] = (0, 0, 0)
        # self.leds.write()
        try:
            # Send trade animation command to Arduino
            command = f"TRADE:{offer_led},{request_led}\n"
            self.serial.write(command.encode())
        except Exception as e:
            print(f"Error sending command to Arduino: {e}")


    def visualize_trade(self, offer: Trade, request: Trade):
        """Trigger LED animation for a trade in a non-blocking way"""
        if not self.leds:
            print("Warning: LED controller not initialized with companies yet")
            return
            
        offer_led = self.company_to_led_map[offer.requester_company]
        request_led = self.company_to_led_map[request.requester_company] + 1
        
        # Run animation in a separate thread to not block the main process
        Thread(target=self._animate_trade, args=(offer_led, request_led)).start()