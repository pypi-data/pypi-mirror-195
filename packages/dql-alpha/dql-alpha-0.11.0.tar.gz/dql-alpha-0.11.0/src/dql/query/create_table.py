from typing import Optional

from sqlalchemy.ext.compiler import compiles
from sqlalchemy.sql.expression import ClauseElement, Executable


class TableFromQuery(Executable, ClauseElement):  # pylint: disable=abstract-method
    inherit_cache: Optional[bool] = True

    def __init__(self, tbl, query):
        self.tbl = tbl
        self.query = query


@compiles(TableFromQuery)
def _table_from_query(element, compiler, **kw):  # pylint: disable=unused-argument
    return f"CREATE TABLE {element.tbl} AS {compiler.process(element.query)}"
