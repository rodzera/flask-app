from src.app.constants import ABOUT
from src.app.resources.api import api
from src.app.utils.handlers.request import request_validator


@api.route("/about", methods=["GET"])
@request_validator()
def about():
    return ABOUT, 200
