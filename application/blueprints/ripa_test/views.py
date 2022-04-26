import requests
from flask import Blueprint, jsonify, render_template
from sqlalchemy import func, text, and_

from application.data_tests.tests import local_authorities, datasets
from application.models import Test, TestRun, Result, test_runs

ripa_test = Blueprint("ripa", __name__, url_prefix="/ripa")

BASE_API_URL = "https://www.digital-land.info/entity.json"


@ripa_test.route("/")
def index():
    from application.extensions import db

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

    if not results:
        return jsonify({})

    result_by_dataset = {}
    results_by_local_authority = {}

    run_date_time = results[0].last_run.strftime("%b %d %Y %H:%M")

    for result in results:
        if result.dataset not in result_by_dataset:
            result_by_dataset[result.dataset] = [result]
        else:
            result_by_dataset[result.dataset].append(result)
        if result.local_authority not in results_by_local_authority:
            results_by_local_authority[result.local_authority] = [result]
        else:
            results_by_local_authority[result.local_authority].append(result)

    # maybe another way of looking at it
    results_grid = {}
    for la in local_authorities:
        results = results_by_local_authority.get(la, [])
        dataset_results = {}
        for result in results:
            if result.dataset not in dataset_results:
                dataset_results[result.dataset] = [result.match]
            else:
                dataset_results[result.dataset].append(result.match)

        for key, val in dataset_results.items():
            dataset_results[key] = all(val)

        for dataset in datasets:
            if dataset not in dataset_results:
                dataset_results[dataset] = None

        results_grid[la] = dataset_results

    # return render_template(
    #     "ripa_test/index.html",
    #     results_grid=results_grid,
    #     datasets=datasets,
    #     local_authorities=local_authorities,
    #     run_date_time=run_date_time,
    # )

    return jsonify(results_grid)
