"""BLE bridge: listen for the keychain's requests, answer with AI replies.

Development prototype for a BLE-capable laptop (not a native phone app):

    pip install bleak anthropic
    export ANTHROPIC_API_KEY=...
    python3 -m companion.bridge
"""

import asyncio

from bleak import BleakClient, BleakScanner

from .personality import generate_reply

SERVICE_UUID = "6e400001-b5a3-f393-e0a9-e50e24dcca9e"  # Nordic UART
RX_CHAR_UUID = "6e400002-b5a3-f393-e0a9-e50e24dcca9e"  # phone -> keychain
TX_CHAR_UUID = "6e400003-b5a3-f393-e0a9-e50e24dcca9e"  # keychain -> phone
DEVICE_NAME = "Smart Keychain"


async def run():
    print(f"scanning for {DEVICE_NAME}...")
    device = await BleakScanner.find_device_by_name(DEVICE_NAME, timeout=20)
    if device is None:
        print("keychain not found - is it powered on?")
        return

    queue = asyncio.Queue()

    def on_request(_, data: bytes):
        queue.put_nowait(data.decode().strip())

    async with BleakClient(device) as client:
        await client.start_notify(TX_CHAR_UUID, on_request)
        print("connected. waiting for button presses...")
        while True:
            signal = await queue.get()
            print(f"request: {signal}")
            try:
                reply = await asyncio.to_thread(generate_reply, signal)
            except Exception as e:  # offline, quota, whatever - stay in character
                print(f"ai call failed: {e}")
                reply = "my brain is offline, but i'm still cute"
            print(f"reply:   {reply}")
            await client.write_gatt_char(RX_CHAR_UUID, reply.encode())


if __name__ == "__main__":
    asyncio.run(run())
