# Smart Keychain

A pixel AI companion keychain: a tiny OLED face that blinks and reacts,
edge glow, buttons, and AI replies delivered over Bluetooth from your
a development laptop. Custom PCB and enclosure are planned, not built.

A CS x EE passion project by Saanvi and Olivia.

## the idea

A keychain-sized digital companion:

- 0.96" SSD1306 OLED (128x64) shows animated pixel faces and short messages
- WS2812B edge glow for idle / thinking / notification moods
- two buttons: interact (ask the AI) and dismiss
- the ESP32-C3 never runs AI itself - press interact, the phone gets a BLE
  ping, the companion app calls an AI API, and the reply scrolls across
  the tiny screen
- custom PCB (KiCad) and enclosure, built to be manufacturable - maybe
  even sellable

## repo layout

```
firmware/            Arduino/ESP32-C3 firmware (the EE+CS handshake layer)
  smart_keychain.ino       main loop: face animation, buttons, BLE
  include/pins.h     THE PIN MAP - intentionally blank until the PCB is routed
  src/               display, leds, ble link, pixel faces
companion/           Python development companion (CS side)
  personality.py     Smart Keychain's character + AI call
  bridge.py          BLE bridge: keychain requests -> AI replies
tests/               companion app tests
```

## who builds what

**CS (Saanvi):** the companion app, AI personality and prompts, pixel
animations, BLE protocol, backend.

**EE (Olivia):** the circuit, the custom PCB in KiCad, power (protected
LiPo + charging), the enclosure, assembly.

## status

Firmware skeleton + prototype companion code are in. The display, LED and BLE
headers are declarations only: their implementations are still TODO. This is
not flash-ready firmware and has not been tested on hardware. The Python bridge
is for a BLE-capable laptop; a native phone app is not included. The eight unit
tests use a mocked AI client and do not test live BLE or an AI service. `firmware/include/pins.h` is
deliberately empty - pin values get assigned once the PCB layout is
final, and every other file reads through that one header.

## roadmap

1. [x] firmware scaffold + mocked companion unit tests
2. [ ] display a pixel face on real hardware
3. [ ] animated expressions (blink, wow, sleep)
4. [ ] edge glow + buttons on the board
5. [ ] BLE link phone <-> keychain
6. [ ] AI replies on the screen
7. [ ] custom PCB in KiCad -> assign the pins
8. [ ] enclosure, assembly, final test

## dev

```bash
# development companion (BLE-capable laptop)
pip install bleak anthropic
export ANTHROPIC_API_KEY=...
python3 -m companion.bridge

# tests
python3 -m unittest discover -s tests -v

# firmware: open firmware/smart_keychain.ino in the Arduino IDE
# NOT READY TO FLASH: implement display/LED/BLE drivers, then assign pins
# Arduino requires a sketch folder matching the .ino filename.
```
