#include <Adafruit_NeoPixel.h>

#define LED_PIN 6
#define NUM_LEDS 56
#define SERIAL_BAUD 115200

Adafruit_NeoPixel strip(NUM_LEDS, LED_PIN, NEO_GRB + NEO_KHZ800);

void setup() {
  Serial.begin(SERIAL_BAUD);
  strip.begin();
  strip.show();
}

void loop() {
  const int bytesPerLED = 3;
  const int totalBytes = NUM_LEDS * bytesPerLED;
  static uint8_t ledData[NUM_LEDS * bytesPerLED];
  static int bytesRead = 0;

  while (Serial.available() > 0 && bytesRead < totalBytes) {
    ledData[bytesRead++] = Serial.read();
  }

  if (bytesRead == totalBytes) {
    for (int i = 0; i < NUM_LEDS; i++) {
      int idx = i * bytesPerLED;
      uint8_t r = ledData[idx];
      uint8_t g = ledData[idx + 1];
      uint8_t b = ledData[idx + 2];

      strip.setPixelColor(i, strip.Color(r, g, b));
    }
    strip.show();
    bytesRead = 0; // Reset for the next frame
  }
}