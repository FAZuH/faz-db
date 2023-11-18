from typing import Optional

import aiohttp


class VindicatorError(Exception):
    """Base error class for all library-related exceptions in this file.
    Essentially, this could be caught to handle any exceptions thrown from this library.
    """

    def __init__(self, message: Optional[str] = None):
        if message:
            message = f"{self.__class__.__doc__}\n{message}"
        else:
            message = self.__class__.__doc__

        super().__init__(message)


class BadRequest(VindicatorError):
    """HTTP 400. The server could not process our request, likely due to an error of ours."""


class Unauthorized(VindicatorError):
    """HTTP 401. We are not authorized to access the requested resource.
    This can occur due to an invalid or expired Bearer token.
    """


class Forbidden(VindicatorError):
    """HTTP 403. We do not have permission to access the requested resource."""


class NotFound(VindicatorError):
    """HTTP 404. This resource does not exist."""


class TooManyRequests(VindicatorError):
    """HTTP 429. The server is ratelimiting us. Please wait for a bit before trying again."""


class ServerError(VindicatorError):
    """HTTP 5xx. The server encountered an unexpected condition that prevented it from fulfilling the request."""
