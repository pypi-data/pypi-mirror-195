__all__ = ['Argument', 'Flag', 'Number', 'Required']


from ...base import Base


Argument = Base[bool].new('click.argument', default=True)
Flag = Base[bool].new('click.flag', default=True)
Number = Base[int].new('click.number', default=1)
Required = Base[bool].new('click.required', default=True)
