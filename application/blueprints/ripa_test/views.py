import requests
from flask import Blueprint, jsonify, render_template

from application.models import Test

ripa_test = Blueprint("ripa", __name__, url_prefix="/ripa")

BASE_API_URL = "https://www.digital-land.info/entity.json"


# TODO this is a quick hack to get something into page. The model is wrong and this is not the way we'll specify
# test cases or expectations longer term. I reckon move to a db and then we can also offer way to author/modify tests.

params = {"longitude": -0.14650, "latitude": 51.459335, "dataset": "conservation-area"}
expected = {
    "reference": "CA01",
    "name": "Clapham",
    "organisation": "local-authority-eng:LBH",
}

tests_by_local_authority = {
    "local-authority-eng:LBH": [
        {
            "dataset": "conservation-area",
            "tests": [{"params": params, "expected": expected}],
        }
    ]
}

local_authorities = ["local-authority-eng:LBH"]
datasets = ["conservation-area"]

from application.extensions import db

q = "?longitude=-0.14650&latitude=51.459335&dataset=conservation-area"


@ripa_test.route("/")
def index():

    test = (
        db.session.query(Test)
        .filter(
            Test.query == q,
            Test.dataset == "conservation-area",
            Test.organisation == "local-authority-eng:LBH",
        )
        .all()
    )
    if not test:
        test = Test(
            test="Clapham Common Conservation area",
            query=q,
            dataset="conservation-area",
            organisation="local-authority-eng:LBH",
        )
        db.session.add(test)
        db.session.commit()

    else:
        test = test[0]
    query = test.query

    test_url = f"{BASE_API_URL}{query}"
    resp = requests.get(test_url)
    resp.raise_for_status()
    data = resp.json()

    print(data)

    # results_by_local_authority = {}
    # for local_authority in tests_by_local_authority:
    #     test_cases = tests_by_local_authority.get(local_authority, [])
    #     for test_case in test_cases:
    #         test_results = []
    #         for test in test_case["tests"]:
    #             resp = requests.get(BASE_API_URL, params=test["params"])
    #             resp.raise_for_status()
    #             data = resp.json()
    #             entities = data.get("entities")
    #             result = []
    #             for entity in entities:
    #                 res = {}
    #                 for key, _ in expected.items():
    #                     res[key] = entity.get(key)
    #                 result.append(res)
    #             test_results.append({"test": test, "result": result, "data": data})
    #     results_by_local_authority[local_authority] = test_results
    return render_template("ripa_test/index.html", results=[], local_authorities=[])
