from src.app.logger import get_logger

log = get_logger(__name__)


def query_with_entities(model, *attrs, **kattrs):
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
