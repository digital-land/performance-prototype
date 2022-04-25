import re

import requests
from flask.cli import AppGroup
from jsonpath import JSONPath

from application.models import Test, Assertion, TestRun, Result

data_test_cli = AppGroup("data-test")

BASE_API_URL = "https://www.digital-land.info/entity.json"


@data_test_cli.command("run")
def run():
    from application.extensions import db

    tests = db.session.query(Test).all()
    for test in tests:
        test_run = TestRun(test=test)
        test_url = f"{BASE_API_URL}{test.query}"
        resp = requests.get(test_url)
        resp.raise_for_status()
        data = resp.json()
        for a in test.assertions:
            parsed = JSONPath(a.json_path).parse(data)
            if parsed:
                actual = parsed[0]
                match = True if re.match(a.regex, str(actual)) else False
                result = Result(
                    path=a.json_path, expected=a.regex, actual=actual, match=match
                )
            else:
                result = Result(path=a.json_path, expected=a.regex, actual=None)
            test_run.results.append(result)
        db.session.add(test_run)
        db.session.commit()


def _get_result(data, field, expect):
    return Result(expect=expect, actual=getattr(field, data), data=data)


@data_test_cli.command("load")
def load():
    from application.extensions import db
    from application.data_tests.tests import tests

    local_authorities = [
        "local-authority-eng:LBH",
        "local-authority-eng:CAT",
        "local-authority-eng:BUC",
        "local-authority-eng:SWK",
    ]

    for la in local_authorities:
        la_tests = tests[la]
        for name, test in la_tests.items():
            db_test = db.session.query(Test).get(name)
            if db_test is None:
                print(f"Loading test '{name}'")
                print(f"query = {test['query']}")
                print(f"dataset = {test['dataset']}")
                print(f"assertions = {test['assertions']}")
                db_test = Test(
                    test=name,
                    query=test["query"],
                    dataset=test["dataset"],
                    organisation=la,
                )
                for json_path, regex in test["assertions"].items():
                    a = Assertion(json_path=json_path, regex=regex)
                    db_test.assertions.append(a)

                db.session.add(db_test)
                db.session.commit()
            else:
                print(f"Test '{name}' already loaded")
