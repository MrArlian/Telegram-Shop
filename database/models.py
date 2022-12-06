from sqlalchemy.schema import Column
from sqlalchemy import types
from sqlalchemy import func

from . import base


class User(base.BaseModel):

    __tablename__ = 'users'

    id: base.Integer = Column(types.BigInteger, nullable=False, primary_key=True)
    role: base.String = Column(types.String, default='user')

class Product(base.BaseModel):

    __tablename__ = 'products'

    id: base.Integer = Column(types.BigInteger, nullable=False, primary_key=True)
    name: base.String = Column(types.String, nullable=False)
    price: base.Float = Column(types.Float, nullable=False)
    category: base.String = Column(types.String, nullable=False)
    description: base.String = Column(types.String, default='')
    media_link: base.String = Column(types.String, default='')
    file_link: base.String = Column(types.String, default='')


class Transaction(base.BaseModel):

    __tablename__ = 'transactions'

    id: base.Integer = Column(types.BigInteger, nullable=True, primary_key=True)
    user_id: base.Integer = Column(types.Integer, nullable=True)
    product_id: base.Integer = Column(types.Integer, nullable=True)
    path: base.String = Column(types.String, default='')
    date: base.DateTime = Column(types.DateTime, default=func.now())
    platform: base.String = Column(types.String, default='telegram')
    status: base.String = Column(types.String, default='wait')
