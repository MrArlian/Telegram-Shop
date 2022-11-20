import datetime
import typing

from sqlalchemy.ext.declarative import declarative_base


DateTime = typing.TypeVar('DateTime', bound=datetime.datetime)
Date = typing.TypeVar('Date', bound=datetime.date)

Dictionary = typing.TypeVar('Dictionary', bound=dict)
Boolean = typing.TypeVar('Boolean', bound=bool)
Integer = typing.TypeVar('Integer', bound=int)
String = typing.TypeVar('String', bound=str)
Float = typing.TypeVar('Float', bound=float)

Default = typing.TypeVar('Default')
Table = typing.TypeVar('Table')

NoneType = type(None)

BaseModel = declarative_base()
