from flask import Blueprint

ripa_test = Blueprint("ripa", __name__, url_prefix="/ripa")


@ripa_test.route("/")
def index():
    return "OK"
