__all__ = ['Adapter']


from ..base import Protocol


class Adapter(Protocol):
    '''Adapter'''

    echo = print

    def main(self) -> None:
        cls = self.__class__
        cls.echo(f'meta: {self.group._meta!r}')
        cls.echo(f'func:')
        for name, api in self.group.api.items():
            cls.echo(f'  {name}:')
            cls.echo(f'    args: {api.args!r}')
            cls.echo(f'    meta: {api.meta!r}')
