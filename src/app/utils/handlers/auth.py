from functools import wraps
from flask import request, abort, current_app

from src.app.logger import get_logger
from src.app.models.users import User

log = get_logger(__name__)

__all__ = ["authenticate", "api_auth"]


def authenticate(username, password):
    log.debug(f"Validating credentials for user '{username}'")

    if username == current_app.config["ADMIN_USER"] and password == current_app.config["ADMIN_PASS"]:
        log.debug("Super admin authenticated")
        return ["admin"]

    user = User.query.filter_by(username=username).first()
    if user and user.check_password(password):
        log.debug(f"User {username} authenticated")
        return [role.name for role in user.roles]

    log.debug(f"Not found any user with username '{username}'")
    return False


def api_auth(roles=None):
    if roles is None:
        roles = ["admin"]

    def decorator(func):
        @wraps(func)
        def wrap(*args, **kwargs):
            log.info(f"Authentication required called: {request.endpoint}")
            auth = request.authorization
            if not auth or not hasattr(auth, "username") or not hasattr(auth, "password"):
                log.debug("Invalid authorization in headers")
                abort(401)

            if not (user_roles := authenticate(auth.username, auth.password)):
                log.error("Invalid credentials to access this resource")
                abort(401)

            if len(roles) > 0 and not any([r in roles for r in user_roles]):
                log.error(f"User '{auth.username}' is not authorized to access this resource")
                abort(401)
            return func(*args, **kwargs)
        return wrap
    return decorator
