"""Exception handling for EOne Systems API."""


class EOneException(Exception):
    """Exception to indicate a general API error."""

    def __init__(self, msg: str) -> None:
        """Initialize."""
        super().__init__()
        self.__msg = msg

    @property
    def msg(self) -> str:
        """Return error message."""
        return self.__msg


class CommunicationException(EOneException):
    """Exception to indicate a communication error."""

    def __init__(self) -> None:
        """Initialize."""
        super().__init__("A communication error occured")


class InvalidCredentialsException(EOneException):
    """Exception to indicate an authentication error."""

    def __init__(self) -> None:
        """Initialize."""
        super().__init__("Invalid credentials")


class UnauthorizedException(EOneException):
    """Exception to indicate an authorization error."""

    def __init__(self) -> None:
        """Initialize."""
        super().__init__("Unauthorized")


class NotConnectedException(EOneException):
    """Exception to indicate an authorization error."""

    def __init__(self) -> None:
        """Initialize."""
        super().__init__("NotConnected")       


class MaxRetry(EOneException):
    """Exception to indicate max retries waiting."""

    def __init__(self) -> None:
        """Initialize."""
        super().__init__("MaxRetry")               
