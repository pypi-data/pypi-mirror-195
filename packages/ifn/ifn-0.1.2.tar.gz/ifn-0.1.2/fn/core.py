__all__ = ['Group']


import collections as c
import typing as t

from .base import Data
from .standard.adapter import Adapter
from .standard.config import Base, Type
from .type import Fa, NestedDict, OptStr, Unknown

if t.TYPE_CHECKING:
    from typing_extensions import Self


class Group:
    '''Group of commands

    Example:
        >>> from fn.standard.adapter import Adapter
        >>> from fn.standard.config import Help, Type
        >>>
        >>> group = Group('test', off=False)
        >>>
        >>> @group.register({
        ...     'char':   Type('str') + Help('todo'),
        ...     'number': Type('int') + Help('todo'),
        ...     'return': Type('str') + Help('todo'),
        ... })
        ... def test(char: str, number: int) -> str:
        ...     return number * char
        >>>
        >>> Group.main(Adapter)
    '''

    __api__ = c.namedtuple('API', ['meta', 'data'])
    __instances__ = {}

    def __init__(self, key: OptStr = None, off: bool = False) -> None:
        self._key = key
        self._off = off
        self._api = {}
        self.__instances__[key] = self

    def __enter__(self) -> 'Self':
        return self

    def __exit__(self, type: Unknown, value: Unknown, traceback: Unknown) -> None:
        pass

    @classmethod
    def main(cls, Adapter: type = Adapter) -> None:
        Adapter(cls.__instances__).main()

    @property
    def api(self) -> t.Dict[str, __api__]:
        return self._api

    def register(self, meta: NestedDict = {}, key: OptStr = None) -> t.Callable[[Fa], Fa]:
        def decorate(func: Fa) -> Fa:
            if not self._off:
                self._register(func, meta, key or func.__name__)
            return func
        return decorate

    def _register(self, func: Fa, meta: NestedDict, key: str) -> None:
        for arg, annotation in func.__annotations__.items():
            if arg not in meta:
                meta[arg] = Data({})
            elif isinstance(meta[arg], dict):
                meta[arg] = Data(meta[arg])
            elif isinstance(meta[arg], Base):
                meta[arg] = Data(meta[arg].as_dict())
            keys = Type._keys()
            if keys not in meta[arg]:
                meta[arg][keys] = self._strize(annotation)
        self._api[key] = self.__api__(meta, func)

    def _strize(self, annotation: object) -> str:
        if isinstance(annotation, type):
            return annotation.__name__
        else:  # typing._GenericAlias
            ans = repr(annotation)
            for old, new in [('typing.', ''), ('NoneType', 'None')]:
                ans = ans.replace(old, new)
            return ans
