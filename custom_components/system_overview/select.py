from homeassistant.components.select import SelectEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity import EntityCategory
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .const import DOMAIN, NAME
from .coordinator import LOG_PROVIDERS


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    data = hass.data[DOMAIN][entry.entry_id]
    logs_coordinator = data["logs_coordinator"]

    async_add_entities([SystemOverviewLogProviderSelect(logs_coordinator)], True)


class SystemOverviewLogProviderSelect(SelectEntity):
    _attr_entity_category = EntityCategory.DIAGNOSTIC
    _attr_icon = "mdi:format-list-bulleted"
    _attr_unique_id = DOMAIN + "_log_provider"

    def __init__(self, logs_coordinator) -> None:
        self._logs = logs_coordinator
        self._attr_name = NAME + " Log Provider"
        self._attr_options = list(LOG_PROVIDERS)

    @property
    def current_option(self) -> str:
        return self._logs.provider

    async def async_select_option(self, option: str) -> None:
        await self._logs.async_update_logs(provider=option)