import json
from datetime import datetime

from flask import render_template, Blueprint, current_app
from flask.helpers import url_for
from flask import request

from application.filters import clean_int_filter
from application.datasette import (
    sources_with_endpoint,
    datasets_for_an_organisation,
    datasets_by_organistion,
    total_entities,
    sources_per_dataset_for_organisation,
    latest_resource,
    get_monthly_counts,
    publisher_counts,
    entity_count,
    publisher_coverage,
    active_resources,
    active_datasets,
    sources_by_dataset,
    resources_by_dataset,
    get_source,
    datasets,
    get_organisation,
    get_datasets_summary,
    get_resource_count,
)
from application.utils import resources_per_publishers


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
    gs_datasets = get_datasets_summary()

    return render_template(
        "performance.html",
        info_page=url_for("base.performance_info"),
        datasets=gs_datasets,
        stats=get_monthly_counts(),
        org_count=len(datasets_by_organistion().keys()),
        sources=sources_with_endpoint(),
        entity_count=total_entities(),
        datasette_datasets=datasets(split=True),
        resource_count=get_resource_count(),
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


@base.route("/dataset")
def dataset():
    datasets = active_datasets()
    return render_template("dataset/index.html", datasets=datasets)


@base.route("/dataset/<dataset_name>")
def dataset_performance(dataset_name):
    datasets = get_datasets_summary()
    # name = dataset_name.replace("_", " ").capitalize()
    dataset = [v for k, v in datasets.items() if v.get("pipeline") == dataset_name]

    resources_by_publisher = resources_per_publishers(active_resources(dataset_name))

    publishers = publisher_counts(dataset_name)
    publisher_splits = {"active": [], "noactive": []}
    for k, publisher in publishers.items():
        if publisher["active_resources"] == 0:
            publisher_splits["noactive"].append(publisher)
        else:
            publisher_splits["active"].append(publisher)

    # for the active resource charts
    resource_stats = {
        "over_one": len(
            [p for p in resources_by_publisher if len(resources_by_publisher[p]) > 1]
        ),
        "one": len(
            [p for p in resources_by_publisher if len(resources_by_publisher[p]) == 1]
        ),
        "zero": len(publisher_splits["noactive"]),
    }

    return render_template(
        "dataset/performance.html",
        name=dataset_name,
        info_page=url_for("base.dataset_info", dataset_name=dataset_name),
        dataset=dataset[0] if len(dataset) else "",
        latest_resource=latest_resource(dataset_name),
        monthly_counts=get_monthly_counts(pipeline=dataset_name),
        publishers=publisher_splits,
        today=datetime.utcnow().isoformat()[:10],
        entity_count=entity_count(dataset_name),
        coverage=publisher_coverage(dataset_name)[0],
        resource_stats=resource_stats,
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


@base.route("/organisation")
def organisation():
    dataset_counts_by_organisations = datasets_by_organistion()

    lpas = {
        publisher: dataset_counts_by_organisations[publisher]
        for publisher in dataset_counts_by_organisations.keys()
        if "local-authority-eng" in publisher
    }
    dev_corps = {
        publisher: dataset_counts_by_organisations[publisher]
        for publisher in dataset_counts_by_organisations.keys()
        if "development-corporation" in publisher
    }
    national_parks = {
        publisher: dataset_counts_by_organisations[publisher]
        for publisher in dataset_counts_by_organisations.keys()
        if "national-park" in publisher
    }
    other = {
        publisher: dataset_counts_by_organisations[publisher]
        for publisher in dataset_counts_by_organisations.keys()
        if not any(
            s in publisher
            for s in ["local-authority", "development-corporation", "national-park"]
        )
    }
    return render_template(
        "organisation/index.html",
        publishers={
            "Development corporation": dev_corps,
            "National parks": national_parks,
            "Other publishers": other,
            "Local planning authority": lpas,
        },
        today=datetime.utcnow().isoformat()[:10],
    )


@base.route("/organisation/<prefix>/<org_id>")
def organisation_performance(prefix, org_id):
    id = prefix + ":" + org_id
    organisation = get_organisation(id)
    data = datasets_for_an_organisation(id)
    source_counts = sources_per_dataset_for_organisation(id)

    return render_template(
        "organisation/performance.html",
        organisation=organisation,
        info_page=url_for("base.organisation_info", prefix=prefix, org_id=org_id),
        data=data,
        sources_per_dataset=source_counts,
        has_missing_datasets=any(
            dataset["sources_with_endpoint"] == 0 for dataset in source_counts
        ),
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


@base.route("/source")
def sources():
    pipeline = request.args.get("pipeline")
    datasets = sources_by_dataset()

    stats = {
        "active": sum(
            [d["active_sources"] for d in datasets if d["active_sources"] > 0]
        ),
        "inactive": sum([d["ended_sources"] for d in datasets]),
        "datasets": len([d for d in datasets if d["active_sources"] > 0]),
    }

    if pipeline:
        sources = sources_by_dataset(pipeline)
        return render_template(
            "source/index.html",
            by_dataset=datasets,
            stats=stats,
            sources=sources,
            pipeline=pipeline,
        )

    return render_template("source/index.html", by_dataset=datasets, stats=stats)


@base.route("/source/<source>")
def source(source):
    source_data = get_source(source)
    return render_template("source/source.html", source=source_data[0])


@base.route("/resource")
def resource():
    datasets = resources_by_dataset()

    return render_template("resource/index.html", by_dataset=datasets)
