__all__ = ['Default', 'Help', 'Name', 'Type', 'Version']


from ..base import Base
from ..type import Ta


Default = Base[Ta].new('default')
Help = Base[str].new('help')
Name = Base[str].new('name')
Type = Base[str].new('type')
Version = Base[str].new('version')
