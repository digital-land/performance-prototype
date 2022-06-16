#! /usr/bin/env sh
set -e

if [ -f ./.env ]; then
  export $(cat .env | xargs)
fi

BUCKET=digital-land-production-collection-dataset
URL="https://$BUCKET.s3.eu-west-2.amazonaws.com/entity-builder/dataset/entity.sqlite3"

cd data-loader
for F in *.csv; do
  if [ ! -f "$F" ]; then break; fi
  rm "$F"
done

echo "downloading from $URL"
curl -O $URL

echo "exporting"

sqlite3 entity.sqlite3 ".read sql/export_entity_stats.sql"

if [ -f ../entity-stats.sqlite3 ]; then
  rm ../entity-stats.sqlite3
fi

sqlitebiter -o ../entity-stats.sqlite3 file *.csv

rm *.csv
rm entity.sqlite3

echo "load done"

cd -
