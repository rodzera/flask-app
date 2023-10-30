from flask import Blueprint, redirect

api = Blueprint("api", __name__, url_prefix="/api")

from src.app.resources.api.about import *
from src.app.resources.api.roles import *
from src.app.resources.api.settings import *
from src.app.resources.api.status import *
from src.app.resources.api.users import *


@api.route("/", methods=["GET"])
def index():
    return redirect("/apidocs")
