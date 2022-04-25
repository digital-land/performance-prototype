tests = {
    "local-authority-eng:LBH": {
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
    },
    "local-authority-eng:CAT": {},
    "local-authority-eng:BUC": {
        "Chilterns area of outstanding natural beauty": {
            "query": "?geometry=POINT(-0.8463452%2051.6682134)&geometry_relation=intersects&dataset=area-of-outstanding-natural-beauty",
            "dataset": "area-of-outstanding-natural-beauty",
            "assertions": {
                "$.count": 1,
                "$.entities[0].reference": "5",
                "$.entities[0].name": "Chilterns",
                "$.entities[0].organisation-entity": "local-authority-eng:BUC",
            },
        },
        "Chilterns article 4 direction": {
            "query": "?geometry=POINT(-0.8463452%2051.6682134)&geometry_relation=intersects&dataset=article-4-direction",
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
    "local-authority-eng:SWK": {},
}
