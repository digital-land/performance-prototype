import json

from flask import render_template, Blueprint, current_app
from flask.helpers import url_for

from application.googlesheetscollector import (
    get_datasets,
    get_bfl,
    get_organisations,
    get_esk_datasets,
    get_resource_source_stats,
    get_org_count,
)
from application.filters import clean_int_filter


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


@base.route("/performance")
@base.route("/performance/")
def performance():
    datasets = get_datasets()
    print("DATASETS")
    high_level_numbers = {
        "datasets_with_data": len([d for d in datasets if d["total-resources"] != "0"]),
        "resources": sum([clean_int_filter(d["total-resources"]) for d in datasets]),
    }
    org_count = get_org_count()
    print(org_count)
    return render_template(
        "performance.html",
        info_page=url_for("base.performance_info"),
        datasets=datasets,
        high_level_numbers=high_level_numbers,
        stats=get_resource_source_stats(),
        org_count=org_count.get(
            "Number of organisations we're collecting data from", "?"
        ),
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

    if dataset_name.lower() == "brownfield land":
        withresource, additional, noresource = get_bfl()

        # stats for chart
        resource_stats = {
            "over_one": len([o for o in withresource if int(o["active-resource"]) > 1]),
            "one": len([o for o in withresource if int(o["active-resource"]) == 1]),
            "zero": len(noresource),
        }

        return render_template(
            "dataset/performance.html",
            name=dataset_name,
            info_page=url_for("base.dataset_info", dataset_name=dataset_name),
            dataset=dataset[0] if len(dataset) else "",
            orgs={
                "withresource": withresource,
                "additional": additional,
                "noresource": noresource,
            },
            resource_stats=resource_stats,
        )

    return render_template(
        "dataset/performance.html",
        name=dataset_name,
        info_page=url_for("base.dataset_info", dataset_name=dataset_name),
        dataset=dataset[0] if len(dataset) else "",
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


def get_organisation(id):
    organisations = get_organisations()
    return next(o for o in organisations if o["organisation"] == id)


@base.route("/organisation/<prefix>/<org_id>")
def organisation_performance(prefix, org_id):
    id = prefix + ":" + org_id
    organisation = get_organisation(id)

    if org_id == "ESK":
        datasets = get_esk_datasets()
        no_current = [
            d
            for d in datasets
            if int(d["total-resource"]) > 0 and int(d["active-resource"]) == 0
        ]
        has_current = [
            d
            for d in datasets
            if int(d["total-resource"]) > 0 and int(d["active-resource"]) > 0
        ]
        no_data = [d for d in datasets if int(d["total-resource"]) == 0]
        return render_template(
            "organisation/performance.html",
            organisation=organisation,
            info_page=url_for("base.organisation_info", prefix=prefix, org_id=org_id),
            datasets={
                "current": has_current,
                "nocurrent": no_current,
                "missing": no_data,
            },
        )

    return render_template(
        "organisation/performance.html",
        organisation=organisation,
        info_page=url_for("base.organisation_info", prefix=prefix, org_id=org_id),
    )


@base.route("/organisation/<prefix>/<org_id>/info")
def organisation_info(prefix, org_id):
    data = read_json_file("application/data/info/organisation.json")
    return render_template(
        "info.html",
        page_title="Organisation performance",
        page_url=url_for("base.organisation_performance", prefix=prefix, org_id=org_id),
        data=data,
    )


@base.route("/resource/<resource>")
def resource_performance(resource):
    return render_template(
        "resource/performance.html",
        resource=resource,
        info_page=url_for("base.resource_info", resource=resource),
    )


@base.route("/resource/<resource>/info")
def resource_info(resource):
    data = read_json_file("application/data/info/resource.json")
    return render_template(
        "info.html",
        page_title="Resource performance",
        page_url=url_for("base.resource_performance", resource=resource),
        data=data,
    )
