__all__ = [
    'Fa', 'Fb', 'Ta', 'Tb', 'Tc',
    'BaseOrData', 'Keys', 'NestedDict', 'NestedItem', 'NestedKeys', 'NestedValue', 'OptStr', 'TupleSeq', 'Unknown',
    'ModuleType', 'NoneType',
]


import typing as t

if t.TYPE_CHECKING:
    from .base import Base, Data


Fa, Fb = t.TypeVar('Fa', bound=t.Callable), t.TypeVar('Fb', bound=t.Callable)
T0 = t.TypeVar('T0')
Ta, Tb, Tc = t.TypeVar('Ta'), t.TypeVar('Tb'), t.TypeVar('Tc')

BaseOrData = t.Union['Base', 'Data']
TupleSeq = t.Tuple[T0, ...]
Keys = t.Union[T0, TupleSeq[T0]]
NestedDict = t.Dict[str, t.Union[T0, 'NestedDict[T0]']]
NestedKeys = TupleSeq[str]
NestedItem = t.Tuple[NestedKeys, T0]
NestedValue = t.Union[T0, NestedDict[T0]]
OptStr = t.Optional[str]
Unknown = t.Any

ModuleType = type(t)
NoneType = type(None)
