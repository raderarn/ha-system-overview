from homeassistant.components.sensor import SensorEntity, SensorStateClass
from homeassistant.helpers.entity import EntityCategory
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import DOMAIN, NAME


def _get_nested(data, path):
    cur = data or {}
    for key in path:
        if not isinstance(cur, dict):
            return None
        cur = cur.get(key)
    return cur


class SystemOverviewBaseSensor(CoordinatorEntity, SensorEntity):
    _attr_entity_category = EntityCategory.DIAGNOSTIC

    def __init__(self, coordinator, key, name_suffix, path, unit, state_class, precision):
        super().__init__(coordinator)
        self._path = path
        self._attr_name = NAME + " " + name_suffix
        self._attr_unique_id = DOMAIN + "_" + key
        if unit is not None:
            self._attr_native_unit_of_measurement = unit
        if state_class is not None:
            self._attr_state_class = state_class
        if precision is not None:
            self._attr_suggested_display_precision = precision

    @property
    def device_info(self):
        data = self.coordinator.data or {}
        host = data.get("host") or {}
        core = data.get("core") or {}
        hostname = host.get("hostname")
        core_version = core.get("version")
        return {
            "identifiers": {(DOMAIN, "system")},
            "name": NAME,
            "manufacturer": "Home Assistant",
            "model": hostname or "system",
            "sw_version": core_version,
        }

    @property
    def native_value(self):
        return _get_nested(self.coordinator.data, self._path)


class SystemOverviewOverviewSensor(SystemOverviewBaseSensor):
    def __init__(self, coordinator):
        super().__init__(
            coordinator,
            "overview",
            "Core Version",
            ["core", "version"],
            None,
            None,
            None,
        )

    @property
    def extra_state_attributes(self):
        return self.coordinator.data or {}


async def async_setup_entry(hass, entry, async_add_entities):
    coordinator = entry.runtime_data

    entities = [
        SystemOverviewOverviewSensor(coordinator),

        SystemOverviewBaseSensor(
            coordinator, "core_latest", "Core Latest Version",
            ["supervisor", "core_info", "version_latest"], None, None, None
        ),
        SystemOverviewBaseSensor(
            coordinator, "core_update_available", "Core Update Available",
            ["supervisor", "core_info", "update_available"], None, None, None
        ),

        SystemOverviewBaseSensor(
            coordinator, "supervisor_version", "Supervisor Version",
            ["supervisor", "supervisor_info", "version"], None, None, None
        ),
        SystemOverviewBaseSensor(
            coordinator, "supervisor_latest", "Supervisor Latest Version",
            ["supervisor", "supervisor_info", "version_latest"], None, None, None
        ),
        SystemOverviewBaseSensor(
            coordinator, "supervisor_update_available", "Supervisor Update Available",
            ["supervisor", "supervisor_info", "update_available"], None, None, None
        ),
        SystemOverviewBaseSensor(
            coordinator, "supervisor_channel", "Supervisor Channel",
            ["supervisor", "supervisor_info", "channel"], None, None, None
        ),
        SystemOverviewBaseSensor(
            coordinator, "supervisor_supported", "Installation Supported",
            ["supervisor", "supervisor_info", "supported"], None, None, None
        ),

        SystemOverviewBaseSensor(
            coordinator, "core_cpu_percent", "Core CPU Percent",
            ["supervisor", "core_stats", "cpu_percent"], "%", SensorStateClass.MEASUREMENT, 2
        ),
        SystemOverviewBaseSensor(
            coordinator, "core_memory_percent", "Core Memory Percent",
            ["supervisor", "core_stats", "memory_percent"], "%", SensorStateClass.MEASUREMENT, 2
        ),
        SystemOverviewBaseSensor(
            coordinator, "supervisor_cpu_percent", "Supervisor CPU Percent",
            ["supervisor", "supervisor_stats", "cpu_percent"], "%", SensorStateClass.MEASUREMENT, 2
        ),
        SystemOverviewBaseSensor(
            coordinator, "supervisor_memory_percent", "Supervisor Memory Percent",
            ["supervisor", "supervisor_stats", "memory_percent"], "%", SensorStateClass.MEASUREMENT, 2
        ),
        SystemOverviewBaseSensor(
            coordinator, "hostname", "Hostname",
            ["host", "hostname"], None, None, None
        ),
        SystemOverviewBaseSensor(
            coordinator, "host_ip", "Host IP",
            ["host", "ip_address"], None, None, None
        ),
        SystemOverviewBaseSensor(
            coordinator, "host_os", "Host OS",
            ["host", "os"], None, None, None
        ),
        SystemOverviewBaseSensor(
            coordinator, "host_os_supervisor", "Host OS (Supervisor)",
            ["supervisor", "host_info", "operating_system"], None, None, None
        ),
        SystemOverviewBaseSensor(
            coordinator, "docker_version", "Docker Version",
            ["host", "docker_version"], None, None, None,
        ),
        SystemOverviewBaseSensor(
            coordinator, "host_cpu", "Host CPU Percent",
            ["host", "cpu_percent"], "%", SensorStateClass.MEASUREMENT, 1
        ),
        SystemOverviewBaseSensor(
            coordinator, "host_mem", "Host Memory Percent",
            ["host", "memory_percent"], "%", SensorStateClass.MEASUREMENT, 1
        ),
        SystemOverviewBaseSensor(
            coordinator, "host_disk", "Host Disk Used Percent",
            ["host", "disk_used_percent"], "%", SensorStateClass.MEASUREMENT, 1
        ),

        SystemOverviewBaseSensor(
            coordinator, "url_internal", "Internal URL",
            ["urls", "internal_url"], None, None, None
        ),
        SystemOverviewBaseSensor(
            coordinator, "url_external", "External URL",
            ["urls", "external_url"], None, None, None
        ),

        SystemOverviewBaseSensor(
            coordinator, "supervisor_available", "Supervisor Available",
            ["supervisor", "available"], None, None, None
        ),
    ]

    async_add_entities(entities)