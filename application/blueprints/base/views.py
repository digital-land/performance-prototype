import json

from flask import render_template, Blueprint, current_app
from flask.helpers import url_for

from application.googlesheetscollector import get_datasets


base = Blueprint("base", __name__)


@base.context_processor
def set_globals():
    return {"staticPath": "https://digital-land.github.io"}


def read_json_file(data_file_path):
    f = open(
        data_file_path,
    )
    data = json.load(f)
    f.close()
    return data


@base.route("/")
@base.route("/index")
def index():
    return render_template("index.html")


def clean_int(s):
    s = s.replace(",", "")
    return int(s)


@base.route("/performance")
def performance():
    datasets = get_datasets()
    print("DATASETS")
    high_level_numbers = {
        "datasets_with_data": len([d for d in datasets if d["total-resources"] != "0"]),
        "resources": sum([clean_int(d["total-resources"]) for d in datasets]),
    }
    print("hello", high_level_numbers)
    return render_template(
        "performance.html",
        info_page=url_for("base.performance_info"),
        datasets=datasets,
        high_level_numbers=high_level_numbers,
    )


@base.route("/performance/info")
def performance_info():
    data = read_json_file("application/data/info/performance.json")
    return render_template(
        "info.html",
        page_title="Digital land team performance",
        page_url=url_for("base.performance"),
        data=data,
    )


@base.route("/dataset/<dataset_name>")
def dataset_performance(dataset_name):
    datasets = get_datasets()
    name = dataset_name.replace("_", " ").capitalize()
    dataset = [
        d for d in datasets if d["name"] == dataset_name.replace("_", " ").capitalize()
    ]
    return render_template(
        "dataset/performance.html",
        name=dataset_name,
        info_page=url_for("base.dataset_info", dataset_name=dataset_name),
        dataset=dataset,
    )


@base.route("/dataset/<dataset_name>/info")
def dataset_info(dataset_name):
    data = read_json_file("application/data/info/dataset.json")
    return render_template(
        "info.html",
        page_title=dataset_name + " performance",
        page_url=url_for("base.dataset_performance", dataset_name=dataset_name),
        data=data,
    )


@base.route("/organisation/<organisation>/performance")
def organisation_performance(organisation):
    return render_template("organisation/performance.html", organisation=organisation)


@base.route("/resource/<resource>/performance")
def resource_performance(resource):
    return render_template("resource/performance.html", resource=resource)
