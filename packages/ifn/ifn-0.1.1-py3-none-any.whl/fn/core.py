__all__ = ['API', 'Group']


import typing as t

from .config.base import Data
from .config.standard import Base, Type
from .type import Fa, NestedDict, OptStr


class API(t.NamedTuple):
    '''Command api'''

    meta: NestedDict
    data: Fa


class Group:
    '''Group of commands

    Example:
        >>> from fn.config.standard import Help, Type
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
    '''

    def __init__(self, key: OptStr = None, off: bool = False) -> None:
        self._key = key
        self._off = off
        self._api = {}

    @property
    def api(self) -> t.Dict[str, API]:
        return self._api

    def register(self, meta: NestedDict, key: OptStr = None) -> t.Callable[[Fa], Fa]:
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
        self._api[key] = API(meta, func)

    def _strize(self, annotation: object) -> str:
        if isinstance(annotation, type):
            return annotation.__name__
        else:  # typing._GenericAlias
            ans = repr(annotation)
            for old, new in [('typing.', ''), ('NoneType', 'None')]:
                ans = ans.replace(old, new)
            return ans
