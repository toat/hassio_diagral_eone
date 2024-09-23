"""Constants for EOne Systems library."""
DEFAULT_TIMEOUT_IN_SECONDS: int = 60
MAX_RETRY = 100

DEFAULT_BASE_URL: str = "https://appv3.tt-monitor.com"
AUTH_URL: str = "/topaze/authenticate/login"
SYSTEM_URL: str = "/topaze/configuration/getSystems"
CONFIGURATION_URL: str = "/topaze/configuration/getConfiguration"
DEVICES_URL: str = "/topaze/api/scenarios/"
ISCONNECTED_URL: str = "/topaze/installation/isConnected"
CONNECT_URL: str = "/topaze/authenticate/connect"
DEVICESMULTIZONE_URL: str = "/topaze/configuration/v2/getDevicesMultizone/"
MEASURES_TOTAL_URL: str = "/api/measures/total"
STATES_URL: str = "/api/states"
