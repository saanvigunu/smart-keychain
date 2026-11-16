// display.h - SSD1306 OLED rendering for Smart Keychain.

#pragma once
#include <stdint.h>
#include "faces.h"

void display_begin();
void display_face(const uint8_t* face);
void display_scroll_text(const char* msg);   // AI messages, marquee style
void display_battery(uint8_t pct);
