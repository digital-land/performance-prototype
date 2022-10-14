import pytest


@pytest.fixture(scope="session")
def client():
    from application.factory import create_app

    app = create_app("config.TestConfig")
    client = app.test_client()
    yield client


def test_app(client):

    resp = client.get("/performance/")
    assert 200 == resp.status_code
    assert "Summary" in resp.data.decode("utf-8")

    resp = client.get("/dataset/")
    assert 200 == resp.status_code
    assert "Datasets" in resp.data.decode("utf-8")

    resp = client.get("/organisation/")
    assert 200 == resp.status_code
    assert "Organisations" in resp.data.decode("utf-8")

    resp = client.get("/ripa/")
    assert 200 == resp.status_code
    assert "Test results" in resp.data.decode("utf-8")
