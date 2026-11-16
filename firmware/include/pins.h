// pins.h - Smart Keychain pin map
//
// LEFT BLANK ON PURPOSE.
// Pin values get filled in once the EE side finishes the PCB layout in
// KiCad - assigning GPIOs before the board is routed just means redoing
// them. Everything else in the firmware #includes this file and uses the
// names below, so the day the board is real, this is the only file that
// changes.
//
// Component list (from the design doc):
//   ESP32-C3            - main processor
//   SSD1306 OLED 128x64 - I2C display (faces + messages)
//   WS2812B strip       - edge glow
//   2 tactile buttons   - interact / dismiss
//   buzzer              - sounds
//   protected 3.7V LiPo + charging circuit

#pragma once

// --- OLED display (I2C) ---
#define PIN_OLED_SDA        // TODO(EE): SDA GPIO
#define PIN_OLED_SCL        // TODO(EE): SCL GPIO

// --- WS2812B edge glow ---
#define PIN_LED_STRIP       // TODO(EE): data GPIO
#define LED_STRIP_COUNT     // TODO(EE): how many pixels fit the enclosure edge

// --- buttons (active-low, internal pullups) ---
#define PIN_BTN_INTERACT    // TODO(EE)
#define PIN_BTN_DISMISS     // TODO(EE)

// --- buzzer ---
#define PIN_BUZZER          // TODO(EE)

// --- battery sense (ADC divider) ---
#define PIN_BATTERY_ADC     // TODO(EE)
