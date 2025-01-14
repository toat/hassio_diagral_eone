"""Custom integration to integrate eone with Home Assistant."""
from __future__ import annotations

from homeassistant.config_entries import ConfigEntry
from homeassistant.const import CONF_URL
from homeassistant.core import HomeAssistant
from homeassistant.helpers.aiohttp_client import async_get_clientsession

from .api.client import DEFAULT_BASE_URL, EOneApiClient
from .const import DOMAIN, PLATFORMS, DATA_COORDINATOR
from .coordinator import EOneDataUpdateCoordinator


# https://developers.home-assistant.io/docs/config_entries_index/#setting-up-an-entry
async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up this integration using UI."""
    session = async_get_clientsession(hass)

    client = EOneApiClient(
        base_url=entry.data.get(CONF_URL, DEFAULT_BASE_URL),
        session=session,
    )
    local_coordinator = EOneDataUpdateCoordinator(hass=hass, client=client)

    hass.data.setdefault(DOMAIN, {})[entry.entry_id] = {DATA_COORDINATOR: local_coordinator}

    # https://developers.home-assistant.io/docs/integration_fetching_data#coordinated-single-api-poll-for-data-for-all-entities
    await local_coordinator.async_config_entry_first_refresh()

    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)
    entry.async_on_unload(entry.add_update_listener(async_reload_entry))

    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Handle removal of an entry."""
    if unloaded := await hass.config_entries.async_unload_platforms(
        entry, PLATFORMS
    ):
        hass.data[DOMAIN].pop(entry.entry_id)
    return unloaded


async def async_reload_entry(hass: HomeAssistant, entry: ConfigEntry) -> None:
    """Reload config entry."""
    await async_unload_entry(hass, entry)
    await async_setup_entry(hass, entry)
