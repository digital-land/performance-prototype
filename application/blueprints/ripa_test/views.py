from flask import Blueprint, jsonify, render_template
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
    latest_test_run = query.one()

    datasets_tested = set([])
    result_by_dataset = {}
    results_by_local_authority = {}

    for result in latest_test_run.results:
        datasets_tested.add(result.dataset)
        if result.dataset not in result_by_dataset:
            result_by_dataset[result.dataset] = [result]
        else:
            result_by_dataset[result.dataset].append(result)
        if result.organisation not in results_by_local_authority:
            results_by_local_authority[result.organisation] = [result]
        else:
            results_by_local_authority[result.organisation].append(result)

    results_grid = {}
    for la in local_authorities.keys():
        results = results_by_local_authority.get(la, [])
        dataset_results = {}
        for result in results:
            if result.dataset not in dataset_results:
                dataset_results[result.dataset] = [result.match]
            else:
                dataset_results[result.dataset].append(result.match)

        for key, val in dataset_results.items():
            dataset_results[key] = all(val)

        for dataset in datasets_tested:
            if dataset not in dataset_results:
                dataset_results[dataset] = None

        results_grid[la] = dataset_results

    return render_template(
        "ripa_test/index.html",
        results_grid=results_grid,
        local_authorities=local_authorities,
        date_of_test_run=latest_test_run.created_timestamp.strftime('%A %d-%m-%Y, %H:%M:%S')
    )

