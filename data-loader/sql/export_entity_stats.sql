.headers on
.mode csv

.output entity_count.csv

SELECT
  COUNT(DISTINCT entity) AS count
FROM entity;


.output entity_counts.csv

SELECT COUNT(DISTINCT entity) AS count, dataset, organisation_entity
FROM entity
GROUP BY dataset, organisation_entity;


.output entity_end_date_counts.csv

SELECT dataset, organisation_entity, end_date
FROM entity
WHERE end_date is not null
AND end_date != ''
AND organisation_entity is not null
AND organisation_entity != '';
