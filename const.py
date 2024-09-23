"""Constants for EOne."""
from logging import Logger, getLogger

from homeassistant.const import Platform

LOGGER: Logger = getLogger(__package__)

# General
NAME = "EOne"
DOMAIN = "eone"
PLATFORMS = [Platform.SENSOR, Platform.SWITCH]
VERSION = "0.0.1"
COORDINATOR = "coordinator"
ATTRIBUTION = "Data provided by EOne"
SCAN_INTERVAL_IN_MINUTES = 15

# Configuration
CONF_VIRTUAL_DEVICE_ID = "virtual_device_id"
CONF_VIRTUAL_BATTERY_ID = "virtual_battery_id"
CONF_MASTER_ID = "master_id"
CONF_MASTER_REPORT_PERIOD = "master_report_period"
CONF_SUBSCRIPTION_ID = "subscription_id"
CONF_GRID_TYPE = "grid_type"
CONF_MASTER_RELAY_ID = "master_relay_id"
CONF_WATER_HEATER_ID = "water_heater_id"

# Data
DATA_COORDINATOR = "coordinator"
