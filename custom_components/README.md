# System Overview – Home Assistant

**System Overview** is a custom integration for Home Assistant that restores and extends
system-level information previously available under **Supervisor → System → Info**,
which was removed in later Home Assistant releases.

The integration provides structured and reliable visibility into the Home Assistant
runtime environment and is primarily intended for advanced users and system operators.

---

## Features

- Sensors for:
  - Home Assistant Core
  - Supervisor
  - Host system
- CPU, memory, and disk usage metrics
- Version and update availability information
- UI-based setup via Config Flow
- Diagnostics support for troubleshooting
- Built using `DataUpdateCoordinator`

---

## Installation

### HACS (recommended)

1. Open **HACS → Integrations**
2. Add this repository as a **Custom repository**
3. Search for **System Overview**
4. Install and restart Home Assistant

---

### Manual installation

1. Copy the directory:

custom_components/system_overview

to:


/config/custom_components/system_overview

2. Restart Home Assistant

---

## Configuration

After installation:

1. Go to **Settings → Devices & Services**
2. Click **Add integration**
3. Search for **System Overview**
4. Complete the setup dialog

No YAML configuration is required.

---

## Development notes

This integration focuses purely on system-level observability.
The exposed sensors and diagnostics may change as Home Assistant
internal APIs evolve.

The integration is developed and tested primarily on
**Home Assistant Supervised** installations.

---

## License

MIT License