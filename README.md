# System Overview

System Overview is a Home Assistant custom integration that provides
centralized visibility into Home Assistant Core, Supervisor, and Host
system information.

The integration also includes a flexible system log viewer with a
selectable log source.

---

## Features

- Home Assistant Core information (version, updates, CPU, memory)
- Supervisor information (version, channel, updates, CPU, memory)
- Host information (OS, hostname, IP address, disk usage, Docker version)
- Restart buttons for Core, Supervisor, and Host
- Integrated system log viewer with selectable log source

---

## Log viewer

The integration exposes two entities:

- `sensor.system_overview_logs`  
  Contains the current log output.

- `select.system_overview_log_provider`  
  Select which log source to display:
  - supervisor
  - core
  - host
  - dns
  - audio
  - multicast

Changing the select option updates the log output immediately.

---

## Dashboard preview 

[System Overview dashboard](docs/images/dashboard.png)

---

## Full dashboards

Complete dashboard configurations are provided as separate files:

- **Basic dashboard (no custom cards)**  
  `docs/dashboard-basic.yaml`

- **Advanced dashboard (optional custom cards)**  
  `docs/dashboard-advanced.yaml`

The advanced dashboard includes Core, Supervisor, and Host information,
restart buttons, and enhanced visual presentation.

---

## Optional custom cards

The advanced dashboard uses optional custom Lovelace cards such as:

- `entity-progress-card`

These cards are **not required** for the integration itself.

---

## Installation

Install using HACS:

1. Open HACS
2. Add this repository as a custom integration
3. Install **System Overview**
4. Restart Home Assistant
5. Add the integration via **Settings → Devices & Services**

---

## Support

If you encounter issues or have feature requests, please open an issue
in the GitHub repository.

---

© System Overview
