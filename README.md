# System Overview

System Overview is a Home Assistant custom integration that provides a
centralized view of Home Assistant Core, Supervisor, and Host system
information.

The integration also includes a flexible log viewer that allows you to
switch between different system log sources directly from the dashboard.

## Features

- Home Assistant Core information (version, updates, CPU, memory)
- Supervisor information (version, channel, updates, CPU, memory)
- Host information (OS, hostname, IP address, disk usage, Docker version)
- Restart buttons for Core, Supervisor, and Host
- Integrated system log viewer with selectable log source

## Log viewer

The integration exposes a log sensor and a select entity:

- `sensor.system_overview_logs`  
  Holds the current log output.

- `select.system_overview_log_provider`  
  Select which log source to display:
  - supervisor
  - core
  - host
  - dns
  - audio
  - multicast

Changing the select option immediately updates the log output.

## Dashboard examples

### Basic example (no custom cards)

This example works on a completely default Home Assistant installation
and does **not require any custom Lovelace cards**.

```yaml
type: vertical-stack
cards:
  - type: entities
    title: System logs
    entities:
      - select.system_overview_log_provider

  - type: markdown
    entity_id:
      - sensor.system_overview_logs
      - select.system_overview_log_provider
    content: >
      {% set provider = states('select.system_overview_log_provider') %}
      {% set t = state_attr('sensor.system_overview_logs', 'text') %}
      **Source:** {{ provider }}

      ```text
      {{ t if t else 'No log data' }}
      ```

Advanced dashboard
A complete system dashboard including Core, Supervisor, Host information,
restart buttons, and a log viewer is available in:
docs/dashboard-advanced.yaml

This advanced example uses optional custom Lovelace cards such as:

entity-progress-card

These cards are not required for the integration itself and are only
used to improve visual presentation.
Optional custom cards
If you choose to use the advanced dashboard, you may need:

entity-progress-card

These are optional and not installed automatically.
Screenshots
Screenshots of the advanced dashboard can be found in:
docs/images/

Installation
Install using HACS:

Open HACS
Add this repository as a custom integration
Install System Overview
Restart Home Assistant

After installation, add the integration via Settings → Devices & Services.