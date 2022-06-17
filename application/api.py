from application.wsgi import app


@app.route("/health")
def healthcheck():
    return {
        "status": "OK",
    }
