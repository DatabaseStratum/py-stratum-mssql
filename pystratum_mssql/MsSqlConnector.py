import abc
from typing import Any


class MsSqlConnector:
    """
    Interface for classes for connecting to a MS SQL Server instances.
    """

    # ------------------------------------------------------------------------------------------------------------------
    @abc.abstractmethod
    def connect(self) -> Any:
        """
        Connects to a MS SQL Server instance.
        """
        raise NotImplementedError()

    # ------------------------------------------------------------------------------------------------------------------
    @abc.abstractmethod
    def disconnect(self) -> None:
        """
        Disconnects from a MS SQL Server instance.
        """
        raise NotImplementedError()

# ----------------------------------------------------------------------------------------------------------------------
