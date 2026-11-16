// leds.h - WS2812B edge glow effects.

#pragma once
#include <stdint.h>

void leds_begin();
void leds_idle_glow();      // soft warm breathing glow
void leds_thinking();       // swirl while the AI answers
void leds_notify();         // quick flash for phone notifications
void leds_off();
