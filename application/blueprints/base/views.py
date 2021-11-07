import json
from datetime import datetime

from flask import render_template, Blueprint, current_app
from flask.helpers import url_for
from flask import request

from application.filters import clean_int_filter, days_since
from application.datasette import (
    sources_with_endpoint,
    datasets_for_an_organisation,
    datasets_by_organistion,
    get_monthly_counts,
    publisher_counts,
    publisher_coverage,
    active_resources,
    sources_by_dataset,
    resources_by_dataset,
    get_source,
    get_datasets_info,
    get_organisation,
    get_datasets_summary,
    get_resource_count,
    total_publisher_coverage,
    content_type_counts,
    resources_of_type,
    get_resources,
    get_resource,
    entry_count,
    get_sources,
    source_count_per_organisation,
    get_datasets,
    get_theme,
    get_typology,
    dataset_latest_logs,
    DLDatasette,
)
from application.utils import (
    resources_per_publishers,
    index_by,
    index_with_list,
    recent_dates,
    read_json_file,
)
from application.enddatechecker import EndDateChecker


base = Blueprint("base", __name__)


@base.context_processor
def set_globals():
    return {"staticPath": "https://digital-land.github.io"}


###################
# Service homepage
###################


@base.route("/")
@base.route("/index")
def index():
    return render_template("index.html")


####################
# Overview dashboard
####################


@base.route("/performance")
@base.route("/performance/")
def performance():
    ds = DLDatasette()
    gs_datasets = get_datasets_summary()
    checker = EndDateChecker()

    return render_template(
        "performance.html",
        info_page=url_for("base.performance_info"),
        datasets=gs_datasets,
        stats=get_monthly_counts(),
        publisher_count=total_publisher_coverage(),
        sources=sources_with_endpoint(),
        entity_count=ds.get_entity_count(),
        datasette_datasets=get_datasets_info(split=True),
        resource_count=get_resource_count(),
        using_enddate=checker.get_count(),
        content_type_counts=content_type_counts(),
        new_resources=ds.get_new_resources(dates=recent_dates(7)),
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


##########
# Datasets
##########


@base.route("/dataset")
def datasets():
    filters = {}
    if request.args.get("active"):
        filters["active"] = request.args.get("active")
    if request.args.get("theme"):
        filters["theme"] = request.args.get("theme")
    if request.args.get("typology"):
        filters["typology"] = request.args.get("typology")

    if len(filters.keys()):
        dataset_records = get_datasets(filter=filters)
    else:
        dataset_records = get_datasets()

    return render_template(
        "dataset/index.html",
        datasets=dataset_records,
        filters=filters,
        filter_btns=filter_off_btns(filters),
        themes=get_theme(),
        typologies=get_typology(),
    )


@base.route("/dataset/<dataset>")
def dataset(dataset):
    ds = DLDatasette()
    datasets = get_datasets_summary()
    dataset_name = dataset
    dataset = [v for k, v in datasets.items() if v.get("pipeline") == dataset]

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

    resource_count = (
        resources_by_dataset(dataset_name)[0]
        if resources_by_dataset(dataset_name)
        else 0
    )

    source_filters = {"documentation_url": "", "pipeline": dataset_name}

    return render_template(
        "dataset/performance.html",
        name=dataset_name,
        info_page=url_for("base.dataset_info", dataset=dataset_name),
        dataset=dataset[0] if len(dataset) else "",
        latest_resource=ds.get_latest_resource(dataset_name),
        monthly_counts=get_monthly_counts(pipeline=dataset_name),
        publishers=publisher_splits,
        today=datetime.utcnow().isoformat()[:10],
        entity_count=ds.get_entity_count(pipeline=dataset_name),
        resource_count=resource_count,
        coverage=publisher_coverage(dataset_name)[0],
        resource_stats=resource_stats,
        sources_no_doc_url=get_sources(filter=source_filters),
        content_type_counts=content_type_counts(dataset_name),
        latest_logs=dataset_latest_logs(),
        blank_sources=ds.get_blank_sources(dataset_name),
        source_count=ds.source_counts(pipeline=dataset_name),
    )


@base.route("/dataset/<dataset>/info")
def dataset_info(dataset):
    data = read_json_file("application/data/info/dataset.json")
    return render_template(
        "info.html",
        page_title=dataset + " performance",
        page_url=url_for("base.dataset_performance", dataset_name=dataset),
        data=data,
    )


############
# Publishers
############


def split_publishers(organisations):
    lpas = {
        publisher: organisations[publisher]
        for publisher in organisations.keys()
        if "local-authority-eng" in publisher
    }
    dev_corps = {
        publisher: organisations[publisher]
        for publisher in organisations.keys()
        if "development-corporation" in publisher
    }
    national_parks = {
        publisher: organisations[publisher]
        for publisher in organisations.keys()
        if "national-park" in publisher
    }
    other = {
        publisher: organisations[publisher]
        for publisher in organisations.keys()
        if not any(
            s in publisher
            for s in ["local-authority", "development-corporation", "national-park"]
        )
    }
    return {
        "Development corporation": dev_corps,
        "National parks": national_parks,
        "Other publishers": other,
        "Local planning authority": lpas,
    }


@base.route("/organisation")
def organisation():
    ds = DLDatasette()
    publishers_with_no_data = {
        k: publisher
        for k, publisher in ds.get_expected_publishers().items()
        if publisher["active"] == 0
    }

    return render_template(
        "organisation/index.html",
        publishers=split_publishers(datasets_by_organistion()),
        today=datetime.utcnow().isoformat()[:10],
        none_publishers=split_publishers(publishers_with_no_data),
    )


@base.route("/organisation/<prefix>/<org_id>")
def organisation_performance(prefix, org_id):
    ds = DLDatasette()
    id = prefix + ":" + org_id
    organisation = get_organisation(id)
    data = datasets_for_an_organisation(id)
    source_counts = ds.get_sources_per_dataset_for_organisation(id)
    checker = EndDateChecker()
    used_enddate, datasets_with_enddate = checker.has_used_enddate(id)
    sources = index_with_list("pipeline", ds.get_all_sources_for_organisation(id))
    missing_datasets = [
        dataset for dataset in source_counts if dataset["sources_with_endpoint"] == 0
    ]

    erroneous_sources = []
    for dataset in data["datasets_covered"]:
        for source in sources[dataset]:
            if source["endpoint"] == "":
                erroneous_sources.append(source)

    return render_template(
        "organisation/performance.html",
        organisation=organisation,
        info_page=url_for("base.organisation_info", prefix=prefix, org_id=org_id),
        data=data,
        sources_per_dataset=source_counts,
        missing_datasets=missing_datasets,
        enddate={"used": used_enddate, "datasets": datasets_with_enddate},
        sources=sources,
        erroneous_sources=erroneous_sources,
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


###########
# Resources
###########


def filter_off_btns(filters):
    # used by all index pages with filter options
    btns = []
    for filter, value in filters.items():
        filters_copy = filters.copy()
        del filters_copy[filter]
        btns.append({"filter": filter, "value": value, "url_params": filters_copy})
    return btns


@base.route("/resource")
def resources():
    filters = {}
    if request.args.get("pipeline"):
        filters["pipeline"] = request.args.get("pipeline")
    if request.args.get("content_type"):
        filters["content_type"] = request.args.get("content_type")
    if request.args.get("organisation"):
        filters["organisation"] = request.args.get("organisation")
    if request.args.get("resource"):
        filters["resource"] = request.args.get("resource")

    resources_per_dataset = index_by("pipeline", resources_by_dataset())

    if len(filters.keys()):
        resource_records = get_resources(filter=filters)
    else:
        resource_records = get_resources()

    return render_template(
        "resource/index.html",
        by_dataset=resources_per_dataset,
        resource_count=get_resource_count(),
        content_type_counts=content_type_counts(),
        datasets=get_datasets_info(split=True),
        resources=resource_records,
        filters=filters,
        filter_btns=filter_off_btns(filters),
        organisations=datasets_by_organistion(),
    )


@base.route("/resource/<resource>")
def resource(resource):
    resource_data = get_resource(resource)
    dataset = resource_data[0]["pipeline"].split(";")[0]
    return render_template(
        "resource/resource.html",
        resource=resource_data,
        info_page=url_for("base.resource_info", resource=resource),
        entry_count=entry_count(dataset, resource)[0],
    )


@base.route("/resource/<resource>/info")
def resource_info(resource):
    data = read_json_file("application/data/info/resource.json")
    return render_template(
        "info.html",
        page_title="Resource performance",
        page_url=url_for("base.resource", resource=resource),
        data=data,
    )


#########
# Sources
#########


def paramify(url):
    # there was a problem if the url to search on included url params
    # this can be avoid if all & are replaced with %26
    url = url.replace("&", "%26")
    # replace spaces (' ' or '%20' ) with %2520 - datasette automatically decoded %20
    url = url.replace(" ", "%2520")
    return url.replace("%20", "%2520")


@base.route("/source")
def sources():
    ds = DLDatasette()
    filters = {}
    if request.args.get("pipeline"):
        filters["pipeline"] = request.args.get("pipeline")
    if request.args.get("organisation") is not None:
        filters["organisation"] = request.args.get("organisation")
    if request.args.get("endpoint_url"):
        filters["endpoint_url"] = paramify(request.args.get("endpoint_url"))
    if request.args.get("endpoint_"):
        filters["endpoint_"] = request.args.get("endpoint_")
    if request.args.get("source"):
        filters["source"] = request.args.get("source")
    if request.args.get("documentation_url") is not None:
        filters["documentation_url"] = request.args.get("documentation_url")

    datasets = sources_by_dataset()
    organisations = source_count_per_organisation()

    if len(filters.keys()):
        source_records = get_sources(filter=filters)
    else:
        source_records = get_sources()

    return render_template(
        "source/index.html",
        by_dataset=datasets,
        counts=ds.source_counts()[0],
        sources=source_records,
        filters=filters,
        filter_btns=filter_off_btns(filters),
        organisations=organisations,
    )


@base.route("/source/<source>")
def source(source):
    source_data = get_source(source)
    return render_template(
        "source/source.html",
        source=source_data[0],
        resources=get_resources(filter={"source": source}),
    )


###############
# Content-types
###############


@base.route("/content-type")
def content_types():
    pipeline = request.args.get("pipeline")

    if pipeline:
        return render_template(
            "content_type/index.html",
            content_type_counts=content_type_counts(pipeline),
            pipeline=pipeline,
        )

    return render_template(
        "content_type/index.html", content_type_counts=content_type_counts()
    )


@base.route("/content-type/<content_type>")
def content_type(content_type):

    return render_template(
        "content_type/type.html",
        content_type=content_type,
        resources=resources_of_type(content_type),
    )


######
# Logs
######


@base.route("/logs")
def logs():
    ds = DLDatasette()

    return render_template(
        "logs/logs.html",
        summary=ds.get_daily_log_summary(),
        resources=ds.get_new_resources(),
    )


@base.route("/logs/<date>")
def log(date):
    ds = DLDatasette()

    return render_template(
        "logs/logs.html",
        summary=ds.get_daily_log_summary(date=date),
        resources=ds.get_new_resources(dates=[date]),
        date=date,
    )
