// ble_link.h - BLE UART link between the keychain and the phone.
//
// The keychain never runs AI itself: INTERACT sends a request, the
// companion app on the phone calls the AI API and writes the reply back.

#pragma once
#include <stdint.h>

void ble_begin(const char* device_name);
void ble_request_message();                  // ask the phone for an AI message
bool ble_poll_message(char* out, uint16_t max_len);  // true when a reply arrived
