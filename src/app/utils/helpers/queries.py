from typing import Tuple, Union
from sqlalchemy import text, exc

from src.app.factory import db, get_logger

log = get_logger(__name__)

__all__ = ["get_db_timestamp", "query_with_entities"]


def get_db_timestamp() -> Union[str, bool]:
    log.info("Querying db current timestamp")
    try:
        with db.engine.connect() as conn:
            query = conn.execute(text("SELECT CURRENT_TIMESTAMP"))
            result = [row[0] for row in query]
            log.info(f"Query result: {result}")
        return result[0].strftime("%Y-%m-%d %H:%M:%S")
    except exc.OperationalError as e:
        log.error(f"Error fetching db current timestamp: {e}")
        return False


def query_with_entities(model, *attrs, **kattrs) -> Union[Tuple, bool]:
    """
    Query a given model using the "with_entities" and "filter_by" functions.

    :param model: A SQLAlchemy model.
    :param attrs: Attributes to be searched and returned.
    :param kattrs: Attributes to be filtered.
    :return: A tuple with the following attributes values if matched.

    """
    log.debug(f"Table to be queried with func 'with_entities': {model.__tablename__.upper()}")
    log.debug(f"Attributes to be returned: {attrs}")
    if not attrs:
        return False

    attrs = tuple(getattr(model, attr) for attr in attrs)
    if not kattrs:
        return model.query.with_entities(*attrs)
    log.debug(f"Filters to be applied in query: {kattrs}")
    return model.query.with_entities(*attrs).filter_by(**kattrs)
