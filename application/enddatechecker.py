import asyncio
from typing import DefaultDict
import aiohttp
import time

EAV_MODELS = [
    "document-type",
    "development-plan-type",
    "development-policy-category",
    "planning-permission-status",
    "planning-permission-type",
    "conservation-area",
    "ownership-status",
    "site-category",
    "local-authority-district",
    "parish",
    "ancient-woodland",
    "area-of-outstanding-natural-beauty",
    "brownfield-land",
    "brownfield-site",
    "development-policy",
    "development-plan-document",
    "document",
    "green-belt",
    "heritage-coast",
    "battlefield",
    "building-preservation-notice",
    "certificate-of-immunity",
    "heritage-at-risk",
    "listed-building",
    "park-and-garden",
    "protected-wreck-site",
    "scheduled-monument",
    "world-heritage-site",
    "special-area-of-conservation",
    "ramsar",
    "site-of-special-scientific-interest",
    "article-4-direction",
    "infrastructure-funding-statement",
    "contribution-funding-status",
    "contribution-purpose",
    "developer-agreement-contribution",
    "developer-agreement-transaction",
    "developer-agreement-type",
    "developer-agreement",
]

from datasette import DLDatasette

class EndDateChecker:
    def __init__(self):
        self.orgs_with_end_dates = DefaultDict(list)

    @staticmethod
    def query_url(organisation=None):
        if organisation is not None:
            return (
                "{}/{}.json?sql=select%0D%0A++o.value%0D%0Afrom%0D%0A++fact+AS+f%0D%0AJOIN+fact+AS+o+ON+o.slug+%3D+f.slug%0D%0AWHERE%0D%0A++f.attribute+%3D+%22end-date%22%0D%0A++AND+f.value+%21%3D+%22%22%0D%0A++AND+o.attribute+%3D+%22organisation%22%0D%0A++AND+o.value+%3D+%3Aorganisation%0D%0AGROUP+BY%0D%0Ao.value&organisation="
                + organisation
            )
        return "{}/{}.json?sql=select%0D%0A++o.value%0D%0Afrom%0D%0A++fact+AS+f%0D%0AJOIN+fact+AS+o+ON+o.slug+%3D+f.slug%0D%0AWHERE%0D%0A++f.attribute+%3D+%22end-date%22%0D%0A++AND+f.value+%21%3D+%22%22%0D%0A++AND+o.attribute+%3D+%22organisation%22%0D%0AGROUP+BY%0D%0Ao.value"

    async def retrieve_orgs_with_end_dates(self, db, organisation):
        async with aiohttp.ClientSession() as session:
            query = self.query_url(organisation).format(DLDatasette.BASE_URL, db)
            # print(query)
            async with session.get(query) as response:
                results = await response.json()
                if response.status == 200:
                    for org_list in results["rows"]:
                        self.orgs_with_end_dates[org_list[0]].append(db)
                else:
                    print(response.status)
                    print(db)

    async def main(self, organisation):
        self.orgs_with_end_dates = DefaultDict(list)
        tasks = [
            self.retrieve_orgs_with_end_dates(db, organisation) for db in EAV_MODELS
        ]
        await asyncio.gather(*tasks)

    def get_organisations(self, organisation=None):
        start_time = time.time()
        asyncio.run(self.main(organisation))
        return self.orgs_with_end_dates
        # print(time.time() - start_time)

    def get_count(self):
        self.get_organisations()
        return len(self.orgs_with_end_dates)

    def has_used_enddate(self, organisation):
        self.get_organisations(organisation)
        return (
            bool(len(self.orgs_with_end_dates)),
            self.orgs_with_end_dates[organisation],
        )
