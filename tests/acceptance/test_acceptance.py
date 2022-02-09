import time
import pytest
import uvicorn
from multiprocessing.context import Process

from application.factory import create_app  # noqa: E402

# app = create_app("config.DevelopmentConfig")

HOST = "0.0.0.0"
PORT = 9000
BASE_URL = f"http://{HOST}:{PORT}"

app = create_app("config.DevelopmentConfig")


def run_server():
    app.run(host=HOST, port=PORT, debug=False)


@pytest.fixture(scope="session")
def server_process():
    proc = Process(target=run_server, args=(), daemon=True)
    proc.start()
    time.sleep(10)
    yield proc
    proc.kill()


def test_acceptance(server_process, page):

    page.goto(BASE_URL)
    page.click("text=Browse datasets")
    assert page.url == f"{BASE_URL}/dataset"
