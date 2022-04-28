import dateutil
from flask import Blueprint, render_template, redirect, url_for
from application.data_tests.tests import local_authorities
from application.models import TestRun

ripa_test = Blueprint("ripa", __name__, url_prefix="/ripa")

BASE_API_URL = "https://www.digital-land.info/entity.json"


@ripa_test.route("/")
def index():
    from application.extensions import db

    subquery = (
        db.session.query(TestRun.id).order_by(TestRun.created_timestamp.desc()).limit(1)
    )
    query = db.session.query(TestRun).filter(TestRun.id.in_(subquery))
    try:
        latest_test_run = query.one()
    except Exception as e:
        return render_template(
            "ripa_test/index.html",
            results_grid=[],
            local_authorities=local_authorities,
            results=[],
        )

    datasets_tested = set([])
    result_by_local_authority = {}

    for result in latest_test_run.results:
        datasets_tested.add(result.dataset)
        if result.organisation not in result_by_local_authority:
            result_by_local_authority[result.organisation] = [result]
        else:
            result_by_local_authority[result.organisation].append(result)

    results_grid = {}
    for la in local_authorities.keys():
        results = result_by_local_authority.get(la, [])
        dataset_results = {}
        for result in results:
            for assertion in result.assertions:
                if result.dataset not in dataset_results:
                    dataset_results[result.dataset] = [assertion.match]
                else:
                    dataset_results[result.dataset].append(assertion.match)

        for key, val in dataset_results.items():
            dataset_results[key] = all(val)

        for dataset in datasets_tested:
            if dataset not in dataset_results:
                dataset_results[dataset] = None

        results_grid[la] = dict(sorted(dataset_results.items()))

    return render_template(
        "ripa_test/index.html",
        results_grid=results_grid,
        local_authorities=local_authorities,
        date_of_test_run=latest_test_run.created_timestamp.astimezone(
            dateutil.tz.gettz("Europe/London")
        ).strftime("%d %B %Y %H:%M:%S"),
        results=latest_test_run.results,
    )


@ripa_test.route("/run-tests")
def run_tests():
    from application.commands import _run_tests

    _run_tests()
    return redirect(url_for("ripa.index"))
