import concurrent
import datetime
import re

import requests
from flask.cli import AppGroup
from jsonpath import JSONPath

from application.models import TestRun, Result, ResponseData, Assertion, AssertionType

data_test_cli = AppGroup("data-test")

BASE_API_URL = "https://www.digital-land.info/entity.json"


@data_test_cli.command("run")
def run():
    _run_tests()


def _run_tests():
    from application.extensions import db
    from application.data_tests.tests import tests, local_authorities

    print(f"Running tests at {datetime.datetime.utcnow()}")
    results = []
    for local_authority in local_authorities:
        results.extend(_run_tests_for_local_authority(local_authority, tests))

    test_run = TestRun(results=results)
    db.session.add(test_run)
    db.session.commit()

    print(f"Finished running tests at {datetime.datetime.utcnow()}")


def _run_tests_for_local_authority(local_authority, tests):
    results = []
    test_names = []
    test_details = []
    for test_name, details in tests[local_authority].items():
        test_names.append(test_name)
        test_details.append(details)
    local_authority_names = [local_authority]*len(test_names)

    with concurrent.futures.ThreadPoolExecutor() as executor:
        for result in executor.map(_run_single_test, local_authority_names, test_names, test_details):
            results.extend(result)
        executor.shutdown()

    return results


def _run_single_test(local_authority, test_name, details):
    print(f"Running test: {test_name}")
    results = []
    dataset = details.get("dataset")
    query = details.get("query")
    assertions = details.get("assertions", {})
    warnings = details.get("warnings", {})
    ticket = details.get("ticket")
    checks = {"strict": assertions, "warning": warnings}
    test_url = f"{BASE_API_URL}{query}"
    try:
        resp = requests.get(test_url)
        resp.raise_for_status()
    except Exception as e:
        print(e)
        return results
    data = resp.json()
    # sort by entity id to give tests a predicable ordering
    if data["count"] > 1 and data.get("entities"):
        data["entities"].sort(key=lambda e: e["entity"])
    response_data = ResponseData(query=query, test_name=test_name, data=data)
    result = Result(
        query=query,
        organisation=local_authority,
        dataset=dataset,
        test_name=test_name,
        ticket=ticket,
    )
    response_data.results.append(result)
    results.append(result)
    for level, checks in checks.items():
        for path, expected in checks.items():
            print(f"path = {path} expect = {expected} : check {level}")
            parsed = JSONPath(path).parse(data)
            assertion_type = AssertionType(level)
            if parsed:
                actual = str(parsed[0])
                expected = str(expected)
                if expected.startswith("~"):
                    match = True if re.match(expected[1:], actual) else False
                else:
                    match = expected == actual
                assertion = Assertion(
                    path=path,
                    expected=expected,
                    actual=actual,
                    match=match,
                    assertion_type=assertion_type,
                )
            else:
                assertion = Assertion(
                    path=path,
                    expected=expected,
                    actual=None,
                    match=None,
                    assertion_type=assertion_type,
                )
            result.assertions.append(assertion)

    return results


@data_test_cli.command("delete-old-tests")
def delete_old_tests():
    from application.extensions import db
    from datetime import datetime, timedelta

    now = datetime.now()
    yesterday = now - timedelta(days=1)

    tests_runs_to_delete = (
        db.session.query(TestRun).filter(TestRun.created_timestamp < yesterday).all()
    )

    for t in tests_runs_to_delete:
        print(f"Deleting test from {t.created_timestamp}")
        db.session.delete(t)
    db.session.commit()
