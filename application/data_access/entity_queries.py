import logging

from application.data_access.api_queries import get_organisation_entity_number
from application.data_access.db import Database
from application.factory import entity_db_path
from application.utils import split_organisation_id

logger = logging.getLogger(__name__)


def get_total_entity_count():
    sql = "SELECT COUNT(DISTINCT entity) AS count FROM entity"
    with Database(entity_db_path) as db:
        row = db.execute(sql).fetchone()
    return row["count"]


def get_entity_count(pipeline=None):
    if pipeline is not None:
        sql = "SELECT COUNT(DISTINCT entity) AS count FROM entity e WHERE e.dataset = :pipeline"
        with Database(entity_db_path) as db:
            row = db.execute(sql, {"pipeline": pipeline}).fetchone()
        return row["count"]

    return get_total_entity_count()


def get_grouped_entity_count(dataset=None, organisation_entity=None):
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


def get_organisation_entity_count(organisation, dataset=None):
    prefix, ref = split_organisation_id(organisation)
    return get_grouped_entity_count(
        dataset=dataset,
        organisation_entity=get_organisation_entity_number(prefix, ref),
    )


def get_organisation_entities_using_end_dates():
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


def get_datasets_organisation_has_used_enddates(organisation):
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
    with Database(entity_db_path) as db:
        rows = db.execute(query_str).fetchall()
    if rows:
        return [dataset[0] for dataset in rows]

    return []
