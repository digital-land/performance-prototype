import requests
from flask import Blueprint, jsonify, render_template
from sqlalchemy import func, text, and_

from application.models import Test, TestRun, Result, test_runs

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

    results = (
        db.session.query(
            Test.test.label("test_name"),
            Test.organisation.label("local_authority"),
            Test.dataset,
            Result.path,
            Result.expected,
            Result.actual,
            Result.match,
            func.max(TestRun.created_timestamp).label("last_run"),
        )
        .join(TestRun, Test.test_runs)
        .join(
            Result, and_(Test.test == Result.test_id, TestRun.id == Result.test_run_id)
        )
        .group_by(
            Test.test,
            Test.organisation,
            Test.dataset,
            Result.path,
            Result.expected,
            Result.actual,
            Result.match,
        )
        .all()
    )

    result_by_dataset = {}
    results_by_local_authority = {}
    datasets = set([])
    local_authorities = set([])
    run_date_time = results[0].last_run.strftime("%b %d %Y %H:%M")

    for result in results:
        datasets.add(result.dataset)
        local_authorities.add(result.local_authority)
        if result.dataset not in result_by_dataset:
            result_by_dataset[result.dataset] = [result]
        else:
            result_by_dataset[result.dataset].append(result)
        if result.local_authority not in results_by_local_authority:
            results_by_local_authority[result.local_authority] = [result]
        else:
            results_by_local_authority[result.local_authority].append(result)

    return render_template(
        "ripa_test/index.html",
        result_by_dataset=result_by_dataset,
        results_by_local_authority=results_by_local_authority,
        datasets=datasets,
        local_authorities=local_authorities,
        run_date_time=run_date_time,
    )
