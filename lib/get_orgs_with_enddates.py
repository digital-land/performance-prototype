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
	"developer-agreement"
]

query_url = "http://datasette.digital-land.info/{}.json?sql=select%0D%0A++o.value%0D%0Afrom%0D%0A++fact+AS+f%0D%0AJOIN+fact+AS+o+ON+o.slug+%3D+f.slug%0D%0AWHERE%0D%0A++f.attribute+%3D+%22end-date%22%0D%0A++AND+f.value+%21%3D+%22%22%0D%0A++AND+o.attribute+%3D+%22organisation%22%0D%0AGROUP+BY%0D%0Ao.value"
orgs_with_end_dates = DefaultDict(list)
    

async def retrieve_orgs_with_end_dates(db):
    async with aiohttp.ClientSession() as session:
        async with session.get(query_url.format(db)) as response:
            results = await response.json()
            if response.status == 200:
                for org_list in results["rows"]:
                    orgs_with_end_dates[org_list[0]].append(db)
            else:
                print(response.status)
                print(db)

async def main():
    tasks = [retrieve_orgs_with_end_dates(db) for db in EAV_MODELS]
    await asyncio.gather(*tasks)

start_time = time.time()
asyncio.run(main())
print(orgs_with_end_dates)
print(time.time() - start_time)
