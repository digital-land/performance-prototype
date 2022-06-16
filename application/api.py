from application.wsgi import app


@app.route("/health")
def heathcheck():
    return {
        "status": "OK",
    }
