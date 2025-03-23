from typing import Any, Dict, Optional


class CraftyServerStats:
    def __init__(
        self,
        running: bool,
        server_port: int,
        online: int,
        icon: Optional[str],
        version: Optional[str],
    ) -> None:
        self.running: bool = running
        self.server_port: int = server_port
        self.online: int = online
        self.icon: Optional[str] = icon
        self.version: str = version

    @staticmethod
    def _validate_version(value: Any) -> Optional[str]:
        """
        Validates the version value.
        If the version is None, an empty string, "False", or False, return None.
        Otherwise, return it as a string.
        """
        if value in (None, "", "False", False):
            return None
        return str(value)

    @staticmethod
    def _validate_icon(value: Any) -> Optional[str]:
        """
        Validates the icon value.
        If the icon is None, an empty string, "False", or False, return None.
        Otherwise, return it as a string (assumed to be a base64 encoded string).
        """
        if value in (None, "", "False", False):
            return None
        return str(value)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "CraftyServerStats":
        """
        Create a ServerStats instance from a dictionary.
        It only extracts the properties used in equality:
        'running', 'server_port', 'online', 'icon', and 'version'.
        """
        return cls(
            running=data.get("running", False),
            server_port=data.get("server_port", 0),
            online=data.get("online", 0),
            icon=cls._validate_icon(data.get("icon")),
            version=cls._validate_version(data.get("version")),
        )

    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, CraftyServerStats):
            return NotImplemented
        return (
            self.running == other.running
            and self.server_port == other.server_port
            and self.online == other.online
            and self.icon == other.icon
            and self.version == other.version
        )

    def __repr__(self):
        return (
            f"ServerStats(running={self.running}, "
            f"server_port={self.server_port}, online={self.online}, "
            f"icon={self.icon}, version='{self.version}')"
        )
