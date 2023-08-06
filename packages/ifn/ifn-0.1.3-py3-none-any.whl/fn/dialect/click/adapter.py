__all__ = ['Adapter']


import typing as t

from click.decorators import argument, group, option
from click.utils import echo

from ...base import Data, Protocol
from ...type import Fa, Fb

if t.TYPE_CHECKING:
    from typing_extensions import ParamSpec

    P = ParamSpec('P')


class Adapter(Protocol):
    '''Adapter for click'''

    echo = echo

    def main(self) -> None:
        cli = group(lambda: None)
        for name, api in self._group.api.items():
            callback = self._callback(api.func)
            for arg, data in api.args.items():
                if arg == 'return':
                    continue
                func = self._argument if data.get('click', 'argument', default=False) else self._option
                callback = func(arg, data)(callback)
            cli.command(name, help=api.meta.get('help', default=None))(callback)
        cli()

    def _callback(self, func: Fa) -> Fb:
        cls = self.__class__
        def decorate(*args: 'P.args', **kwargs: 'P.kwargs') -> None:
            ans = func(*args, **kwargs)
            if ans is not None:
                cls.echo(ans)
        return decorate

    def _argument(self, arg: str, data: Data) -> Fa:
        return argument(
            arg,
            nargs=data.get('click', 'number', default=1),
            default=data.get('default', default=None),
            required=data.get('click', 'required', default=False),
            type=self._type(data['type']),
        )

    def _option(self, arg: str, data: Data) -> Fa:
        arg = arg.replace('_', '-')
        return option(
            f'--{arg}',
            default=data.get('default', default=None),
            help=data.get('help', default=None),
            type=self._type(data['type']),
        )

    def _type(self, expr: str) -> type:
        return {
            'str': str, 'int': int, 'float': float,
            'List[str]': str, 'List[int]': int, 'List[float]': float,
        }[expr]
