__all__ = ['Help', 'Type']


from ..base import Base


Help = Base[str].new('help')
Type = Base[str].new('type')
