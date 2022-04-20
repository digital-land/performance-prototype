import requests
from flask import Blueprint, jsonify

ripa_test = Blueprint("ripa", __name__, url_prefix="/ripa")

BASE_API_URL = "https://www.digital-land.info/entity.json"

params = {"longitude": -0.14650, "latitude": 51.459335, "dataset": "conservation-area"}
expect = {
    "reference": "CA01",
    "name": "Clapham",
    "organisation": "local-authority-eng:LBH",
}


@ripa_test.route("/")
def index():
    resp = requests.get(BASE_API_URL, params=params)
    resp.raise_for_status()
    data = resp.json()
    return jsonify(data)
