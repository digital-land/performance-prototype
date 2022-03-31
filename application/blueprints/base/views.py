from urllib.parse import unquote

from flask import render_template, Blueprint, redirect
from flask.helpers import url_for
from flask import request

from application.datasette import (
    get_monthly_counts,
    get_datasets_summary,
    DLDatasette,
)
from application.data_access.entity_queries import (
    fetch_entity_count,
    fetch_organisation_entities_using_end_dates,
)
from application.data_access.digital_land_queries import (
    fetch_log_summary,
    fetch_sources,
    fetch_organisation_stats,
    fetch_publisher_coverage,
    fetch_source_counts,
    fetch_resource_count_per_dataset,
    fetch_resource,
    fetch_resources,
    fetch_total_resource_count,
    fetch_logs,
    fetch_content_type_counts,
    get_source_counts,
)
from application.data_access.dataset_db_queries import fetch_resource_from_dataset

from application.utils import (
    create_dict,
    index_by,
    recent_dates,
    read_json_file,
    yesterday,
    convert_field_str_to_list,
    filter_off_btns,
)


base = Blueprint("base", __name__)


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
    entity_counts = fetch_entity_count()

    content_type_counts = sorted(
        fetch_content_type_counts(),
        key=lambda x: x["resource_count"],
        reverse=True,
    )

    return render_template(
        "performance.html",
        info_page=url_for("base.performance_info"),
        datasets=gs_datasets,
        stats=get_monthly_counts(),
        publisher_count=fetch_publisher_coverage(),
        source_counts=fetch_source_counts(groupby="dataset"),
        entity_count=ds.get_entity_count(),
        datasets_with_data_count=len(entity_counts.keys()),
        resource_count=fetch_total_resource_count(),
        publisher_using_enddate_count=len(
            fetch_organisation_entities_using_end_dates()
        ),
        content_type_counts=content_type_counts,
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


###########
# Resources
###########


@base.route("/resource")
def resources():
    filters = {}
    if request.args.get("pipeline"):
        filters["pipeline"] = request.args.get("pipeline")
    if request.args.get("content_type"):
        filters["content_type"] = unquote(request.args.get("content_type"))
    if request.args.get("organisation"):
        filters["organisation"] = request.args.get("organisation")
    if request.args.get("resource"):
        filters["resource"] = request.args.get("resource")

    resources_per_dataset = index_by("pipeline", fetch_resource_count_per_dataset())

    if len(filters.keys()):
        resource_records_results = fetch_resources(filters=filters)
    else:
        resource_records_results = fetch_resources()

    content_type_counts = sorted(
        fetch_content_type_counts(),
        key=lambda x: x["resource_count"],
        reverse=True,
    )

    columns = resource_records_results[0].keys() if resource_records_results else []
    resource_results = [create_dict(columns, row) for row in resource_records_results]

    return render_template(
        "resource/index.html",
        by_dataset=resources_per_dataset,
        resource_count=fetch_total_resource_count(),
        content_type_counts=content_type_counts,
        datasets=fetch_entity_count(),
        resources=resource_results,
        filters=filters,
        filter_btns=filter_off_btns(filters),
        organisations=fetch_organisation_stats(),
    )


@base.route("/resource/<resource>")
def resource(resource):
    resource_data = convert_field_str_to_list(fetch_resource(resource), "content_type")
    dataset = resource_data[0]["pipeline"].split(";")[0]
    return render_template(
        "resource/resource.html",
        resource=resource_data,
        info_page=url_for("base.resource_info", resource=resource),
        resource_counts=fetch_resource_from_dataset(dataset, resource),
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
    include_blanks = False
    if request.args.get("include_blanks") is not None:
        include_blanks = request.args.get("include_blanks")

    if len(filters.keys()):
        source_records, query_url = fetch_sources(
            filter=filters, include_blanks=include_blanks
        )
    else:
        source_records, query_url = fetch_sources(include_blanks=include_blanks)

    return render_template(
        "source/index.html",
        datasets=fetch_source_counts(groupby="dataset"),
        counts=get_source_counts()[0],
        sources=source_records,
        filters=filters,
        filter_btns=filter_off_btns(filters),
        organisations=fetch_source_counts(groupby="organisation"),
        query_url=query_url,
        include_blanks=include_blanks,
    )


@base.route("/source/<source>")
def source(source):
    source_data, q = fetch_sources(filter={"source": source})
    if len(source_data) == 0:
        # if no source record return check if blank one exists
        source_data, q = fetch_sources(filter={"source": source}, include_blanks=True)
    resource_result = fetch_resources(filters={"source": source})

    columns = resource_result[0].keys() if resource_result else []

    return render_template(
        "source/source.html",
        source=source_data[0],
        resources=[create_dict(columns, row) for row in resource_result],
    )


###############
# Content-types
###############


@base.route("/content-type")
def content_types():
    pipeline = request.args.get("pipeline")

    content_type_counts = sorted(
        fetch_content_type_counts(dataset=pipeline)
        if pipeline
        else fetch_content_type_counts(),
        key=lambda x: x["resource_count"],
        reverse=True,
    )

    if pipeline:
        return render_template(
            "content_type/index.html",
            content_type_counts=content_type_counts,
            pipeline=pipeline,
        )

    return render_template(
        "content_type/index.html", content_type_counts=content_type_counts
    )


@base.route("/content-type/<content_type>")
def content_type(content_type):

    unquoted_content_type = unquote(content_type)

    return render_template(
        "content_type/type.html",
        content_type=unquoted_content_type,
        resources=fetch_logs(
            filters={"content_type": unquoted_content_type}, group_by="resource"
        ),
    )


######
# Logs
######


@base.route("/logs")
def logs():
    ds = DLDatasette()

    if (
        request.args.get("log-date-day")
        and request.args.get("log-date-month")
        and request.args.get("log-date-year")
    ):

        log_year = request.args.get("log-date-year")
        log_month = request.args.get("log-date-month")
        log_day = request.args.get("log-date-day")
        d = f"{log_year}-{log_month}-{log_day}"
        return redirect(url_for("base.log", date=d))

    summary = fetch_log_summary()

    return render_template(
        "logs/logs.html",
        summary=summary,
        resources=ds.get_new_resources(),
        yesterday=yesterday(string=True),
        endpoint_count=sum([status["count"] for status in summary]),
    )


@base.route("/logs/<date>")
def log(date):
    ds = DLDatasette()

    summary = fetch_log_summary(date=date)

    return render_template(
        "logs/logs.html",
        summary=summary,
        resources=ds.get_new_resources(dates=[date]),
        date=date,
        endpoint_count=sum([status["count"] for status in summary]),
    )
