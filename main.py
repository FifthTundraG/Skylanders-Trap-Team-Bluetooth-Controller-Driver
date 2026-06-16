import asyncio
import vgamepad as vg
from bleak import BleakClient, BleakScanner

CHARACTERISTIC_UUID = "533e1541-3abe-f33f-cd00-594e8b0a8ea3"
NAME_CONTROLLER = "Skylanders GamePad"

def scale_axis(value):
    if value > 127: val = value - 256
    else: val = value
    val = max(-127, min(127, val))
    if abs(val) < 12: return 0
    return int(val * 257)

def notification_handler(sender, data, gamepad):
    b = list(data)
    if len(b) < 16: return

    # DPAD (Byte 8)
    dpad = b[8] & 0x0F
    gamepad.release_button(vg.XUSB_BUTTON.XUSB_GAMEPAD_DPAD_UP)
    gamepad.release_button(vg.XUSB_BUTTON.XUSB_GAMEPAD_DPAD_DOWN)
    gamepad.release_button(vg.XUSB_BUTTON.XUSB_GAMEPAD_DPAD_LEFT)
    gamepad.release_button(vg.XUSB_BUTTON.XUSB_GAMEPAD_DPAD_RIGHT)
    if dpad == 0x01: gamepad.press_button(vg.XUSB_BUTTON.XUSB_GAMEPAD_DPAD_UP)
    elif dpad == 0x02: gamepad.press_button(vg.XUSB_BUTTON.XUSB_GAMEPAD_DPAD_DOWN)
    elif dpad == 0x04: gamepad.press_button(vg.XUSB_BUTTON.XUSB_GAMEPAD_DPAD_LEFT)
    elif dpad == 0x08: gamepad.press_button(vg.XUSB_BUTTON.XUSB_GAMEPAD_DPAD_RIGHT)

    # ABXY (Byte 8)
    if b[8] & 0x10: gamepad.press_button(vg.XUSB_BUTTON.XUSB_GAMEPAD_A)
    else: gamepad.release_button(vg.XUSB_BUTTON.XUSB_GAMEPAD_A)
    if b[8] & 0x20: gamepad.press_button(vg.XUSB_BUTTON.XUSB_GAMEPAD_B)
    else: gamepad.release_button(vg.XUSB_BUTTON.XUSB_GAMEPAD_B)
    if b[8] & 0x40: gamepad.press_button(vg.XUSB_BUTTON.XUSB_GAMEPAD_X)
    else: gamepad.release_button(vg.XUSB_BUTTON.XUSB_GAMEPAD_X)
    if b[8] & 0x80: gamepad.press_button(vg.XUSB_BUTTON.XUSB_GAMEPAD_Y)
    else: gamepad.release_button(vg.XUSB_BUTTON.XUSB_GAMEPAD_Y)

    # DORSI & HOME (Byte 9)
    if b[9] & 0x10: gamepad.press_button(vg.XUSB_BUTTON.XUSB_GAMEPAD_LEFT_SHOULDER)
    else: gamepad.release_button(vg.XUSB_BUTTON.XUSB_GAMEPAD_LEFT_SHOULDER)
    if b[9] & 0x20: gamepad.press_button(vg.XUSB_BUTTON.XUSB_GAMEPAD_RIGHT_SHOULDER)
    else: gamepad.release_button(vg.XUSB_BUTTON.XUSB_GAMEPAD_RIGHT_SHOULDER)
    if b[9] & 0x04: gamepad.press_button(vg.XUSB_BUTTON.XUSB_GAMEPAD_GUIDE)
    else: gamepad.release_button(vg.XUSB_BUTTON.XUSB_GAMEPAD_GUIDE)

    # TRIGGER (Byte 10-11)
    gamepad.left_trigger(255 if b[10] == 0xFF else 0)
    gamepad.right_trigger(255 if b[11] == 0xFF else 0)

    # Sticks (Byte 12-15)
    gamepad.right_joystick(scale_axis(b[12]), scale_axis(b[13]))
    gamepad.left_joystick(scale_axis(b[14]), scale_axis(b[15]))

    gamepad.update()

async def run_driver():
    print(f"Driver avviato. Ricerca di: {NAME_CONTROLLER}...")
    while True:
        try:
            device = await BleakScanner.find_device_by_name(NAME_CONTROLLER)
            if device:
                print("Controller Found! Activating ViGEmBus...")
                virtual_pad = vg.VX360Gamepad() 
                
                async with BleakClient(device) as client:
                    print(f"Connected to {NAME_CONTROLLER}. Have fun")
                    await client.start_notify(
                        CHARACTERISTIC_UUID, 
                        lambda s, d: notification_handler(s, d, virtual_pad)
                    )
                    
                    while client.is_connected:
                        await asyncio.sleep(1)
                
                print("Lost connection with the controller. Removing virtual gamepad.")
                del virtual_pad
            else:
                await asyncio.sleep(5)
        except Exception as e:
            print(f"Error: {e}. Trying again in 5 seconds...")
            await asyncio.sleep(5)

if __name__ == "__main__":
    try:
        asyncio.run(run_driver())
    except KeyboardInterrupt:
        pass