from homeassistant.components.diagnostics.util import async_redact_data

TO_REDACT = []

async def async_get_config_entry_diagnostics(hass, entry):
    coordinator = entry.runtime_data
    data = coordinator.data if coordinator is not None and coordinator.data is not None else {}
    return {
        "entry_data": async_redact_data(dict(entry.data), TO_REDACT),
        "data": data,
    }