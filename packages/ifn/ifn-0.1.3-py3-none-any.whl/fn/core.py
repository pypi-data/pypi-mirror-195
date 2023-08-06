__all__ = ['API', 'Group']


import typing as t

from .base import Base, Data
from .standard.adapter import Adapter
from .standard.config import Type
from .type import Fa, BaseOrData, Unknown

if t.TYPE_CHECKING:
    from typing_extensions import Self


class API(t.NamedTuple):
    func: Fa
    args: t.Dict[str, Data]
    meta: Data


class Group:
    '''Group of commands

    Example:
        >>> from fn.standard.adapter import Adapter
        >>> from fn.standard.config import Help, Type
        >>>
        >>> group = Group()
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

    def __init__(self, meta: t.Optional[BaseOrData] = None) -> None:
        self._meta = self._as_data(meta or {})
        self._off = False
        self._api = {}

    def __enter__(self) -> 'Self':
        return self

    def __exit__(self, type: Unknown, value: Unknown, traceback: Unknown) -> None:
        self.off()

    @property
    def api(self) -> t.Dict[str, API]:
        return self._api

    def main(self, adapter: t.Optional[Adapter] = None) -> None:
        if adapter is None:
            adapter = Adapter()
        adapter.setup(self).main()

    def off(self) -> None:
        self._off = True

    def on(self) -> None:
        self._off = False

    def register(
            self,
            args: t.Optional[t.Dict[str, BaseOrData]] = None,
            meta: t.Optional[BaseOrData] = None,
    ) -> t.Callable[[Fa], Fa]:
        assert not self._off

        def decorate(func: Fa) -> Fa:
            self._register(func, args or {}, meta or {})
            return func
        return decorate

    def _register(self, func: Fa, args: t.Dict[str, BaseOrData], meta: BaseOrData) -> None:
        for arg, annotation in func.__annotations__.items():
            if arg not in args:
                args[arg] = Data({})
            else:
                args[arg] = self._as_data(args[arg])
            keys = Type._keys()
            if keys not in args[arg]:
                args[arg][keys] = self._strize(annotation)
        meta = self._as_data(meta)
        if 'name' not in meta:
            meta['name'] = func.__name__
        self._api[meta['name']] = API(func, args, meta)

    def _strize(self, annotation: object) -> str:
        if isinstance(annotation, type):
            return annotation.__name__
        else:  # typing._GenericAlias
            ans = repr(annotation)
            for old, new in [('typing.', ''), ('NoneType', 'None')]:
                ans = ans.replace(old, new)
            return ans

    def _as_data(self, data: t.Union[dict, BaseOrData]) -> Data:
        if isinstance(data, dict):
            return Data(data)
        elif isinstance(data, Base):
            return Data(data.as_dict())
        elif isinstance(data, Data):
            return data
        # raise Exception
