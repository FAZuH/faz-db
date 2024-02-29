from uuid import UUID


class UsernameOrUuidField:
    """For API response fields that can be either an username or an uuid."""

    def __init__(self, username_or_uuid: str) -> None:
        self._username_or_uuid: str = username_or_uuid

        self._username: None | str = None
        self._uuid: None | UUID = None

        self._is_uuid: bool = False
        try:
            self._uuid = UUID(username_or_uuid)
            self._is_uuid = True
        except ValueError:
            self._username = username_or_uuid

    def __str__(self) -> str:
        return self._username_or_uuid

    def is_uuid(self) -> bool:
        """If the passed field is a valid UUID."""
        return self._is_uuid

    @property
    def username_or_uuid(self) -> str:
        """Returns the username or uuid as a string."""
        return self._username_or_uuid
