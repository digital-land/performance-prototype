from application.wsgi import app


@app.route("/heath")
def heathcheck():
    return {
        "status": "OK",
    }
