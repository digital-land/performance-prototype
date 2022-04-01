from datetime import datetime

from flask import render_template, Blueprint, request
from flask.helpers import url_for

from application.data_access.digital_land_queries import (
    get_datasets,
    get_active_resources,
    get_latest_resource,
    get_latest_collector_run_date,
    get_sources,
    get_themes,
    get_typologies,
    get_resource_count_per_dataset,
    get_publisher_coverage,
    get_content_type_counts,
    get_source_counts,
)
from application.data_access.entity_queries import (
    get_grouped_entity_count,
    get_entity_count,
)
from application.utils import (
    filter_off_btns,
    resources_per_publishers,
    index_by,
    read_json_file,
)

# trying to replace these
from application.data_access.datasette import (
    get_monthly_counts,
    publisher_counts,
    get_datasets_summary,
)

dataset_bp = Blueprint("dataset", __name__, url_prefix="/dataset")


@dataset_bp.route("/")
def datasets():
    filters = {}
    # if request.args.get("active"):
    #     filters["active"] = request.args.get("active")
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
        themes=get_themes(),
        typologies=get_typologies(),
    )


@dataset_bp.route("/<dataset>")
def dataset(dataset):
    datasets = get_datasets_summary()
    dataset_name = dataset
    dataset = [v for k, v in datasets.items() if v.get("pipeline") == dataset]

    resources_by_publisher = resources_per_publishers(
        get_active_resources(dataset_name)
    )

    # publishers = fetch_publisher_stats(dataset_name)
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

    resource_counts = index_by("pipeline", get_resource_count_per_dataset())
    resource_count = (
        resource_counts[dataset_name]["resources"]
        if resource_counts.get(dataset_name)
        else 0
    )

    sources_no_doc_url, query_url = get_sources(
        limit=500, filter={"documentation_url": "", "pipeline": dataset_name}
    )

    try:
        # wrapping in try/except because datasette occasionally timesout
        content_type_counts = sorted(
            get_content_type_counts(dataset=dataset_name),
            key=lambda x: x["resource_count"],
            reverse=True,
        )
    except Exception as e:
        print(e)
        content_type_counts = []
        print("Query to extract content type counts is failing")

    blank_sources, bls_query = get_sources(
        limit=500,
        filter={"pipeline": dataset_name},
        only_blanks=True,
    )

    return render_template(
        "dataset/performance.html",
        name=dataset_name,
        info_page=url_for("dataset.dataset_info", dataset=dataset_name),
        dataset=dataset[0] if len(dataset) else "",
        latest_resource=get_latest_resource(dataset_name),
        monthly_counts=get_monthly_counts(pipeline=dataset_name),
        publishers=publisher_splits,
        today=datetime.utcnow().isoformat()[:10],
        entity_count=get_entity_count(pipeline=dataset_name),
        resource_count=resource_count,
        coverage=get_publisher_coverage(dataset_name),
        resource_stats=resource_stats,
        sources_no_doc_url=sources_no_doc_url,
        content_type_counts=content_type_counts,
        latest_logs=get_latest_collector_run_date(dataset=dataset_name),
        blank_sources=blank_sources,
        source_count=get_source_counts(pipeline=dataset_name),
    )


@dataset_bp.route("/<dataset>/info")
def dataset_info(dataset):
    data = read_json_file("application/data/info/dataset.json")
    return render_template(
        "info.html",
        page_title=dataset + " performance",
        page_url=url_for("dataset.dataset_performance", dataset_name=dataset),
        data=data,
    )
