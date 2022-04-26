import datetime
import re
import uuid

import requests
from flask.cli import AppGroup
from jsonpath import JSONPath

from application.data_tests.tests import local_authorities
from application.models import Test, Assertion, TestRun, Result

data_test_cli = AppGroup("data-test")

BASE_API_URL = "https://www.digital-land.info/entity.json"

@data_test_cli.command("run")
def run():
    from application.extensions import db

    print(f"Running tests at {datetime.datetime.utcnow()}")
    for la in local_authorities:
        tests = db.session.query(Test).filter(Test.organisation == la).all()
        if tests is None:
            continue
        test_run = TestRun()
        for test in tests:
            test_run.tests.append(test)
            test_url = f"{BASE_API_URL}{test.query}"
            resp = requests.get(test_url)
            resp.raise_for_status()
            data = resp.json()
            # TODO - perhaps sort entities on something predictable so
            # that assertions can rely on some ordering?
            for a in test.assertions:
                parsed = JSONPath(a.json_path).parse(data)
                if parsed:
                    actual = parsed[0]
                    match = True if re.match(a.regex, str(actual)) else False
                    result = Result(
                        path=a.json_path,
                        expected=a.regex,
                        actual=actual,
                        match=match,
                        test_id=test.test,
                    )
                else:
                    result = Result(
                        path=a.json_path,
                        expected=a.regex,
                        actual=None,
                        test_id=test.test,
                    )

                test_run.results.append(result)

        db.session.add(test_run)
        db.session.commit()

    print(f"Finished running tests at {datetime.datetime.utcnow()}")


def _get_result(data, field, expect):
    return Result(expect=expect, actual=getattr(field, data), data=data)


@data_test_cli.command("load")
def load():
    from application.extensions import db
    from application.data_tests.tests import tests

    print(f"Loading tests at {datetime.datetime.utcnow()}")

    for la in local_authorities:
        la_tests = tests.get(la, {})
        for name, test in la_tests.items():
            db_test = db.session.query(Test).get(name)
            if db_test is None:
                print(f"Loading test '{name}'")
                print(f"query = {test['query']}")
                print(f"dataset = {test['dataset']}")
                print(f"assertions = {test['assertions']}")
                print(f"ticket = {test.get('ticket', None)}")
                db_test = Test(
                    test=name,
                    query=test["query"],
                    dataset=test["dataset"],
                    organisation=la,
                    ticket=test.get("ticket", None)
                )
                for json_path, regex in test["assertions"].items():
                    a = Assertion(json_path=json_path, regex=regex)
                    db_test.assertions.append(a)

                db.session.add(db_test)
                db.session.commit()
            else:
                db_test.query = test["query"]
                db_test.dataset = test["dataset"]
                db_test.organisation = la
                db_test.ticket = test.get("ticket", None)
                for a in db_test.assertions:
                    db.session.delete(a)
                for json_path, regex in test["assertions"].items():
                    a = Assertion(json_path=json_path, regex=regex)
                    db_test.assertions.append(a)
                print(f"Test '{name}' already loaded. Updating with {test}")

    print(f"Finished loading tests at {datetime.datetime.utcnow()}")
