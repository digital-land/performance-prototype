import csv
import requests


class GooglesheetsCollector:
    def __init__(
        self, key="1Euj1Hok-gggrOyZFbaRl7A7Ck7bL6koYTGiuOMHjRF8", sheet="performance"
    ) -> None:
        self.sheet = sheet
        self.key = key
        self.main_url = self.generate_csv_url()
        self.session = requests.Session()
        print("SHEET: ", sheet)

    def generate_csv_url(self):
        return (
            "https://docs.google.com/spreadsheets/d/%s/gviz/tq?tqx=out:csv&sheet=%s"
            % (self.key, self.sheet)
        )

    def read_sheet(self):
        content = self.session.get(self.main_url)
        return content.content.decode("utf-8")

    def read_by_row(self, func=None):
        content = self.read_sheet()
        rows = []
        for row in csv.DictReader(content.splitlines()):
            rows.append(row)
            if func is not None:
                func(row)
        if func is None:
            return rows


def get_datasets():
    sheets_collector = GooglesheetsCollector()
    return sheets_collector.read_by_row()


def get_bfl():
    collector = GooglesheetsCollector(sheet="brownfield-land-by-org")
    rows = collector.read_by_row()
    # print(rows[0])
    expected = [o for o in rows if o["expected-to-publish"] == "yes"]
    additional = [o for o in rows if o["expected-to-publish"] != "yes"]
    return expected, additional
