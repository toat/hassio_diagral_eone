"""WeatherFlow Data Wrapper."""
from __future__ import annotations

import asyncio
import logging
import socket
import time

import aiohttp
import async_timeout
from yarl import URL

import json
import uuid

from .const import (
    AUTH_URL,
    DEFAULT_BASE_URL,
    DEFAULT_TIMEOUT_IN_SECONDS,
    CONFIGURATION_URL,
    DEVICES_URL,
    ISCONNECTED_URL,
    CONNECT_URL,
    DEVICESMULTIZONE_URL,
    MEASURES_TOTAL_URL,
    SYSTEM_URL,
    STATES_URL,
    MAX_RETRY,
)
from .exceptions import (
    CommunicationException,
    InvalidCredentialsException,
    UnauthorizedException,
    NotConnectedException,
    MaxRetry,
)
from .models import Configuration, Login, Measure, System, IsConnected
from .models import Connect, Devices, DevicesMultizone

_LOGGER = logging.getLogger(__name__)


class EOneApiClient:
    """Main class to perform EOne API requests."""

    _session: aiohttp.ClientSession = None

    def __init__(self, base_url: str, session: aiohttp.ClientSession) -> None:
        """Initialize."""
        self._session = session
        self._base_url = (
            base_url
            if base_url and not base_url.isspace()
            else DEFAULT_BASE_URL
        )

    async def _execute_request(
        self,
        method: str,
        path: str,
        params: dict | None = None,
        headers: dict | None = None,
        json: dict | None = None,
    ) -> any:
        """Execute request."""
        try:
            _LOGGER.debug(
                "Data for request method %s, url: %s, headers: %s, params: %s, json: %s",
                method,
                URL(self._base_url).with_path(path),
                headers,
                params,
                json,
            )
            async with async_timeout.timeout(DEFAULT_TIMEOUT_IN_SECONDS):
                response = await self._session.request(
                    method=method,
                    url=URL(self._base_url).with_path(path),
                    headers=headers,
                    params=params,
                    json=json,
                )

                _LOGGER.debug(
                    "Data retrieved from %s, status: %s, content_type: %s, text: %s, content_length: %s",
                    response.url,
                    response.status,
                    response.content_type,
                    response.text,
                    response.content_length
                )
                response.raise_for_status()
                if response.content_type == "application/octet-stream":
                    data = await response.text()
                else:
                    data = await response.json()

                return data, response.status
        except (
            asyncio.TimeoutError,
            aiohttp.ClientError,
            socket.gaierror,
            Exception,
        ) as exception:
            _LOGGER.debug("An error occured : %s", exception, exc_info=True)
            raise CommunicationException() from exception

    async def async_login(self, email: str, password: str) -> Login:
        """Log user and return the authentication token."""
        response, status = await self._execute_request(
            "post",
            AUTH_URL,
            json={
                "username": email,
                "password": password
            },
            headers={
                "User-Agent": "Jeedom/1.0",
                "Accept": "application/json, text/plain, */*",
                "Accept-Encoding": "deflate",
                "X-App-Version": "1.12.1",
                "X-Identity-Provider": "JANRAIN",
                "ttmSessionIdNotRequired": "true",
                "X-Vendor": "diagral",
                "Content-Type": "application/json;charset=UTF-8",
                "Connection": "Close",
                # "Content-Length": str(len(json.dumps({"username": email,"password": password}))),
            },
        )

        _LOGGER.debug("response : %s, status %s", response, status)

        if "sessionId" not in response:
            if response["error"] in (
                "invalid.credentials",
                "undefined.email",
                "undefined.password",
            ):
                raise InvalidCredentialsException()

        return Login(response["sessionId"])

    async def async_get_system(self, session_id: str) -> System:
        """Get user profile."""
        response, status = await self._execute_request(
            "post",
            SYSTEM_URL,
            headers={
                "Authorization": "Bearer " + session_id,
                "User-Agent": "Jeedom/1.0",
                "Accept": "application/json, text/plain, */*",
                "Accept-Encoding": "deflate",
                "X-App-Version": "1.12.1",
                "X-Identity-Provider": "JANRAIN",
                "ttmSessionIdNotRequired": "true",
                "X-Vendor": "diagral",
                "Content-Type": "application/json;charset=UTF-8",
                "Connection": "Close",
            },
        )

        _LOGGER.debug("response : %s, status %s", response, status)

        if status != "200":
            if status == "not.authorized":
                raise UnauthorizedException()

        return System(response["diagralId"], response["systems"])

    async def async_get_configuration(self, session_id: str, system_id: int, system_role: int) -> Configuration:
        """Get user devices (virtual and battery)."""
        response, status = await self._execute_request(
            "post",
            CONFIGURATION_URL,
            json={
                "systemId": system_id,
                "role": system_role,
            },
            headers={
                "Authorization": "Bearer " + session_id,
                "User-Agent": "Jeedom/1.0",
                "Accept": "application/json, text/plain, */*",
                "Accept-Encoding": "deflate",
                "X-App-Version": "1.12.1",
                "X-Identity-Provider": "JANRAIN",
                "ttmSessionIdNotRequired": "true",
                "X-Vendor": "diagral",
                "Content-Type": "application/json;charset=UTF-8",
                "Connection": "Close",
                # "Content-Length": str(len(json.dumps(params_data))),
            },
        )

        _LOGGER.debug("response : %s, status %s", response, status)

        if status != "200":
            if status == "not.authorized":
                raise UnauthorizedException()

        return Configuration(
            response['transmitterId'],
            response['centralId'],
            response['installationComplete'],
            response['name'],
            response['role'],
            response['rights'],
            response['id'],
            response['standalone'],
            response['gprsPhone']
            )

    async def async_isconnected(self, session_id: str, transmitter_id: str) -> IsConnected:
        """Get devices."""
        response, status = await self._execute_request(
            "post",
            ISCONNECTED_URL,
            json={
                "transmitterId": transmitter_id,
            },
            headers={
                "Authorization": "Bearer " + session_id,
                "User-Agent": "Jeedom/1.0",
                "Accept": "application/json, text/plain, */*",
                "Accept-Encoding": "deflate",
                "X-App-Version": "1.12.1",
                "X-Identity-Provider": "JANRAIN",
                "ttmSessionIdNotRequired": "true",
                "X-Vendor": "diagral",
                "Content-Type": "application/json;charset=UTF-8",
                "Connection": "Close",
            },
        )

        _LOGGER.debug("response : %s, status %s", response, status)

        if status != "200":
            if status == "not.authorized":
                raise UnauthorizedException()

        return IsConnected(response["isConnected"])

    async def async_connect(self, session_id: str, code: str, transmitter_id: str, system_id: str, role: int, is_connected: bool) -> Connect:
        """Connect."""

        if not is_connected:
            raise NotConnectedException()
            
        response, status = await self._execute_request(
            "post",
            CONNECT_URL,
            json={
                "masterCode": code,
                "transmitterId": transmitter_id,
                "systemId": system_id,
                "role": role,
            },
            headers={
                "Authorization": "Bearer " + session_id,
                "User-Agent": "Jeedom/1.0",
                "Accept": "application/json, text/plain, */*",
                "Accept-Encoding": "deflate",
                "X-App-Version": "1.12.1",
                "X-Identity-Provider": "JANRAIN",
                "ttmSessionIdNotRequired": "true",
                "X-Vendor": "diagral",
                "Content-Type": "application/json;charset=UTF-8",
                "Connection": "Close",
            },
        )

        _LOGGER.debug("response : %s, status %s", response, status)

        if status != "200":
            if status == "not.authorized":
                raise UnauthorizedException()

        return Connect(
            response["message"],
            response["ttmSessionId"],
            response["systemState"],
            response["groups"],
            response["groupList"],
            response["gprsConnection"],
            response["status"],
            response["versions"],
            response["connectedUserType"],
            response["codeIndex"],
            response["userRightsConfiguration"])

    async def async_get_devicesmultizone(self, session_id: str, system_id: str, central_id: str, transmitter_id: str, ttmsession_id: str, box_version: str) -> DevicesMultizone:
        """Get devices."""
        uuidv4 = str(uuid.uuid4())
        retry = 0
        response, status = await self._execute_request(
                "post",
                DEVICESMULTIZONE_URL+uuidv4,
                json={
                    "systemId": system_id,
                    "centralId": central_id,
                    "transmitterId": transmitter_id,
                    "ttmSessionId": ttmsession_id,
                    "isVideoOptional": "true",
                    "isScenariosZoneOptional": "true",
                    "boxVersion": box_version,
                },
                headers={
                    "Authorization": "Bearer " + session_id,
                    "User-Agent": "Jeedom/1.0",
                    "Accept": "application/json, text/plain, */*",
                    "Accept-Encoding": "deflate",
                    "X-App-Version": "1.12.1",
                    "X-Identity-Provider": "JANRAIN",
                    "ttmSessionIdNotRequired": "true",
                    "X-Vendor": "diagral",
                    "Content-Type": "application/json;charset=UTF-8",
                    "Connection": "Close",
                },
            )

        _LOGGER.debug("response : %s, status %s", response, status)

        while 'status' in response and response['status'] == "request_status_not_found" or retry < MAX_RETRY:
            response, status = await self._execute_request(
                "get",
                DEVICESMULTIZONE_URL+uuidv4,
                headers={
                    "Authorization": "Bearer " + session_id,
                    "User-Agent": "Jeedom/1.0",
                    "Accept": "application/json, text/plain, */*",
                    "Accept-Encoding": "deflate",
                    "X-App-Version": "1.12.1",
                    "X-Identity-Provider": "JANRAIN",
                    "ttmSessionIdNotRequired": "true",
                    "X-Vendor": "diagral",
                    "Content-Type": "application/json;charset=UTF-8",
                    "Connection": "Close",
                },
            )

            _LOGGER.debug("response : %s, status %s", response, status)

            if status != "200":
                if status == "not.authorized":
                    raise UnauthorizedException()
            if retry >= MAX_RETRY:
                _LOGGER.error("Unable to get DeviceMultizone (generation in pending) after %s retries", retry)
                raise MaxRetry()
            elif response['status'] == "request_status_done":
                _LOGGER.info("DeviceMultizone is generated... returning result")
                break
            _LOGGER.info("DeviceMultizone is in generation... Pending")
            time.sleep(1)
            retry += 1

        group_names = json.loads(response["response"])["centralLearningZone"]["groupNames"]
        system_state_code = json.loads(response["response"])["statusZone"]["centralStatus"]["sytemState"]
        system_state_text = json.loads(response["response"])["statusZone"]["centralStatus"]["sytemStateText"]
        #_LOGGER.debug("JSON %s", json.dumps(json.loads(response["response"]), indent=2))
        _LOGGER.debug("Found groups : %s", group_names)
        _LOGGER.debug("Found system state code: %s", system_state_code)
        _LOGGER.debug("Found system state: %s", system_state_text)

        return DevicesMultizone(response["response"])

    async def async_get_devices(self, session_id: str, system_id: str) -> Devices:
        """Get devices."""
        response, status = await self._execute_request(
            "get",
            DEVICES_URL+str(system_id)+"/devices",
            headers={
                "Authorization": "Bearer " + session_id,
                "User-Agent": "Jeedom/1.0",
                "Accept": "application/json, text/plain, */*",
                "Accept-Encoding": "deflate",
                "X-App-Version": "1.12.1",
                "X-Identity-Provider": "JANRAIN",
                "ttmSessionIdNotRequired": "true",
                "X-Vendor": "diagral",
                "Content-Type": "application/json;charset=UTF-8",
                "Connection": "Close",
            },
        )

        _LOGGER.debug("response : %s, status %s", response, status)

        if status != "200":
            if status == "not.authorized":
                raise UnauthorizedException()

        return Devices(response["diagralId"], response["systems"])          

    async def async_get_measures_total(
        self, auth_token: str, phase: str, device_id: str
    ) -> list[Measure]:
        """Get device measures total."""
        response = await self._execute_request(
            "get",
            MEASURES_TOTAL_URL,
            params={
                "authToken": auth_token,
                "measureType": phase,
                "deviceId": device_id,
            },
        )

        if response["status"] == "error":
            if response["error"] == "not.authorized":
                raise UnauthorizedException()

        measures: list[Measure] = []
        for value in response["measure"]["values"]:
            measures.append(
                Measure(value["type"], value["value"], value["unit"])
            )

        return measures

    async def async_get_battery_state(
        self, auth_token: str, battery_id: str
    ) -> Measure | None:
        """Get battery state."""
        response = await self._execute_request(
            "get", STATES_URL, params={"authToken": auth_token}
        )

        if response["status"] == "error":
            if response["error"] == "not.authorized":
                raise UnauthorizedException()

        measure: Measure | None = None

        for device in response["deviceStates"]:
            if device["deviceId"] == battery_id:
                for state in device["sensorStates"]:
                    if state["sensorId"] == battery_id + "-soc":
                        measure = Measure(
                            state["measure"]["type"],
                            state["measure"]["value"],
                            state["measure"]["unit"],
                        )
                        return measure

        return measure

    async def async_turn_off(self, auth_token: str, relay_id: str) -> str:
        """Turn off the switch."""
        response = await self._execute_request(
            "get",
            SWITCH_URL,
            params={
                "authToken": auth_token,
                "id": relay_id,
                "on": "false",
            },
        )

        if response["status"] == "error":
            if response["error"] == "switch.not.allowed":
                return "off"
            if response["error"] == "not.authorized":
                raise UnauthorizedException()

        return response["state"]

    async def async_turn_on(self, auth_token: str, relay_id: str) -> str:
        """Turn on the switch."""
        response = await self._execute_request(
            "get",
            SWITCH_URL,
            params={
                "authToken": auth_token,
                "id": relay_id,
                "on": "true",
            },
        )

        if response["status"] == "error":
            if response["error"] == "switch.not.allowed":
                return "on"
            if response["error"] == "not.authorized":
                raise UnauthorizedException()

        return response["state"]

    async def async_get_relay_state(
        self, auth_token: str, relay_id: str
    ) -> str | None:
        """Get relay state."""
        response = await self._execute_request(
            "get", STATES_URL, params={"authToken": auth_token}
        )

        if response["status"] == "error":
            if response["error"] == "not.authorized":
                raise UnauthorizedException()

        for device in response["deviceStates"]:
            if device["deviceId"] == relay_id:
                return device["state"]

        return None
