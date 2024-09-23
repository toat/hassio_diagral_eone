"""Adds config flow for eone."""
from __future__ import annotations

import voluptuous as vol
from homeassistant import config_entries
from homeassistant.const import CONF_EMAIL, CONF_PASSWORD, CONF_URL, CONF_CODE
from homeassistant.helpers import selector
from homeassistant.helpers.aiohttp_client import async_create_clientsession

from .api.client import DEFAULT_BASE_URL, EOneApiClient
from .api.exceptions import (
    CommunicationException,
    InvalidCredentialsException,
    EOneException,
)
from .const import (
    CONF_GRID_TYPE,
    CONF_MASTER_ID,
    CONF_MASTER_REPORT_PERIOD,
    CONF_SUBSCRIPTION_ID,
    CONF_VIRTUAL_BATTERY_ID,
    CONF_VIRTUAL_DEVICE_ID,
    DOMAIN,
    LOGGER,
    CONF_MASTER_RELAY_ID,
    CONF_WATER_HEATER_ID,
)


class EOneFlowHandler(config_entries.ConfigFlow, domain=DOMAIN):
    """Config flow for EOne."""

    VERSION = 1
    CONNECTION_CLASS = config_entries.CONN_CLASS_CLOUD_POLL

    async def async_step_user(
        self,
        user_input: dict | None = None,
    ) -> config_entries.FlowResult:
        """Handle a flow initialized by the user."""
        _errors = {}
        if user_input is not None:
            try:
                api_client = EOneApiClient(
                    base_url=user_input[CONF_URL],
                    session=async_create_clientsession(self.hass),
                )

                login_response = await api_client.async_login(
                    user_input[CONF_EMAIL], user_input[CONF_PASSWORD]
                )

                LOGGER.debug(login_response)

                system_response = await api_client.async_get_system(
                    login_response.session_id
                )
                
                LOGGER.debug(system_response)
                
                for system in system_response.systems:
                    configuration_response = await api_client.async_get_configuration(
                        login_response.session_id,
                        system['id'],
                        system['role']
                    )
                    
                    LOGGER.debug(configuration_response)

                    isconnected_response = await api_client.async_isconnected(
                        login_response.session_id,
                        configuration_response.transmitter_id
                    )

                    LOGGER.debug(isconnected_response)

                    connect_response = await api_client.async_connect(
                        login_response.session_id,
                        user_input[CONF_CODE],
                        configuration_response.transmitter_id,
                        configuration_response.id,
                        configuration_response.role,
                        isconnected_response.is_connected,
                    )

                    LOGGER.debug(connect_response)

                    # devices_response = await api_client.async_get_devices(
                    #     login_response.session_id,
                    #     configuration_response.id,
                    # )

                    # LOGGER.debug(devices_response)

                    devicesmultizone_reponse = await api_client.async_get_devicesmultizone(
                        login_response.session_id,
                        configuration_response.id,
                        configuration_response.central_id,
                        configuration_response.transmitter_id,
                        connect_response.ttmsession_id,
                        connect_response.version['box'],
                    )

                    LOGGER.debug(devicesmultizone_reponse) 
                    # devices_response = await api_client.async_get_devices(
                    #     login_response.session_id,
                    #     configuration_response.id,
                    # )
                                       

                data = {
                    # CONF_EMAIL: user_input[CONF_EMAIL],
                    # CONF_PASSWORD: user_input[CONF_PASSWORD],
                    # CONF_URL: user_input[CONF_URL],
                    # CONF_SUBSCRIPTION_ID: user_profile.subscription_id,
                    # CONF_GRID_TYPE: user_profile.grid_type,
                    # CONF_VIRTUAL_DEVICE_ID: device_ids.virtual_device_id,
                    # CONF_VIRTUAL_BATTERY_ID: device_ids.virtual_battery_id,
                    # CONF_MASTER_ID: device_ids.master_id,
                    # CONF_MASTER_REPORT_PERIOD: device_ids.master_report_period,
                    # CONF_MASTER_RELAY_ID: device_ids.master_relay_id,
                    # CONF_WATER_HEATER_ID: device_ids.water_heater_id,
                }

                # await self.async_set_unique_id(
                #     str(user_profile.subscription_id)
                # )

                self._abort_if_unique_id_configured()

            except InvalidCredentialsException as exception:
                LOGGER.warning(exception)
                _errors["base"] = "auth"
            except CommunicationException as exception:
                LOGGER.error(exception)
                _errors["base"] = "connection"
            except EOneException as exception:
                LOGGER.exception(exception)
                _errors["base"] = "unknown"
            else:
                return self.async_create_entry(
                    title=user_profile.subscription_id,
                    data=data,
                )

        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema(
                {
                    vol.Required(
                        CONF_EMAIL,
                        default=(user_input or {}).get(CONF_EMAIL),
                    ): selector.TextSelector(
                        selector.TextSelectorConfig(
                            type=selector.TextSelectorType.EMAIL
                        ),
                    ),
                    vol.Required(CONF_PASSWORD): selector.TextSelector(
                        selector.TextSelectorConfig(
                            type=selector.TextSelectorType.PASSWORD
                        ),
                    ),
                    vol.Required(CONF_CODE): selector.TextSelector(
                        selector.TextSelectorConfig(
                            type=selector.TextSelectorType.PASSWORD
                        ),
                    ),
                    vol.Optional(
                        CONF_URL, default=DEFAULT_BASE_URL
                    ): selector.TextSelector(
                        selector.TextSelectorConfig(
                            type=selector.TextSelectorType.URL,
                        ),
                    ),
                }
            ),
            errors=_errors,
        )
