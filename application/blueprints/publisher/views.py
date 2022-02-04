from datetime import datetime

from flask import render_template, Blueprint, current_app, redirect
from flask.helpers import url_for
from flask import request

from application.datasette import (
    datasets_for_an_organisation,
    get_organisation,
    DLDatasette,
)
from application.data_access.entity_queries import (
    fetch_organisation_entity_count,
    fetch_datasets_organisation_has_used_enddates,
)

from application.data_access.digital_land_queries import (
    fetch_datasets,
    fetch_sources_by_organisation,
    fetch_organisation_stats,
)

from application.data_access.api_queries import get_entities

from application.utils import (
    index_by,
    index_with_list,
    read_json_file,
)


publisher_pages = Blueprint("publisher", __name__, url_prefix="/organisation")


@publisher_pages.context_processor
def set_globals():
    return {"staticPath": "https://digital-land.github.io"}


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


@publisher_pages.route("/")
def organisation():
    ds = DLDatasette()
    publishers_with_no_data = {
        k: publisher
        for k, publisher in ds.get_expected_publishers().items()
        if publisher["active"] == 0
    }

    return render_template(
        "organisation/index.html",
        publishers=split_publishers(fetch_organisation_stats()),
        today=datetime.utcnow().isoformat()[:10],
        none_publishers=split_publishers(publishers_with_no_data),
    )


@publisher_pages.route("/<prefix>/<org_id>")
def organisation_performance(prefix, org_id):
    ds = DLDatasette()
    id = prefix + ":" + org_id
    organisation = get_organisation(id)
    data = datasets_for_an_organisation(id)
    source_counts = ds.get_sources_per_dataset_for_organisation(id)
    sources = index_with_list("pipeline", ds.get_all_sources_for_organisation(id))
    missing_datasets = [
        dataset for dataset in source_counts if dataset["sources_with_endpoint"] == 0
    ]

    # TO FIX: I'm not sure this is working
    erroneous_sources = []
    for dataset in data["datasets_covered"]:
        for source in sources[dataset]:
            if source["endpoint"] == "":
                erroneous_sources.append(source)

    # setup dict to capture datasets with data from secondary sources
    data["data_from_secondary"] = {}

    # add entity counts to dataset data
    data["dataset_counts"] = index_by("pipeline", data["dataset_counts"])
    entity_counts = fetch_organisation_entity_count(organisation=id)
    for dn, count in entity_counts.items():
        if dn in data["dataset_counts"].keys():
            data["dataset_counts"][dn]["entity_count"] = count
        else:
            # add dataset to list from secondary sources
            data["data_from_secondary"].setdefault(dn, {"pipeline": dn})
            data["data_from_secondary"][dn]["entity_count"] = count

    return render_template(
        "organisation/performance.html",
        organisation=organisation,
        info_page=url_for("publisher.organisation_info", prefix=prefix, org_id=org_id),
        data=data,
        sources_per_dataset=source_counts,
        missing_datasets=missing_datasets,
        enddates=fetch_datasets_organisation_has_used_enddates(id),
        sources=sources,
        erroneous_sources=erroneous_sources,
        entity_counts=entity_counts,
    )


@publisher_pages.route("/<prefix>/<org_id>/info")
def organisation_info(prefix, org_id):
    data = read_json_file("application/data/info/organisation.json")
    return render_template(
        "info.html",
        page_title="Organisation performance",
        page_url=url_for(
            "publisher.organisation_performance", prefix=prefix, org_id=org_id
        ),
        data=data,
    )


@publisher_pages.route("/<prefix>/<org_id>/map")
def map(prefix, org_id):
    id = prefix + ":" + org_id
    organisation = get_organisation(id)

    dataset_name = "conservation-area"
    if request.args.get("dataset"):
        dataset_name = request.args.get("dataset")

    dataset = fetch_datasets(dataset=dataset_name)

    # should fail if no dataset of that name

    publisher_entities = get_entities(
        {
            "dataset": dataset["dataset"],
            "organisation_entity": organisation["entity"],
            "limit": "1000",
        }
    )

    intersecting_entities = get_entities(
        {
            "dataset": dataset["dataset"],
            "geometry_reference": organisation["statistical_geography"],
            "limit": "1000",
        }
    )

    entities_not_by_publisher = [
        e["entity"]
        for e in intersecting_entities
        if e["organisation-entity"] != str(organisation["entity"])
    ]

    additional_publishers = [
        e["organisation-entity"]
        for e in intersecting_entities
        if e["organisation-entity"] != str(organisation["entity"])
    ]

    expected_datasets = index_with_list(
        "pipeline", fetch_sources_by_organisation(organisation["organisation"])
    )

    return render_template(
        "organisation/map.html",
        organisation=organisation,
        publisher_entities=publisher_entities,
        entities_not_by_publisher=entities_not_by_publisher,
        additional_publishers=set(additional_publishers),
        dataset=dataset,
        expected_datasets=expected_datasets,
    )
