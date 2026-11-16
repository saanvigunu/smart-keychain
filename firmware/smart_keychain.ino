// smart_keychain.ino - Smart Keychain firmware entry point (ESP32-C3, Arduino core).
//
// Loop: animate the face on the OLED, glow the edge strip, poll buttons.
// A short press on INTERACT pings the phone over BLE for an AI message;
// DISMISS goes back to the idle face.

#include <Arduino.h>
#include "include/pins.h"
#include "src/display.h"
#include "src/leds.h"
#include "src/ble_link.h"
#include "src/faces.h"

static Mood mood = MOOD_HAPPY;
static uint32_t last_blink = 0;

void setup() {
    display_begin();
    leds_begin();
    ble_begin("Smart Keychain");
    display_face(FACE_HAPPY);
    leds_idle_glow();
}

void loop() {
    // idle animation: blink every few seconds
    uint32_t now = millis();
    if (now - last_blink > 3800) {
        display_face(FACE_BLINK);
        delay(140);
        display_face(face_for_mood(mood));
        last_blink = now;
    }

    if (button_pressed(PIN_BTN_INTERACT)) {
        mood = MOOD_WOW;
        display_face(FACE_WOW);
        leds_thinking();              // swirl while the phone thinks
        ble_request_message();        // phone runs the AI, replies over BLE
    }
    if (button_pressed(PIN_BTN_DISMISS)) {
        mood = MOOD_HAPPY;
        display_face(FACE_HAPPY);
        leds_idle_glow();
    }

    // AI reply from the phone: show it, then settle back
    char msg[128];
    if (ble_poll_message(msg, sizeof(msg))) {
        display_scroll_text(msg);
        mood = MOOD_HAPPY;
        display_face(FACE_HAPPY);
        leds_idle_glow();
    }

    delay(20);
}

static bool button_pressed(int pin) {
    // buttons are active-low with internal pullups; naive debounce
    if (digitalRead(pin) == LOW) {
        delay(30);
        return digitalRead(pin) == LOW;
    }
    return false;
}
