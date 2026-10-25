# System Overview

System Overview is a Home Assistant custom integration that provides
a centralized overview of Home Assistant Core, Supervisor, and Host
system information.

The integration also includes a flexible system log viewer with a
selectable log source.

---

## Features

- Home Assistant Core information (version, updates, CPU, memory)
- Supervisor information (version, channel, updates, data path, CPU, memory)
- Host information (OS, hostname, IP address, disk usage, Docker version)
- Restart buttons for Core and Host
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

### Full Dashboard Example

This example displays Core, Supervisor, and Host details side by side in a 3-column grid alongside the log viewer.

<details>
<summary><strong>Click to view example</strong></summary>

```yaml
type: vertical-stack
cards:
  - type: grid
    columns: 3
    square: false
    cards:
      # --- CORE ---
      - type: entities
        title: Core
        entities:
          - entity: sensor.system_overview_overview
            name: Version
            icon: mdi:eye-outline
          - entity: sensor.system_overview_core_latest
            name: Latest version
            icon: mdi:eye-outline
          - entity: sensor.system_overview_core_update_available
            name: Update available
            icon: mdi:eye-outline
          - entity: sensor.system_overview_core_cpu_percent
            name: Core CPU usage
            icon: mdi:eye-outline
          - entity: sensor.system_overview_core_memory_percent
            name: Core memory usage
            icon: mdi:eye-outline

      # --- SUPERVISOR ---
      - type: entities
        title: Supervisor
        entities:
          - entity: sensor.system_overview_supervisor_version
            name: Version
            icon: mdi:eye-outline
          - entity: sensor.system_overview_supervisor_latest
            name: Latest version
            icon: mdi:eye-outline
          - entity: sensor.system_overview_supervisor_channel
            name: Channel
            icon: mdi:eye-outline
          - entity: sensor.system_overview_installation_supported
            name: Installation supported
            icon: mdi:eye-outline
          - entity: sensor.system_overview_supervisor_update_available
            name: Update available
            icon: mdi:eye-outline
          - entity: sensor.system_overview_supervisor_data_path
            name: Data path
            icon: mdi:folder-outline
          - entity: sensor.system_overview_supervisor_cpu_percent
            name: Supervisor CPU usage
            icon: mdi:eye-outline
          - entity: sensor.system_overview_supervisor_memory_percent
            name: Supervisor memory usage
            icon: mdi:eye-outline

      # --- HOST ---
      - type: entities
        title: Host
        entities:
          - entity: sensor.system_overview_hostname
            name: Hostname
            icon: mdi:eye-outline
          - entity: sensor.system_overview_host_ip
            name: IP address
            icon: mdi:eye-outline
          - entity: sensor.system_overview_host_os
            name: Operating system
            icon: mdi:eye-outline
          - entity: sensor.system_overview_host_os_supervisor
            name: Host OS
            icon: mdi:eye-outline
          - entity: sensor.system_overview_docker_version
            name: Docker version
            icon: mdi:eye-outline
          - entity: sensor.system_overview_host_cpu
            name: CPU usage
            icon: mdi:eye-outline
          - entity: sensor.system_overview_host_mem
            name: Memory usage
            icon: mdi:eye-outline
          - entity: sensor.system_overview_host_disk
            name: Disk usage
            icon: mdi:eye-outline

  # --- LOGS ---
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
