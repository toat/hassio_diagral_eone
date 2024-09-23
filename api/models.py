"""Api Models."""


class Login:
    """Login model."""

    __session_id: str = None

    def __init__(self, session_id: str) -> None:
        """Initialize."""
        self.__session_id = session_id

    @property
    def session_id(self):
        """Return session_id."""
        return self.__session_id


class System:
    """System model."""

    __diagral_id: str = None
    __systems: list = None

    def __init__(self, diagral_id: str, systems: dict) -> None:
        """Initialize."""
        self.__diagral_id = diagral_id
        self.__systems = systems

    @property
    def diagral_id(self):
        """Return subscription id."""
        return self.__diagral_id

    @property
    def systems(self):
        """Return grid type."""
        return self.__systems


class Configuration:
    """Configuration  model"""

    __transmitter_id: str = None
    __central_id: str = None
    __installation_complete: bool = None
    __name: str = None
    __role: int = None
    __rights: dict = None
    __id: int = None
    __standalone: bool = None 
    __gprs_phone: str = None

    def __init__(self, transmitter_id: str, central_id: str, installation_complete: bool, name: str, role: int, rights: dict, id: int, standalone: bool, gprs_phone: str) -> None:
        """Initialize."""
        self.__transmitter_id = transmitter_id
        self.__central_id = central_id
        self.__installation_complete = installation_complete
        self.__name = name
        self.__role = role
        self.__rights = rights
        self.__id = id
        self.__standalone = standalone
        self.__gprs_phone = gprs_phone

    @property
    def transmitter_id(self):
        """Return master id."""
        return self.__transmitter_id

    @transmitter_id.setter
    def transmitter_id(self, value: str):
        """Set master id."""
        self.__transmitter_id = value

    @property
    def central_id(self):
        """Return master report period."""
        return self.__central_id

    @central_id.setter
    def central_id(self, value: str):
        """Set master report period."""
        self.__central_id = value

    @property
    def installation_complete(self):
        """Return virtual device id."""
        return self.__installation_complete

    @installation_complete.setter
    def installation_complete(self, value: bool):
        """Set virtual device id id."""
        self.__installation_complete = value

    @property
    def name(self):
        """Return virtual battery id."""
        return self.__name

    @name.setter
    def name(self, value: str):
        """Set virtual battery id."""
        self.__name = value

    @property
    def role(self):
        """Return master relay id."""
        return self.__role

    @role.setter
    def role(self, value: int):
        """Set master relay id."""
        self.__role = value

    @property
    def rights(self):
        """Return master relay id."""
        return self.__rights

    @rights.setter
    def rights(self, value: dict):
        """Set master relay id."""
        self.__rights = value

    @property
    def id(self):
        """Return water heater device id."""
        return self.__id

    @id.setter
    def id(self, value: int):
        """Set water heater id."""
        self.__id = value

    @property
    def standalone(self):
        """Return water heater device id."""
        return self.__standalone

    @standalone.setter
    def standalone(self, value: bool):
        """Set water heater id."""
        self.__standalone = value

    @property
    def gprs_phone(self):
        """Return water heater device id."""
        return self.__gprs_phone

    @gprs_phone.setter
    def gprs_phone(self, value: str):
        """Set water heater id."""
        self.__gprs_phone = value


class Devices:
    """Devices model."""

    __diagral_id: str = None
    __systems: list = None

    def __init__(self, diagral_id: str, systems: dict) -> None:
        """Initialize."""
        self.__diagral_id = diagral_id
        self.__systems = systems

    @property
    def diagral_id(self):
        """Return subscription id."""
        return self.__diagral_id

    @property
    def systems(self):
        """Return grid type."""
        return self.__systems


class IsConnected:
    """IsConnect model."""

    __is_connected: bool = None

    def __init__(self, is_connected: bool) -> None:
        """Initialize."""
        self.__is_connected = is_connected

    @property
    def is_connected(self):
        """Return subscription id."""
        return self.__is_connected

    @is_connected.setter
    def gprs_phone(self, value: str):
        """Set water heater id."""
        self.__is_connected = value    


class Connect:
    """Connect model."""
    
    __message: str = None
    __ttmsession_id: str = None
    __system_state: str = None
    __groups: list = None
    __group_list: list = None
    __gprs_connection: bool = None
    __status: str = None
    __version: dict = None
    __connected_user_type: str = None
    __code_index: int = None
    __userrights_configuration: str = None


    def __init__(self, message: str, ttmsession_id: str, system_state: str, groups: list, group_list: list, gprs_connection: bool, status: str, version: dict, connected_user_type: str, code_index: int, userrights_configuration: str) -> None:
        """Initialize."""
        self.__message = message
        self.__ttmsession_id = ttmsession_id
        self.__system_state = system_state
        self.__groups = groups
        self.__group_list = group_list
        self.__gprs_connection = gprs_connection
        self.__status = status
        self.__version = version
        self.__connected_user_type = connected_user_type
        self.__code_index = code_index 
        self.__userrights_configuration = userrights_configuration

    @property
    def message(self):
        """Return master id."""
        return self.__message

    @message.setter
    def message(self, value: str):
        """Set master id."""
        self.__message = value

    @property
    def ttmsession_id(self):
        """Return master id."""
        return self.__ttmsession_id

    @ttmsession_id.setter
    def transmitter_id(self, value: str):
        """Set master id."""
        self.__ttmsession_id = value

    @property
    def system_state(self):
        """Return master report period."""
        return self.__system_state

    @system_state.setter
    def system_state(self, value: str):
        """Set master report period."""
        self.__system_state = value

    @property
    def groups(self):
        """Return virtual device id."""
        return self.__groups

    @groups.setter
    def groups(self, value: list):
        """Set virtual device id id."""
        self.__groups = value

    @property
    def group_list(self):
        """Return virtual battery id."""
        return self.__group_list

    @group_list.setter
    def group_list(self, value: list):
        """Set virtual battery id."""
        self.__group_list = value

    @property
    def gprs_connection(self):
        """Return master relay id."""
        return self.__gprs_connection

    @gprs_connection.setter
    def gprs_connection(self, value: bool):
        """Set master relay id."""
        self.__gprs_connection = value

    @property
    def status(self):
        """Return master relay id."""
        return self.__status

    @status.setter
    def status(self, value: str):
        """Set master relay id."""
        self.__status = value

    @property
    def version(self):
        """Return water heater device id."""
        return self.__version

    @version.setter
    def version(self, value: dict):
        """Set water heater id."""
        self.__version = value

    @property
    def connected_user_type(self):
        """Return water heater device id."""
        return self.__connected_user_type

    @connected_user_type.setter
    def connected_user_type(self, value: str):
        """Set water heater id."""
        self.__connected_user_type = value

    @property
    def code_index(self):
        """Return water heater device id."""
        return self.__code_index

    @code_index.setter
    def code_index(self, value: int):
        """Set water heater id."""
        self.__code_index = value

    @property
    def userrights_configuration(self):
        """Return water heater device id."""
        return self.__userrights_configuration

    @userrights_configuration.setter
    def userrights_configuration(self, value: str):
        """Set water heater id."""
        self.__userrights_configuration = value

class DevicesMultizone:
    """DevicesMultizone model."""

    __is_connected: bool = None

    def __init__(self, is_connected: bool) -> None:
        """Initialize."""
        self.__is_connected = is_connected

    @property
    def is_connected(self):
        """Return subscription id."""
        return self.__is_connected

    @is_connected.setter
    def gprs_phone(self, value: str):
        """Set water heater id."""
        self.__is_connected = value   


# class Devices:
#     """Devices model."""

#     __is_connected: bool = None

#     def __init__(self, is_connected: bool) -> None:
#         """Initialize."""
#         self.__is_connected = is_connected

#     @property
#     def is_connected(self):
#         """Return subscription id."""
#         return self.__is_connected

#     @is_connected.setter
#     def gprs_phone(self, value: str):
#         """Set water heater id."""
#         self.__is_connected = value   


class Measure:
    """Represent a measure."""

    def __init__(self, key: str, value: float, unit: str) -> None:
        """Initialize."""
        self.__type = key
        self.__value = value
        self.__unit = unit

    @property
    def type(self) -> str:
        """Return measure type."""
        return self.__type

    @property
    def value(self) -> float:
        """Return measure value."""
        return self.__value

    @property
    def unit(self) -> str:
        """Return measure unit."""
        return self.__unit
