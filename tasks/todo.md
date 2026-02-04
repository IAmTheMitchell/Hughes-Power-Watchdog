# Todo: Add WD_V5 Protocol Support

## Background
Reverse engineering completed for new WD_V5 device (device name: `WD_V5_9e9e6e20b9ed`).
This device uses a completely different BLE protocol than the existing PMD/PWS devices.

See [WD_V5_PROTOCOL.md](../bt_logs/WD_V5_PROTOCOL.md) for full protocol documentation.

## Key Protocol Differences

| Feature | PMD/PWS (Old) | WD_V5 (New) |
|---------|---------------|-------------|
| Service UUID | `0000ffe0-...` | `000000ff-...` |
| Characteristic | `0000ffe2-...` (TX) / `0000fff5-...` (RX) | `0000ff01-...` (bidirectional) |
| Packet Header | `01 03 20` | `$yw@` (0x24797740) |
| Initialization | None | `!%!%,protocol,open,` |
| Data Format | 2x20 byte chunks | Single 45-byte packet |

## Plan

### Phase 1: Discovery & Config
- [x] Add `WD_V5*` pattern to manifest.json bluetooth discovery
- [x] Update const.py with WD_V5 UUIDs and constants
- [x] Update config_flow.py to recognize WD_V5 devices

### Phase 2: Protocol Implementation
- [x] Create WD_V5 protocol handler (or modify coordinator to detect protocol version)
- [x] Implement initialization sequence (`!%!%,protocol,open,`)
- [x] Implement WD_V5 packet parsing
- [x] Handle both protocols based on device name
- [x] Add comprehensive debug logging for troubleshooting:
  - Log raw packet hex data on receive
  - Log parsed values with field positions
  - Log connection state changes
  - Log initialization command send/response
  - Log any packet parsing errors with full context

### Phase 3: Testing & Refinement
- [x] Test with actual WD_V5 device
- [x] Verify voltage/current/power readings match app
- [x] Investigate unknown fields (energy, frequency, error codes)
  - Energy (kWh) decoded from bytes 21-24 in v0.5.0-beta.2
  - Frequency and error codes still TBD
- [x] Update sensors for WD_V5 (single line only, possibly different available sensors)
  - Line 2 entities now skipped for V5 devices (v0.5.0-beta.3)

### Phase 4: Documentation
- [x] Update README with WD_V5 support info
- [ ] Update how-it-works.md (deferred - excluded from git)
- [x] Increment version number to 0.5.0-beta.1

## Technical Details

### New Constants Needed (const.py)
```python
# WD_V5 Protocol
WD_V5_SERVICE_UUID = "000000ff-0000-1000-8000-00805f9b34fb"
WD_V5_CHARACTERISTIC_UUID = "0000ff01-0000-1000-8000-00805f9b34fb"
WD_V5_HEADER = b"$yw@"  # 0x24797740
WD_V5_END_MARKER = b"q!"  # 0x7121
WD_V5_INIT_COMMAND = b"!%!%,protocol,open,"
```

### Packet Structure
```
Offset 9-12:  Voltage (BE int32 / 10000)
Offset 13-16: Current (BE int32 / 10000)
Offset 17-20: Power (BE int32 / 10000)
```

## Debug Logging Strategy

When testing with actual device, user should enable debug logging in Home Assistant:

```yaml
logger:
  default: info
  logs:
    custom_components.hughes_power_watchdog: debug
```

Key debug output to capture:
- `[WD_V5] Connected to {address}` - Connection established
- `[WD_V5] Sending init command: {hex}` - Initialization
- `[WD_V5] Raw notification ({len} bytes): {hex}` - Every packet received
- `[WD_V5] Parsed: V={voltage}V I={current}A P={power}W` - Successful parse
- `[WD_V5] Unknown packet type 0x{type}: {hex}` - Unrecognized packets
- `[WD_V5] Parse error at offset {n}: {error}` - Parsing failures

This will allow remote troubleshooting without physical access to the device.

## Changes Summary (v0.5.0-beta.4)

### Files Modified

**const.py**
- Added Line 2 byte position constants for V5 protocol (speculative):
  - `WD_V5_BYTE_L2_VOLTAGE_START/END`, `WD_V5_BYTE_L2_CURRENT_START/END`, `WD_V5_BYTE_L2_POWER_START/END`
  - `WD_V5_MIN_L2_PACKET_SIZE = 37`
- Added voltage validation range: `WD_V5_VOLTAGE_MIN = 90.0`, `WD_V5_VOLTAGE_MAX = 145.0`

**coordinator.py**
- Updated `_parse_data_packet_v5()` to try decoding Line 2 from bytes 25-36
- Only populates `_line_2_data` if decoded voltage is in valid range (90-145V)
- Logs whether device is detected as single-phase or dual-phase

**sensor.py**
- Reverted to create all entities for all devices
- Line 2 sensors will show unavailable for single-phase devices

**manifest.json** / **version.py**
- Updated version to 0.5.0-beta.4

### Approach
- All entities created for all devices
- V5 devices auto-detect single vs dual-phase from packet data
- Single-phase devices: Line 2 sensors show unavailable
- Dual-phase devices: Line 2 sensors populate if voltage in valid range

---

## Changes Summary (v0.5.0-beta.3) [Superseded by beta.4]

### Files Modified

**coordinator.py**
- Added `is_v5_protocol` public property to expose protocol type

**sensor.py**
- Line 2 sensors (Voltage, Current, Power, Combined) now only created for legacy devices
- WD_V5 devices get only Line 1 sensors, Energy, and Error sensors

**manifest.json** / **version.py**
- Updated version to 0.5.0-beta.3

### Improvement
- WD_V5 users no longer see confusing "Unknown" Line 2 entities

---

## Changes Summary (v0.5.0-beta.2)

### Files Modified

**const.py**
- Added energy byte position constants:
  - `WD_V5_BYTE_ENERGY_START = 21`
  - `WD_V5_BYTE_ENERGY_END = 25`
  - `WD_V5_MIN_ENERGY_PACKET_SIZE = 25`

**coordinator.py**
- Added imports for new energy constants
- Updated `_parse_data_packet_v5()` to decode energy from bytes 21-24
- Added debug logging for energy raw/decoded values
- Updated info log message to include energy
- Changed line 1 data `"energy"` from hardcoded 0 to decoded value

**manifest.json** / **version.py**
- Updated version to 0.5.0-beta.2

### Bug Fixed
- Cumulative Power Usage (kWh) now correctly shows energy reading for WD_V5 devices

---

## Changes Summary (v0.5.0-beta.1)

### Files Modified

**manifest.json**
- Added `WD_V5*` to bluetooth discovery patterns
- Version updated to 0.5.0-beta.1

**const.py**
- Added device name prefix lists: `DEVICE_NAME_PREFIXES_LEGACY`, `DEVICE_NAME_PREFIXES_V5`
- Added WD_V5 protocol constants:
  - `WD_V5_SERVICE_UUID`, `WD_V5_CHARACTERISTIC_UUID`
  - `WD_V5_HEADER`, `WD_V5_END_MARKER`, `WD_V5_INIT_COMMAND`
  - `WD_V5_MSG_TYPE_DATA`, `WD_V5_MSG_TYPE_STATUS`, `WD_V5_MSG_TYPE_CONTROL`
  - Byte position constants for V5 packet parsing

**coordinator.py**
- Added `_detect_v5_protocol()` static method for protocol detection
- Added `_is_v5_protocol` and `_v5_initialized` instance attributes
- Split `_request_device_status()` into protocol-specific methods:
  - `_request_device_status_legacy()` for PMD/PWS/PMS
  - `_request_device_status_v5()` for WD_V5 (includes init command)
- Split notification handlers:
  - `_notification_handler_legacy()` for legacy protocol
  - `_notification_handler_v5()` for V5 protocol
- Split packet parsers:
  - `_parse_data_packet_legacy()` for legacy 40-byte packets
  - `_parse_data_packet_v5()` for V5 variable-length packets
- Updated `device_info` property to show "Power Watchdog V5" for V5 devices
- Added comprehensive debug logging with `[Legacy]` and `[WD_V5]` prefixes
- Reset `_v5_initialized` flag on disconnect for proper reinit

**version.py**
- Updated to 0.5.0-beta.1

**README.md**
- Added WD_V5 to tested models table (as experimental)
- Added WD_V5 to supported models list
- Added "WD_V5 Support (Experimental)" section with:
  - Status of supported features
  - Debug logging instructions
  - Call for testers

### Not Yet Implemented for WD_V5
- Energy (kWh) sensor - field not yet decoded
- Frequency sensor - field identified but not implemented
- Error codes - field identified but mapping unknown
- Line 2 support - WD_V5 appears to be 30A single-line only
