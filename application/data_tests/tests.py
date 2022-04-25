tests = {
    "local-authority-eng:LBH": {
        "Lambeth Southbank House listed building": {
            "query": "?geometry=POINT(-0.1198903 51.4922191)&geometry_relation=intersects&dataset=listed-building-outline",
            "dataset": "listed-building-outline",
            "assertions": {
                "$.count": 1,
                "$.entities[0].reference": "13",
                "$.entities[0].name": "South Bank House and Newport Street",
                "$.entities[0].organisation-entity": "192",
                "$.entities[0].notes": "KIBA",
                "$.entities[0].listed-building-grade": "II",
            },
        },
        "Lambeth central activities zone": {
            "query": "?geometry=POINT(-0.1198903 51.4922191)&geometry_relation=intersects&dataset=central-activities-zone",
            "dataset": "central-activities-zone",
            "assertions": {
                "$.count": 1,
                "$.entities[0].reference": "CAZ00000001",
                "$.entities[0].name": "",
                "$.entities[0].organisation-entity": "",
            },
        },
        "Albert Embankment conservation area": {
            "query": "?geometry=POINT(-0.1198903 51.4922191)&geometry_relation=intersects&dataset=conservation-area",
            "dataset": "conservation-area",
            "assertions": {
                "$.count": 1,
                "$.entities[0].reference": "61",
                "$.entities[0].name": "Albert Embankment",
                "$.entities[0].organisation-entity": "192",
            },
        },
        "Lambeth article 4 direction": {
            "query": "?geometry=POINT(-0.1198903 51.4922191)&geometry_relation=intersects&dataset=article-4-direction-area",
            "dataset": "article-4-direction-area",
            "assertions": {
                "$.count": 1,
                "$.entities[0].reference": "13",
                "$.entities[0].name": "South Bank House and Newport Street",
                "$.entities[0].organisation-entity": "192",
                "$.entities[0].notes": "KIBA",
            },
        },
    },
    "local-authority-eng:BUC": {
        "Chilterns area of outstanding natural beauty": {
            "query": "?geometry=POINT(-0.8463452 2051.6682134)&geometry_relation=intersects&dataset=area-of-outstanding-natural-beauty",
            "dataset": "area-of-outstanding-natural-beauty",
            "assertions": {
                "$.count": 1,
                "$.entities[0].reference": "5",
                "$.entities[0].name": "Chilterns",
                "$.entities[0].organisation-entity": "local-authority-eng:BUC",
            },
        },
        "Chilterns article 4 direction": {
            "query": "?geometry=POINT(-0.8463452 2051.6682134)&geometry_relation=intersects&dataset=article-4-direction",
            "dataset": "article-4-direction",
            "assertions": {
                "$.count": 2,
                "$.entities[0].reference": "159",
                "$.entities[0].name": "Former Wycombe Rural District - Poultry Production",
                "$.entities[0].organisation-entity": "",
                "$.entities[1].reference": "163",
                "$.entities[1].name": "Bledlow-cum-Saunderton - Buildings for use as piggery",
                "$.entities[1].organisation-entity": "",
            },
        },
    },
    "local-authority-eng:SWK": {
        "Southwark central activities zone": {
            "query": "?geometry=POINT(-0.0909083 51.5070023)&geometry_relation=intersects&dataset=central-activities-zone",
            "dataset": "central-activities-zone",
            "assertions": {
                "$.count": 1,
                "$.entities[0].reference": "CAZ00000002",
                "$.entities[0].name": "",
                "$.entities[0].organisation-entity": "329",
                "$.entities[0].prefix": "central-activities-zone",
                "$.entities[0].notes": "P2 New family homes; P29 Office and business development; P30 Affordable workspace"
            },
        },
        "Southwark conservation area": {
            "query": "?geometry=POINT(-0.0909083 51.5070023)&geometry_relation=intersects&dataset=conservation-area",
            "dataset": "conservation-area",
            "assertions": {
                "$.count": 1,
                "$.entities[0].reference": "COA00000759",
                "$.entities[0].name": "",
                "$.entities[0].organisation-entity": "329"
            },
        },
        "Southwark  scheduled monument": {
            "query": "?geometry=POINT(-0.0909083 51.5070023)&geometry_relation=intersects&dataset=scheduled-monument",
            "dataset": "scheduled-monument",
            "assertions": {
                "$.count": 1,
                "$.entities[0].reference": "1002054",
                "$.entities[0].name": "Remains of Winchester Palace, Clink Street and waterfront",
                "$.entities[0].organisation-entity": "329"
            },
        },
        "Southwark article 4 direction": {
            "query": "?geometry=POINT(-0.0909083 51.5070023)&geometry_relation=intersects&dataset=article-4-direction",
            "dataset": "article-4-direction",
            "assertions": {
                "$.count": 3
            },
        }
    },
    "local-authority-eng:CAT": {},
}
