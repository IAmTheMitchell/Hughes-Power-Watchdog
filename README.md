# Hughes Power Watchdog

[![hacs_badge](https://img.shields.io/badge/HACS-Custom-orange.svg)](https://github.com/hacs/integration)
[![GitHub Release](https://img.shields.io/github/v/release/john-k-mcdowell/My-Hughes-Power-Watchdog?include_prereleases)](https://github.com/john-k-mcdowell/My-Hughes-Power-Watchdog/releases)
[![License](https://img.shields.io/github/license/john-k-mcdowell/My-Hughes-Power-Watchdog)](LICENSE)

A Home Assistant custom integration for **Hughes Power Watchdog Surge Protectors** with Bluetooth connectivity. 

DOES NOT WORK WITH WiFi DEVICES.  

Adding this support is on the roadmap but will require assistance from users who have WiFi versions to help reverse engineer the protocols.

> **100% Local Control** - This integration communicates directly with the Power Watchdog over Bluetooth Low Energy (BLE). No cloud services, no internet connection required, no data leaves your home.

## Tested Models

| Model      | Protocol | Known Issues |
| ---------- | -------- | ------------ |
| PWD50-EPD  | Legacy   | None         |
| PWD-VM-30A | Legacy   | None         |
| PWD30EPOW  | V5       | None         |

Please let me know via [GitHub issues](https://github.com/john-k-mcdowell/My-Hughes-Power-Watchdog/issues) if you have tested on other models so they can be included in the README.

This integration allows you to monitor your RV's power directly in Home Assistant without needing a special configuration on an ESP32 device. It connects directly to your Hughes Power Watchdog via Bluetooth or ESP-32 Bluetooth Proxy.

Based on the ESPHome implementation by spbrogan, tango2590, and makifoxgirl.

## Features

### Supported Models
- Hughes Power Watchdog (PWD) - any model with Bluetooth
- Hughes Power Watch (PWS) - any model with Bluetooth (not tested yet)
- Hughes Power Watchdog V5 (WD_V5_*) - Supported (v0.5.0+)

### Available Sensors
- **Line 1 Voltage** (volts)
- **Line 1 Current** (amps)
- **Line 1 Power** (watts)
- **Cumulative Power Usage** (kWh)
- **Error Code** (number)
- **Error Description** (text)

**50 Amp Units Only:**
- **Line 2 Voltage** (volts)
- **Line 2 Current** (amps)
- **Line 2 Power** (watts)
- **Total Combined Power** (L1 + L2, watts)

### Controls (Future Development)
- ** Not Fully Tested yet - Monitoring Switch - Enable/disable BLE connection to allow other apps to connect.  Switch turns monitoring on and off, have not yet verified if this allows the WatchDog App to connect.
- ** Not Implemented yet - Reset Power Usage Total

## Installation

### HACS Installation (Recommended)

1. Open HACS in your Home Assistant instance
2. Click on "Integrations"
3. Click the three dots in the top right corner
4. Select "Custom repositories"
5. Add this repository URL: `https://github.com/john-k-mcdowell/My-Hughes-Power-Watchdog`
6. Select category: "Integration"
7. Click "Add"
8. Find "Hughes Power Watchdog" in the integration list
9. Click "Download"
10. Restart Home Assistant

### Manual Installation

1. Copy the `custom_components/hughes_power_watchdog` folder to your Home Assistant `custom_components` directory
2. Restart Home Assistant

## Configuration

### Automatic Discovery (Recommended)

1. Go to **Settings** → **Devices & Services**
2. Click **Add Integration**
3. Search for "Hughes Power Watchdog"
4. Follow the configuration prompts
5. The integration will automatically discover nearby Hughes devices
6. Select your device from the list

### Manual Configuration

If your device is not auto-discovered but is powered on and within Bluetooth range:

1. Follow the steps above - when no devices are found, you'll be prompted for manual entry
2. Enter the MAC address of your Hughes device (found in the Hughes mobile app or your Bluetooth settings)
3. The integration will validate that the device is advertising and configure it

> **Important:** If you successfully configure your device using manual MAC entry, please [open a GitHub issue](https://github.com/john-k-mcdowell/My-Hughes-Power-Watchdog/issues) and include your device model name. This helps us add it to the auto-discovery list for future users.

## V5 Protocol Support

Starting with v0.5.0, this integration supports the newer V5 devices (device names starting with `WD_V5_`, such as PWD30EPOW). These devices use a different Bluetooth protocol than the legacy PMD/PWS models.

**V5 Status:**
- ✅ Voltage, Current, Power readings - Working
- ✅ Energy (kWh) - Working
- ⚠️ Error codes - Not yet implemented
- ⚠️ Line 2 (50A dual-phase) - Not yet tested

**If you have a V5 device with issues**, please help us by:
1. Enabling debug logging (see below)
2. Checking if the readings match your Hughes mobile app
3. Reporting any issues via [GitHub issues](https://github.com/john-k-mcdowell/My-Hughes-Power-Watchdog/issues)

### Debug Logging

Add this to your `configuration.yaml` to enable debug logging:

```yaml
logger:
  default: info
  logs:
    custom_components.hughes_power_watchdog: debug
```

Then check your Home Assistant logs for entries prefixed with `[modern_V5]` or `[Legacy]`.

## Requirements

- Home Assistant 2023.1.0 or newer
- Bluetooth adapter/proxy in range of your Hughes Power Watchdog
- Hughes Power Watchdog with Bluetooth (PMD, PWS, or WD_V5 model)

## Troubleshooting

### Device Not Found
- Ensure no other devices are connected to your Hughes Power Watchdog (it only supports one connection at a time)
- Make sure Bluetooth is enabled on your Home Assistant host
- Verify your Hughes device is powered on and within Bluetooth range
- Try using the Hughes mobile app to confirm the device is functioning

### Connection Issues
- Disconnect any mobile apps connected to the Hughes device
- Toggle the Monitoring Switch off and on
- Restart the integration

## Credits

Based on the original ESPHome implementation by:
- [spbrogan](https://github.com/spbrogan)
- [makifoxgirl](https://github.com/makifoxgirl)
- [tango2590](https://github.com/tango2590/Hughes-Power-Watchdog)
- SergeantBort

## License

MIT License

## Support

For issues and feature requests, please use the [GitHub issue tracker](https://github.com/john-k-mcdowell/My-Hughes-Power-Watchdog/issues).
