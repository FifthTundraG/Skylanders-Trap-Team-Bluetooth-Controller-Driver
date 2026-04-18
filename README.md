# Skylanders Trap Team Bluetooth Controller Driver for PC

This driver allows you to use the wireless Bluetooth controller as a **Xbox 360 Gamepad** on pc.



## Features
* **Full Mapping:** Supports Analog Sticks, D-Pad, ABXY buttons, Bumpers (L1/R1), and Triggers (L2/R2).
* **Xbox 360 Emulation:** Powered by ViGEmBus, making it compatible with Steam, Epic Games, and most emulators.


## Requirements
1. **Windows 10/11** with Bluetooth support.
2. **[ViGEmBus Driver](https://github.com/ViGEm/ViGEmBus/releases)** (Must be installed for the emulation to work).

## How to Install
1. **Download:** Go to the [Releases](https://github.com/ALYX5715/Skylanders-Trap-Team-Bluetooth-Controller-Driver/releases/tag/1.0.0) section and download  `controller.exe`.
2. **Run:** Launch the application and then turn on the GamePad. You will hear the Windows "device connected" sound.
3. **Test:** Visit [Gamepad Tester](https://gamepad-tester.com/) to verify all inputs.

## Technical Details (Data Mapping)
The controller sends 20-byte Bluetooth LE packets. This driver decodes it as follows:
* **Byte 0:** Header, it's always set as 0x53 wich in the ASCII table wich translates as the S from Skylanders.
* **Byte 1:** It's used as a "packet counter" each packet sent increases the value to verify packet losses or duplicates.
* **Byte 2:** Used as pairing mode status.
* **Byte 3:** Battery level
* **Byte 4-7:** I think it's used as "Padding" or Firmware Updates
* **Byte 8:** D-Pad (bits 0x01-0x08) and ABXY (bits 0x10-0x80).
* **Byte 9:** L1 (0x10), R1 (0x20), Home/Guide (0x04).
* **Byte 10** Left Trigger.
* **Byte 11** Right Trigger.
* **Byte 12** Right Stick X axis.
* **Byte 13** Right Stick Y axis.
* **Byte 14** Left Stick X axis.
* **Byte 15** Left Stick Y axis.
* **Byte 16** another counter 
* **Byte 17-19** as another padding set always to 0

## License
This project is licensed under the **MIT License**. See the `LICENSE` file for details.

## Credits
Developed by [ALYX5715](https://github.com/ALYX5715).
