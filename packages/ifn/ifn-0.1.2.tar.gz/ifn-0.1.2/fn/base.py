__all__ = ['Data', 'Base', 'Item', 'Protocol']


import copy
import functools as f
import typing as t

from .type import Ta, Tb, Groups, Keys, NestedDict, NestedItem, NestedKeys, NestedValue, OptStr

if t.TYPE_CHECKING:
    from typing_extensions import Self


class Data(t.Generic[Ta]):
    '''
    Example:
        >>> data = Data({'a': {'b': {'c': -1, 'd': 0, 'e': 1}}})
        >>> for keys, value in data.items():
        ...     print(keys, value)
        ('a', 'b', 'c') -1
        ('a', 'b', 'd') 0
        ('a', 'b', 'e') 1
    '''

    def __init__(self, data: NestedDict[Ta]) -> None:
        self._data = data

    def __repr__(self) -> str:
        return self._data.__repr__()

    def __contains__(self, keys: Keys[str]) -> bool:
        if isinstance(keys, str):
            return self._data.__contains__(keys)
        else:  # tuple
            ans = self._data
            for key in keys:
                if not isinstance(ans, dict):
                    return False
                if key in ans:
                    ans = ans[key]
                else:
                    return False
            return True

    def __getitem__(self, keys: Keys[str]) -> NestedValue:
        if isinstance(keys, str):
            return self._data[keys]
        else:  # tuple
            ans = self._data
            for key in keys:
                ans = ans[key]
            return ans

    def __setitem__(self, keys: Keys[str], value: Ta) -> None:
        if isinstance(keys, str):
            self._data[keys] = value
        else:  # tuple
            assert keys

            ans = self._data
            *init, last = keys
            for key in init:
                ans = ans.setdefault(key, {})
            ans[last] = value

    def as_dict(self) -> NestedDict[Ta]:
        return self._data

    def copy(self, deep: bool = False) -> 'Self':
        return self.__class__(copy.deepcopy(self._data) if deep else self._data.copy())

    def get(self, *keys: str) -> t.Optional[NestedValue]:
        try:
            return self.__getitem__(keys)
        except Exception:
            return None

    def items(self) -> t.Iterator[NestedItem]:
        yield from self._items(self._data)

    def _items(self, data: NestedValue, *keys: str) -> t.Iterator[NestedItem]:
        if isinstance(data, dict):
            for key, value in data.items():
                yield from self._items(value, *keys, key)
        else:
            yield keys, data


class Base(t.Generic[Ta]):
    '''
    Example:
        >>> Type = Base.new('type')
        >>> Default = Base.new('default')
        >>> Help = Base.new('help')
        >>> data = Type(str) + Default('hello world!') + Help('documentation')
        >>> print(data)
        {'default': 'hello world!', 'type': <class 'str'>, 'help': 'documentation'}
    '''

    __key__: str = 'default'
    __sep__: str = '.'

    def __init__(self, value: Ta) -> None:
        self._value = value

    def __repr__(self) -> str:
        return f'<{self.__key__} => {self._value}>'

    def __add__(self, other: t.Union[Data[Tb], 'Self']) -> Data[t.Union[Ta, Tb]]:
        if isinstance(other, Data):
            other = other.copy(deep=True)
        else:  # Self
            other = Data(other.as_dict())
        other[self._keys()] = self._value
        return other

    def __radd__(self, other: t.Union[Data[Tb], 'Self']) -> Data[t.Union[Ta, Tb]]:
        return self.__add__(other)

    @classmethod
    @f.lru_cache(maxsize=None)
    def new(cls, key: str, sep: OptStr = None) -> 'Self':
        name = ''.join(map(str.capitalize, cls._keys(key)))
        return type(name, (cls, ), {'__key__': key, '__sep__': sep or cls.__sep__})

    def as_dict(self) -> t.Dict[str, Ta]:
        ans = self._value
        for key in reversed(self._keys()):
            ans = {key: ans}
        return ans

    @classmethod
    def _keys(cls, key: OptStr = None) -> NestedKeys:
        return tuple((key or cls.__key__).split(cls.__sep__))


class Item(t.Generic[Ta]):
    '''
    Example:
        >>> data = Item('type', str) + Item('default', 'hello world!')
        >>> print(data)
        {'default': 'hello world!', 'type': <class 'str'>}
    '''

    def __new__(cls, key: str, value: Ta, sep: OptStr = None) -> Base[Ta]:
        return Base.new(key, sep)(value)


class Protocol:
    '''Adapter protocol'''
    
    def __init__(self, groups: Groups) -> None:
        self._groups = groups

    @property
    def groups(self) -> Groups:
        return self._groups

    def main(self) -> None:
        raise NotImplementedError
