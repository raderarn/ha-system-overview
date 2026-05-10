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


def _extract_docker_version(info_obj, host_obj):
    candidates = []

    if isinstance(info_obj, dict):
        candidates.append(info_obj.get("docker"))
        candidates.append(info_obj.get("docker_version"))
        candidates.append(info_obj.get("container_engine"))
        docker_obj = info_obj.get("docker")
        if isinstance(docker_obj, dict):
            candidates.append(docker_obj.get("version"))

    if isinstance(host_obj, dict):
        candidates.append(host_obj.get("docker"))
        candidates.append(host_obj.get("docker_version"))
        docker_obj = host_obj.get("docker")
        if isinstance(docker_obj, dict):
            candidates.append(docker_obj.get("version"))

    for c in candidates:
        if isinstance(c, str) and c.strip():
            return c.strip()

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

        host_os = await self.hass.async_add_executor_job(platform.platform)

        token = os.environ.get("SUPERVISOR_TOKEN")
        supervisor_core_info = None
        supervisor_info = None
        supervisor_system_info = None
        host_info = None
        core_stats = None
        supervisor_stats = None

        if token:
            supervisor_core_info = await _supervisor_get_json(self._session, token, "/core/info")
            supervisor_info = await _supervisor_get_json(self._session, token, "/supervisor/info")
            supervisor_system_info = await _supervisor_get_json(self._session, token, "/info")
            host_info = await _supervisor_get_json(self._session, token, "/host/info")
            core_stats = await _supervisor_get_json(self._session, token, "/core/stats")
            supervisor_stats = await _supervisor_get_json(self._session, token, "/supervisor/stats")

        docker_version = _extract_docker_version(supervisor_system_info, host_info)

        return {
            "core": {
                "version": HA_VERSION,
            },
            "host": {
                "hostname": socket.gethostname(),
                "ip_address": ip4,
                "os": host_os,
                "cpu_percent": cpu_percent,
                "memory_percent": mem.percent,
                "disk_used_percent": disk.percent,
                "docker_version": docker_version,
            },
            "urls": {
                "internal_url": self.hass.config.internal_url,
                "external_url": self.hass.config.external_url,
            },
            "supervisor": {
                "available": token is not None,
                "core_info": supervisor_core_info,
                "supervisor_info": supervisor_info,
                "system_info": supervisor_system_info,
                "host_info": host_info,
                "core_stats": core_stats,
                "supervisor_stats": supervisor_stats,
            },
        }
LOG_PROVIDERS = [
    "supervisor",
    "core",
    "host",
    "dns",
    "audio",
    "multicast",
]

DEFAULT_LOG_PROVIDER = "supervisor"
DEFAULT_LOG_LINES = 400


def _tail_lines(text, max_lines, max_chars=12000):
    if not isinstance(text, str):
        return ""
    lines = text.splitlines()
    if len(lines) > max_lines:
        text = "\n".join(lines[-max_lines:])
    if len(text) > max_chars:
        text = text[-max_chars:]
    return text


async def _supervisor_get_text(session, token, path):
    url = "http://supervisor" + path
    headers = {"Authorization": "Bearer " + token}
    try:
        async with session.get(url, headers=headers, timeout=aiohttp.ClientTimeout(total=20)) as resp:
            if resp.status != 200:
                return None
            return await resp.text()
    except Exception:
        return None


class SystemOverviewLogsCoordinator(DataUpdateCoordinator):
    def __init__(self, hass: HomeAssistant):
        self._session = async_get_clientsession(hass)
        self.provider = DEFAULT_LOG_PROVIDER
        self.lines = DEFAULT_LOG_LINES
        super().__init__(
            hass=hass,
            logger=_LOGGER,
            name=DOMAIN + "_logs",
            update_interval=timedelta(seconds=UPDATE_INTERVAL_SECONDS),
        )

    async def _async_update_data(self):
        token = os.environ.get("SUPERVISOR_TOKEN")
        if not token:
            return {
                "available": False,
                "provider": self.provider,
                "text": "",
                "error": "SUPERVISOR_TOKEN is not set",
            }

        # Common patterns: /<provider>/logs/latest and /<provider>/logs 
        text = await _supervisor_get_text(self._session, token, "/" + self.provider + "/logs/latest")
        if text is None:
            text = await _supervisor_get_text(self._session, token, "/" + self.provider + "/logs")

        if text is None:
            return {
                "available": True,
                "provider": self.provider,
                "text": "",
                "error": "Failed to fetch logs",
            }

        return {
            "available": True,
            "provider": self.provider,
            "text": _tail_lines(text, self.lines),
            "error": None,
        }

    async def async_update_logs(self, provider=None, lines=None):
        if isinstance(provider, str) and provider:
            self.provider = provider
        if isinstance(lines, int) and lines > 0:
            self.lines = lines
        await self.async_request_refresh()
