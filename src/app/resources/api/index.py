from flask import redirect

from src.app.resources.api import api


@api.route("/", methods=["GET"])
def index():
    return redirect("/apidocs")
