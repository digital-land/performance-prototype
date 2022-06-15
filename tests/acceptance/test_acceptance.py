import time
import pytest
from multiprocessing.context import Process

from application.factory import create_app  # noqa: E402

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
    page.click("text=Browse overview")
    assert page.url == f"{BASE_URL}/performance/"

    page.click("text=Datasets")
    assert page.url == f"{BASE_URL}/dataset/"
    assert page.text_content("h1") == "Datasets"

    page.click(".app-card__title a:text('Brownfield land')")
    assert page.url == f"{BASE_URL}/dataset/brownfield-land"
    assert page.text_content("h1") == "Brownfield land"

    page.click("text=Publishers")
    assert page.url == f"{BASE_URL}/organisation/"
    assert page.text_content("h1") == "Publishers"

    page.click("[data-org-id='local-authority-eng:LBH'] a")
    assert page.url == f"{BASE_URL}/organisation/local-authority-eng/LBH"

    page.click("text=Sources")
    assert page.url == f"{BASE_URL}/source"
    assert page.text_content("h1") == "Sources"

    page.click("text=Resources")
    assert page.url == f"{BASE_URL}/resource"
    assert page.text_content("h1") == "Resources"
