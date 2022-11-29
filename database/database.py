import typing

from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.sql import select, update, delete
from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from . import base


class DataBase:
    __instance = None

    def __new__(cls, *args, **kwars):
        if not cls.__instance:
            cls.__instance = super(DataBase, cls).__new__(cls)
        return cls.__instance

    def __init__(self, link: str) -> None:
        self._engine = create_engine(link)
        self.session = Session(self._engine)

    def add(self, table: base.Table, conflicts: typing.Iterable[str] = None, **kwargs) -> None:
        """
            Adds a new record to the table.

            :param table: Table model.
            :param conflicts: List of columns that use a unique constraint.
        """

        if not isinstance(conflicts, (list, tuple, base.NoneType)):
            conflicts = (conflicts, )

        sql = insert(table).values(**kwargs)
        sql = sql.on_conflict_do_nothing(index_elements=conflicts)

        self.session.execute(sql)
        self.session.commit()

    def get_data(self,
                 table: base.Table, *,
                 conditions: typing.Iterable = None,
                 default: base.Default = None,
                 **kwargs) -> typing.Union[base.Table, base.Default]:
        """
            Get record from database.

            :param table: Table model.
            :param conditions: condition for getting a record.
            :param default: The default value to be returned if there is no record.
        """

        if not isinstance(conditions, (list, tuple, base.NoneType)):
            conditions = (conditions, )

        sql = select(table)

        if conditions:
            sql = sql.filter(*conditions)
        if kwargs:
            sql = sql.filter_by(**kwargs)

        result = self.session.execute(sql)
        return result.scalars().first() or default

    def get_all_data(self,
                     table: base.Table, *,
                     order_by: typing.Iterable = None,
                     conditions: typing.Iterable = None,
                     distinct: typing.Iterable = None,
                     default: base.Default = None,
                     **kwargs) -> typing.Union[typing.List[base.Table], base.Default]:
        """
            Get records from database.

            :param table: Table model.
            :param conditions: Condition for getting a record.
            :param order_by: Sorts entries by. Accepts either asc or desc.
            :param distinct: Used to get unique record. Takes column.
            :param default: The default value to be returned if there is no record. Default list.
        """

        if not isinstance(conditions, (list, tuple, base.NoneType)):
            conditions = (conditions, )
        if not isinstance(order_by, (list, tuple, base.NoneType)):
            order_by = (order_by, )
        if not isinstance(distinct, (list, tuple, base.NoneType)):
            distinct = (distinct, )

        sql = select(table)

        if order_by:
            sql = sql.order_by(*order_by)
        if conditions:
            sql = sql.filter(*conditions)
        if distinct:
            sql = sql.distinct(*distinct)
        if kwargs:
            sql = sql.filter_by(**kwargs)

        result = self.session.execute(sql)
        return result.scalars().all() or default or []

    def counter(self, table: base.Table, **kwargs) -> int:
        """
            Counts the number of records.

            :param table: Table model.
        """

        return len(self.get_all_data(table, **kwargs))

    def update_by_id(self, table: base.Table, _id: int, **kwargs) -> None:
        """
            Updates records by id.

            :param table: Table model.
            :param id: Record Id.
        """

        self.session.execute(update(table).where(table.id == _id).values(kwargs))
        self.session.commit()

    def delete(self, table: base.Table, **kwargs) -> None:
        """
            Removes a record from a table.

            :param table: Table model.
        """

        self.session.execute(delete(table).filter_by(**kwargs))
        self.session.commit()
