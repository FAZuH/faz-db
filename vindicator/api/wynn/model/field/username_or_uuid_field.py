from uuid import UUID


class UsernameOrUuidField:

    def __init__(self, username_or_uuid: str) -> None:
        self._username_or_uuid: str = username_or_uuid
        self._is_uuid: bool = False
        self._username: None | str = None
        self._uuid: None | UUID = None
        try:
            self._uuid = UUID(username_or_uuid)
            self._is_uuid = True
        except ValueError:
            self._username = username_or_uuid

    def __str__(self) -> str:
        return self._username_or_uuid

    def to_bytes(self) -> bytes:
        if self._uuid is None:
            raise ValueError("UUID is None.")
        return self._uuid.bytes

    def is_uuid(self) -> bool:
        return self._is_uuid

    @property
    def username(self) -> None | str:
        """Returns an username if this object is not an uuid else None."""
        return self._username

    @property
    def username_or_uuid(self) -> str:
        return self._username_or_uuid

    @property
    def uuid(self) -> None | UUID:
        """Returns an uuid if this object is an uuid else None."""
        return self._uuid