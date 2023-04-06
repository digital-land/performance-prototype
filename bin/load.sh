#! /usr/bin/env sh
set -e

if [ -f ./.env ]; then
  export $(cat .env | xargs)
fi



URL="https://datasette.planning.data.gov.uk/entity.db"

cd data-loader
for F in *.csv; do
  if [ ! -f "$F" ]; then break; fi
  rm "$F"
done

if [ ! -f "$(basename "$URL")" ]; then
  echo "downloading from $URL"
  curl -O $URL
else
  echo "using $(basename "$URL") from local filesystem"
fi

echo "exporting"

sqlite3 entity.db ".read sql/export_entity_stats.sql"

if [ -f ../entity-stats.sqlite3 ]; then
  rm ../entity-stats.sqlite3
fi

sqlitebiter -o ../entity-stats.db file *.csv

rm *.csv
rm entity.db

echo "load done"

cd -
