from flask import Blueprint, redirect, url_for

views = Blueprint("views", __name__)


@views.route("/", methods=["GET"])
def index():
    return redirect(url_for("flasgger.apidocs"))
