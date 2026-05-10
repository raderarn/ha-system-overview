# System Overview

System Overview is a Home Assistant custom integration that provides
a centralized overview of Home Assistant Core, Supervisor, and Host
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

## Log Viewer

The integration provides two entities:

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

## Dashboard examples

### Minimal example (no custom cards)

This example works on a completely default Home Assistant installation
and does **not** require any custom Lovelace cards.

<details>
<summary><strong>Click to view example</strong></summary>

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