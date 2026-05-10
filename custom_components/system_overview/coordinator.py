from datetime import timedelta
import logging
import os
import platform
import socket

import aiohttp
import psutil

from homeassistant.const import __version__ as HA_VERSION
from homeassistant.core import HomeAssistant
from homeassistant.helpers.aiohttp_client import async_get_clientsession
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator

from .const import DOMAIN, UPDATE_INTERVAL_SECONDS

_LOGGER = logging.getLogger(__name__)


def _get_primary_ipv4():
    try:
        for ifname, addrs in psutil.net_if_addrs().items():
            for addr in addrs:
                if getattr(addr, "family", None) == socket.AF_INET:
                    ip = getattr(addr, "address", None)
                    if ip and not ip.startswith("127."):
                        return ip
    except Exception:
        return None
    return None


async def _supervisor_get_json(session, token, path):
    url = "http://supervisor" + path
    headers = {"Authorization": "Bearer " + token}
    try:
        async with session.get(url, headers=headers, timeout=aiohttp.ClientTimeout(total=10)) as resp:
            if resp.status != 200:
                return None
            data = await resp.json()
            if isinstance(data, dict) and "data" in data:
                return data.get("data")
            return data
    except Exception:
        return None


class SystemOverviewCoordinator(DataUpdateCoordinator):
    def __init__(self, hass: HomeAssistant):
        psutil.cpu_percent(interval=None)
        self._session = async_get_clientsession(hass)
        super().__init__(
            hass=hass,
            logger=_LOGGER,
            name=DOMAIN,
            update_interval=timedelta(seconds=UPDATE_INTERVAL_SECONDS),
        )

    async def _async_update_data(self):
        cpu_percent = psutil.cpu_percent(interval=None)
        mem = psutil.virtual_memory()
        disk = psutil.disk_usage("/")
        ip4 = _get_primary_ipv4()

        token = os.environ.get("SUPERVISOR_TOKEN")
        supervisor_core_info = None
        supervisor_info = None
        host_info = None
        core_stats = None
        supervisor_stats = None

        if token:
            supervisor_core_info = await _supervisor_get_json(self._session, token, "/core/info")
            supervisor_info = await _supervisor_get_json(self._session, token, "/supervisor/info")
            host_info = await _supervisor_get_json(self._session, token, "/host/info")
            core_stats = await _supervisor_get_json(self._session, token, "/core/stats")
            supervisor_stats = await _supervisor_get_json(self._session, token, "/supervisor/stats")

        return {
            "core": {
                "version": HA_VERSION,
            },
            "host": {
                "hostname": socket.gethostname(),
                "ip_address": ip4,
                "os": platform.platform(),
                "cpu_percent": cpu_percent,
                "memory_percent": mem.percent,
                "disk_used_percent": disk.percent,
            },
            "urls": {
                "internal_url": self.hass.config.internal_url,
                "external_url": self.hass.config.external_url,
            },
            "supervisor": {
                "available": token is not None,
                "core_info": supervisor_core_info,
                "supervisor_info": supervisor_info,
                "host_info": host_info,
                "core_stats": core_stats,
                "supervisor_stats": supervisor_stats,
            },
        }
