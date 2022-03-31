import logging
import urllib.parse

from application.caching import get
from application.data_access.api_queries import get_organisation_entity_number
from application.data_access.db import Database
from application.factory import entity_db_path
from application.utils import split_organisation_id

logger = logging.getLogger(__name__)

DATASETTE_URL = "https://datasette.digital-land.info"


def fetch_entity_count(dataset=None, organisation_entity=None):
    query_lines = [
        "SELECT",
        "dataset,",
        "COUNT(DISTINCT entity) AS count",
        "FROM",
        "entity",
    ]
    if organisation_entity:
        query_lines.append("WHERE")
        query_lines.append(f"organisation_entity = '{organisation_entity}'")
    if dataset:
        if "WHERE" not in query_lines:
            query_lines.append("WHERE")
        else:
            query_lines.append("AND")
        query_lines.append(f"dataset = '{dataset}'")
    else:
        query_lines.append("GROUP BY")
        query_lines.append("dataset")

    query_str = " ".join(query_lines)

    with Database(entity_db_path) as db:
        rows = db.execute(query_str).fetchall()
    if rows:
        return {dataset[0]: dataset[1] for dataset in rows}
    return {}


def fetch_organisation_entity_count(organisation, dataset=None):
    prefix, ref = split_organisation_id(organisation)
    return fetch_entity_count(
        dataset=dataset,
        organisation_entity=get_organisation_entity_number(prefix, ref),
    )


def fetch_organisation_entities_using_end_dates():
    query_lines = [
        "SELECT",
        "entity.organisation_entity",
        "FROM",
        "entity",
        "WHERE",
        '("end_date" is not null and "end_date" != "")',
        "AND",
        '("organisation_entity" is not null and "organisation_entity" != "")',
        "GROUP BY",
        "organisation_entity",
    ]
    query_str = " ".join(query_lines)

    with Database(entity_db_path) as db:
        rows = db.execute(query_str).fetchall()
    return rows


def fetch_datasets_organisation_has_used_enddates(organisation):
    datasette_url = DATASETTE_URL
    prefix, ref = split_organisation_id(organisation)
    organisation_entity_num = get_organisation_entity_number(prefix, ref)
    if not organisation_entity_num:
        return None
    query_lines = [
        "SELECT",
        "entity.dataset",
        "FROM",
        "entity",
        "WHERE",
        '("end_date" is not null and "end_date" != "")',
        "AND",
        f'("organisation_entity" = {organisation_entity_num})',
        "GROUP BY",
        "entity.dataset",
    ]
    query_str = " ".join(query_lines)
    query = urllib.parse.quote(query_str)
    url = f"{datasette_url}/entity.json?sql={query}"
    logger.info("get_datasets_organisation_has_used_enddatess: %s", url)
    result = get(url, format="json")
    if len(result["rows"]):
        return [dataset[0] for dataset in result["rows"]]
    return []
