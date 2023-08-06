from typing import Optional

import sqlalchemy
from sqlalchemy import ColumnClause

from dql.catalog import Catalog
from dql.data_storage.sqlite import SQLiteDataStorage
from dql.query.create_table import TableFromQuery


class ColumnMeta(type):
    def __getattr__(cls, name: str):
        return cls(name)


class Column(ColumnClause, metaclass=ColumnMeta):  # pylint: disable=abstract-method
    inherit_cache: Optional[bool] = True

    def __init__(self, text: str) -> None:
        super().__init__(text)

    def glob(self, glob_str):
        return self.op("GLOB")(glob_str)


class Step:
    pass


class SQLFilter(Step):
    def __init__(self, *args, table=None):  # pylint: disable=super-init-not-called
        self.expressions = args
        self.table = table

    def __and__(self, other):
        return self.__class__(*(self.expressions + other), table=self.table)

    def clone(self):
        return self.__class__(*self.expressions, table=self.table)

    def apply(self, _):
        table = self.table
        if table is None:
            raise Exception("table cannot be None when compiling")
        if isinstance(table, str):
            table = sqlalchemy.table(table)
        return sqlalchemy.select("*", table).filter(*self.expressions)


class SQLQuery:
    def __init__(
        self, table: str = "", engine=None
    ):  # pylint: disable=super-init-not-called
        self.engine = engine
        self.steps = []
        if table:
            self.steps.append(SQLFilter(table=table))

    def __iter__(self):
        return iter(self.run())

    def run(self):
        engine = self.engine
        query = None
        for step in self.steps:
            query = step.apply(query)  # a chain of steps linked by results
        with engine.connect() as con:
            result = con.execute(query).fetchall()
        return result

    def clone(self):
        obj = self.__class__()
        obj.engine = self.engine
        obj.steps = self.steps.copy()
        return obj

    def filter(self, *args):
        query = self.clone()
        steps = query.steps
        if steps and isinstance(steps[-1], SQLFilter):
            steps[-1] = steps[-1] & args
        else:
            steps.append(SQLFilter(*args))
        return query

    def save(self, name: str):
        """Save the result of the query as a new table."""
        engine = self.engine
        query = None
        for step in self.steps:
            query = step.apply(query)
        with engine.connect() as con:
            con.execute(TableFromQuery(name, query))


class DatasetQuery(SQLQuery):
    def __init__(self, path: str = "", name: str = "", catalog=None):
        if catalog is None:
            catalog = Catalog(SQLiteDataStorage())
        self.catalog = catalog

        data_storage = catalog.data_storage
        table = ""
        if path:
            # TODO add indexing step
            raise NotImplementedError("path not supported")
        elif name:
            if catalog is None:
                raise ValueError("using name requires catalog")
            table = data_storage._dataset_table_name(data_storage.get_dataset(name).id)
        super().__init__(table=table, engine=data_storage.engine)

    def __iter__(self):
        return iter(self.run())

    def clone(self):
        obj = self.__class__(catalog=self.catalog)
        obj.engine = self.engine
        obj.steps = self.steps.copy()
        return obj

    def save(self, name: str):
        """Save the query as a shadow dataset."""
        self.catalog.data_storage.create_shadow_dataset(name, create_rows=False)
        dataset = self.catalog.data_storage.get_dataset(name)
        # pylint: disable=protected-access
        table_name = self.catalog.data_storage._dataset_table_name(dataset.id)
        super().save(table_name)


C = Column
