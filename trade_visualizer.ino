#include <FastLED.h>

#define RED_LED_PIN 11
#define GREEN_LED_PIN 10
#define NUM_LEDS 60 // Adjust based on your LED strip length

CRGB redLeds[NUM_LEDS];
CRGB greenLeds[NUM_LEDS];

void setup()
{
    FastLED.addLeds<NEOPIXEL, RED_LED_PIN>(redLeds, NUM_LEDS);
    FastLED.addLeds<NEOPIXEL, GREEN_LED_PIN>(greenLeds, NUM_LEDS);
    Serial.begin(9600);

    // Clear all LEDs
    FastLED.clear();
    FastLED.show();
}

void loop()
{
    if (Serial.available())
    {
        String command = Serial.readStringUntil('\n');

        if (command.startsWith("TRADE:"))
        {
            // Parse LED positions
            int colonPos = command.indexOf(':');
            int commaPos = command.indexOf(',');

            int offerLed = command.substring(colonPos + 1, commaPos).toInt();
            int requestLed = command.substring(commaPos + 1).toInt();

            // Animate trade
            animateTrade(offerLed, requestLed);
        }
    }
}

void animateTrade(int offerLed, int requestLed)
{
    // Red trail animation (offering company)
    for (int i = 0; i <= offerLed; i++)
    {
        // Create trailing effect
        for (int j = 0; j < 5; j++)
        {
            if (i - j >= 0)
            {
                redLeds[i - j] = CRGB(255 >> j, 0, 0); // Diminishing red trail
            }
        }
        FastLED.show();
        delay(50);
    }

    // Clear red LEDs
    for (int i = 0; i < NUM_LEDS; i++)
    {
        redLeds[i] = CRGB::Black;
    }
    FastLED.show();

    // Green trail animation (requesting company)
    for (int i = 0; i <= requestLed; i++)
    {
        // Create trailing effect
        for (int j = 0; j < 5; j++)
        {
            if (i - j >= 0)
            {
                greenLeds[i - j] = CRGB(0, 255 >> j, 0); // Diminishing green trail
            }
        }
        FastLED.show();
        delay(50);
    }

    // Clear green LEDs
    for (int i = 0; i < NUM_LEDS; i++)
    {
        greenLeds[i] = CRGB::Black;
    }
    FastLED.show();
}