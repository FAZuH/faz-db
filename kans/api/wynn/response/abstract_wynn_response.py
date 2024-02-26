from abc import ABC
from typing import TypeVar

from ..model import Headers
from kans.util import ResponseSet

T = TypeVar('T')


class AbstractWynnResponse(ResponseSet[T, Headers], ABC):

    def __repr__(self) -> str:
        return self.__class__.__name__
    #
    # def get_model_type(self) -> Type[T]:
    #     return self.body.__class__
