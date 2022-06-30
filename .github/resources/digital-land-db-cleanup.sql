DELETE
FROM "column"
WHERE resource NOT IN (SELECT resource FROM resource_organisation WHERE organisation != 'local-authority-eng:HAT');

DELETE
FROM convert
WHERE resource NOT IN (SELECT resource FROM resource_organisation WHERE organisation != 'local-authority-eng:HAT');

DELETE
FROM endpoint
WHERE endpoint NOT IN (SELECT resource_endpoint.endpoint
                       FROM resource_endpoint
                                JOIN resource_organisation
                                     ON resource_endpoint.resource = resource_organisation.resource
                       WHERE organisation = 'local-authority-eng:HAT');

DELETE
FROM "log"
WHERE endpoint NOT IN (SELECT resource_endpoint.endpoint
                       FROM resource_endpoint
                                JOIN resource_organisation
                                     ON resource_endpoint.resource = resource_organisation.resource
                       WHERE organisation = 'local-authority-eng:HAT');

DELETE
FROM source_pipeline
WHERE source NOT IN (SELECT source FROM source WHERE organisation = 'local-authority-eng:HAT');

DELETE
FROM source
WHERE organisation != 'local-authority-eng:HAT';
