__all__ = ['Adapter']


from ..base import Protocol


class Adapter(Protocol):
    '''Adapter'''

    def main(self) -> None:
        for key, group in self._groups.items():
            print(key)
            for api, data in group.api.items():
                print(' ', api, data.meta)
