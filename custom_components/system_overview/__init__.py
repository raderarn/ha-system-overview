from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant

from .const import DOMAIN
from .coordinator import (
    SystemOverviewCoordinator,
    SystemOverviewLogsCoordinator,
)

PLATFORMS = ["sensor", "select"]


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    # Main system overview coordinator (existing)
    coordinator = SystemOverviewCoordinator(hass)
    await coordinator.async_config_entry_first_refresh()

    # Logs coordinator (new)
    logs_coordinator = SystemOverviewLogsCoordinator(hass)
    await logs_coordinator.async_config_entry_first_refresh()

    # Store both coordinators
    hass.data.setdefault(DOMAIN, {})
    hass.data[DOMAIN][entry.entry_id] = {
        "coordinator": coordinator,
        "logs_coordinator": logs_coordinator,
    }

    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)
    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    unload_ok = await hass.config_entries.async_unload_platforms(entry, PLATFORMS)
    if unload_ok and DOMAIN in hass.data:
        hass.data[DOMAIN].pop(entry.entry_id, None)
    return unload_ok