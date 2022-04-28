local_authorities = {
    "local-authority-eng:LBH": "London Borough of Lambeth",
    "local-authority-eng:SWK": "London Borough of Southwark",
    "local-authority-eng:BUC": "Buckinghamshire Council",
    "local-authority-eng:CAT": "Canterbury City Council",
}

tests = {
    "local-authority-eng:LBH": {
        "Lambeth Southbank House listed building": {
            "query": "?geometry=POINT(-0.1198903 51.4922191)&geometry_relation=intersects&dataset=listed-building-outline",
            "dataset": "listed-building-outline",
            "assertions": {
                "$.count": 1,
                "$.entities[0].name": "Southbank House, Black Prince Road",
                "$.entities[0].organisation-entity": "192",
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
            "ticket": "https://trello.com/c/CXgfYGUR/19-lambeth-conservation-areas",
            "query": "?geometry=POINT(-0.1198903 51.4922191)&geometry_relation=intersects&dataset=conservation-area",
            "dataset": "conservation-area",
            "assertions": {
                "$.count": 1,
                "$.entities[0].reference": "61",
                "$.entities[0].name": "Albert Embankment",
                "$.entities[0].organisation-entity": "192",
            },
        },
        "Lambeth article 4 direction Brixton": {
            "ticket": "https://trello.com/c/JQuyFI3t/18-lambeth-article-4-directions",
            "query": "?geometry=POINT(-0.114154 51.462486)&geometry_relation=intersects&dataset=article-4-direction-area",
            "dataset": "article-4-direction-area",
            "assertions": {
                "$.count": 1,
                "$.entities[0].name": "Brixton Town Centre",
                "$.entities[0].organisation-entity": "192",
                "$.entities[0].notes": "Brixton",
            },
        },
        "Lambeth article 4 direction South Bank House and Newport Street": {
            "ticket": "https://trello.com/c/JQuyFI3t/18-lambeth-article-4-directions",
            "query": "?geometry=POINT(-0.1198903 51.4922191)&geometry_relation=intersects&dataset=article-4-direction-area",
            "dataset": "article-4-direction-area",
            "assertions": {
                "$.count": 1,
                "$.entities[0].name": "South Bank House and Newport Street",
                "$.entities[0].organisation-entity": "192",
                "$.entities[0].notes": "KIBA",
            },
        },
        "Lambeth article 4 direction count": {
            "ticket": "https://trello.com/c/JQuyFI3t/18-lambeth-article-4-directions",            
            "query": "?dataset=article-4-direction-area&organisation_entity=192&field=reference",
            "dataset": "article-4-direction-area",
            "assertions": {
                "$.count": 28,
            },
        },
        "Lambeth conservation area Park Hall Road": {
            "ticket": "https://trello.com/c/CXgfYGUR/19-lambeth-conservation-areas",
            "query": "?geometry=POINT(-0.09303242 51.43599392)&geometry_relation=intersects&dataset=conservation-area",
            "dataset": "conservation-area",
            "assertions": {
                "$.count": 3,
                "$.entities[0].reference": "CA19",
                "$.entities[0].name": "Park Hall Road",
                "$.entities[0].organisation-entity": "192",
            },
        },
        "Lambeth conservation area Roupell Street": {
            "ticket": "https://trello.com/c/CXgfYGUR/19-lambeth-conservation-areas",
            "query": "?geometry=POINT(-0.10978987 51.50460093)&geometry_relation=intersects&dataset=conservation-area",
            "dataset": "conservation-area",
            "assertions": {
                "$.count": 1,
                "$.entities[0].reference": "CA21",
                "$.entities[0].name": "Roupell Street",
                "$.entities[0].organisation-entity": "192",
            },
        },
        "Lambeth conservation area Streatham Lodge": {
            "ticket": "https://trello.com/c/CXgfYGUR/19-lambeth-conservation-areas",
            "query": "?geometry=POINT(-0.12175931+51.41598617)&geometry_relation=intersects&dataset=conservation-area",
            "dataset": "conservation-area",
            "assertions": {
                "$.count": 1,
                "$.entities[0].reference": "CA62",
                "$.entities[0].name": "Streatham Lodge",
                "$.entities[0].organisation-entity": "192",
            },
        },
        "Lambeth has no scheduled monuments": {
            "query": "?dataset=scheduled-monument&geometry_reference=E09000022",
            "dataset": "scheduled-monument",
            "assertions": {
                "$.count": 0,
            },
        },
        "Lambeth has no areas of outstanding natural beauty": {
            "query": "?dataset=area-of-outstanding-natural-beauty&geometry_reference=E09000022",
            "dataset": "area-of-outstanding-natural-beauty",
            "assertions": {
                "$.count": 0,
            },
        },
    },
    "local-authority-eng:BUC": {
        "Chilterns area of outstanding natural beauty": {
            "query": "?geometry=POINT(-0.8463452 51.6682134)&geometry_relation=intersects&dataset=area-of-outstanding-natural-beauty",
            "dataset": "area-of-outstanding-natural-beauty",
            "assertions": {
                "$.count": 1,
                "$.entities[0].reference": "5",
                "$.entities[0].name": "Chilterns",
                "$.entities[0].organisation-entity": "501910",
            },
        },
        "Chilterns article 4 direction": {
            "query": "?geometry=POINT(-0.845119 51.667878)&geometry_relation=intersects&dataset=article-4-direction-area",
            "dataset": "article-4-direction-area",
            "assertions": {
                "$.count": 2,
                "$.entities[0].name": "Former Wycombe Rural District - Poultry Production",
                "$.entities[0].description": "Certain structures used for production of poultry or eggs - refer to Order & GDO 1950",
                "$.entities[1].name": "Bledlow-cum-Saunderton - Buildings for use as piggery",
                "$.entities[1].description": "Buildings for use as piggery on agricultural land - refer to Order and GDO 1963",
            },
        },
        "Buckinghamshire scheduled monument": {
            "query": "?geometry=POINT (-0.835789 51.724111)&geometry_relation=intersects&dataset=scheduled-monument",
            "dataset": "scheduled-monument",
            "assertions": {
                "$.count": 1,
                "$.entities[0].reference": "1006951",
                "$.entities[0].name": "The Mount",
            },
        },
        "Buckinghamshire has no central activities zone": {
            "query": "?dataset=central-activities-zone&geometry_reference=E06000060",
            "dataset": "central-activities-zone",
            "assertions": {
                "$.count": 0,
            },
        },
        "Whiteleaf tree preservation zone": {
            "query": "?geometry=POINT(-0.813461 51.732499)&geometry_relation=intersects&dataset=tree-preservation-zone",
            "dataset": "tree-preservation-zone",
            "assertions": {
                "$.count": 1,
            },
        },
        "tree preservation zones": {
            "query": "?geometry=POINT(-0.895052 51.558892)&geometry_relation=intersects&dataset=tree-preservation-zone",
            "dataset": "tree-preservation-zone",
            "assertions": {
                "$.count": 2,
                "$.entities[0].tree-preservation-type": "Area",
                "$.entities[1].tree-preservation-type": "Revoked",
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
                "$.entities[0].notes": "P2 New family homes; P29 Office and business development; P30 Affordable workspace",
            },
        },
        "Southwark conservation area": {
            "query": "?geometry=POINT(-0.0909083 51.5070023)&geometry_relation=intersects&dataset=conservation-area",
            "dataset": "conservation-area",
            "assertions": {
                "$.count": 1,
                "$.entities[0].reference": "COA00000759",
                "$.entities[0].name": "",
                "$.entities[0].organisation-entity": "329",
            },
        },
        "Southwark scheduled monument (Clink Street)": {
            "query": "?geometry=POINT(-0.0909083 51.5070023)&geometry_relation=intersects&dataset=scheduled-monument",
            "dataset": "scheduled-monument",
            "assertions": {
                "$.count": 1,
                "$.entities[0].reference": "1002054",
                "$.entities[0].name": "Remains of Winchester Palace, Clink Street and waterfront",
            },
        },
        "Southwark article 4 direction (The Lord Nelson, Union Street)": {
            "ticket": "https://trello.com/c/6G0Vv44y/22-southwark-article-4-directions",
            "query": "?dataset=article-4-direction-area&longitude=-0.102682&latitude=51.503432",
            "dataset": "article-4-direction-area",
            "assertions": {
                "$.count": 6,
                "$.entities[0].name": "The Lord Nelson",
                "$.entities[0].description": "Change of use, demolition or alteration of pubs is restricted",
                "$.entities[0].organisation-entity": "329",
                "$.entities[1].name": "Central Activities Zone",
                "$.entities[1].description": "Change of use from offices to dwelling houses is restricted",
                "$.entities[1].organisation-entity": "329",
                "$.entities[2].name": "Central Activities Zone",
                "$.entities[2].description": "Change of use from Class E to residential is restricted",
                "$.entities[2].organisation-entity": "329",
                "$.entities[3].name": "Bankside and Borough District Town Centre",
                "$.entities[3].description": "Change of use from Class E to residential is restricted",
                "$.entities[3].organisation-entity": "329",
                "$.entities[4].name": "Central Activities Zone",
                "$.entities[4].description": "Demolition of commercial buildings and construction of new dwellinghouses is restricted",
                "$.entities[4].organisation-entity": "329",
                "$.entities[5].name": "Bankside and Borough District Town Centre",
                "$.entities[5].description": "Demolition of commercial buildings and construction of new dwellinghouses is restricted",
                "$.entities[5].organisation-entity": "329",
            },
        },
        "Southwark article 4 direction (The Lord Nelson, Old Kent Road)": {
            "ticket": "https://trello.com/c/6G0Vv44y/22-southwark-article-4-directions",
            "query": "?dataset=article-4-direction-area&longitude=-0.074274&latitude=51.486724",
            "dataset": "article-4-direction-area",
            "assertions": {
                "$.count": 4,
                "$.entities[0].name": "THE LORD NELSON",
                "$.entities[0].description": "Change of use, demolition or alteration of pubs is restricted",
                "$.entities[0].organisation-entity": "329",
                "$.entities[1].name": "Old Kent Road North District Town Centre",
                "$.entities[1].description": "Change of use from Class E to residential is restricted",
                "$.entities[1].organisation-entity": "329",
                "$.entities[2].name": "Protected shopping frontage SF24: Old Kent Road, East Street and Dunton Road",
                "$.entities[2].description": "Change of use from Class E to residential is restricted",
                "$.entities[2].organisation-entity": "329",
                "$.entities[3].name": "Protected shopping frontage SF24: Old Kent Road, East Street and Dunton Road",
                "$.entities[3].description": "Demolition of commercial buildings and construction of new dwellinghouses is restricted",
                "$.entities[3].organisation-entity": "329",
            },
        },
        "Southwark article 4 direction ()": {
            "ticket": "https://trello.com/c/UMN89vva/8-unexpected-results-for-southwark-addresses",
            "query": "?dataset=article-4-direction-area&longitude=-0.1049237&latitude=51.5038861",
            "dataset": "article-4-direction-area",
            "assertions": {
                "$.count": 9,
                "$.entities[0].name": "Railway Arches",
                "$.entities[0].description": "Conversion of railway arches to residential dwellings is restricted",
                "$.entities[1].name": "Central Activities Zone",
                "$.entities[1].description": "Change of use from offices to dwelling houses is restricted",
                "$.entities[2].name": "Central Activities Zone",
                "$.entities[2].description": "Change of use from Class E to residential is restricted",
                "$.entities[3].name": "Site allocation NSP20: Southwark Station and 1 Joan Street",
                "$.entities[3].description": "Change of use from Class E to residential is restricted",
                "$.entities[4].name": "Bankside and Borough District Town Centre",
                "$.entities[4].description": "Change of use from Class E to residential is restricted",
                "$.entities[5].name": "Central Activities Zone",
                "$.entities[5].description": "Change of use from Class E to residential is restricted",
                "$.entities[6].name": "Site allocation NSP20: Southwark Station and 1 Joan Street",
                "$.entities[8].description": "Demolition of commercial buildings and construction of new dwellinghouses is restricted",
                "$.entities[7].name": "Bankside and Borough District Town Centre",
                "$.entities[8].description": "Demolition of commercial buildings and construction of new dwellinghouses is restricted",
                "$.entities[8].name": "Railway Arches",
                "$.entities[8].description": "Demolition of commercial buildings and construction of new dwellinghouses is restricted",
            },
        },
        "Southwark scheduled monument": {
            "query": "?geometry=POINT(-0.052963 51.501611)&geometry_relation=intersects&dataset=scheduled-monument",
            "dataset": "scheduled-monument",
            "assertions": {
                "$.count": 1,
                "$.entities[0].reference": "1005556",
                "$.entities[0].name": "Pumping engine house for Brunel's Thames tunnel",
            },
        },
        "Southwark has no areas of outstanding natural beauty": {
            "query": "?dataset=area-of-outstanding-natural-beauty&geometry_reference=E09000028",
            "dataset": "area-of-outstanding-natural-beauty",
            "assertions": {
                "$.count": 0,
            },
        },
    },
    "local-authority-eng:CAT": {
        "Cantebury article 4 direction (Kemberland Wood)": {
            "ticket": "https://trello.com/c/prY4jzj6/14-canterbury-article-4-directions",
            "query": "?dataset=article-4-direction-area&longitude=1.121256&latitude=51.315129",
            "dataset": "article-4-direction-area",
            "assertions": {
                "$.count": 2,
                "$.entities[0].name": "Land at Kemberland Wood, Sturry",
                "$.entities[0].description": "Article 4 Direction No 1 1979",
                "$.entities[0].organisation-entity": "75",
                "$.entities[0].start-date": "1979-03-16",
                "$.entities[1].name": "Canterbury and surrounding area",
                "$.entities[1].description": "The Canterbury HMO Article 4 D",
                "$.entities[1].organisation-entity": "75",
                "$.entities[1].notes": "Dated 25th February 2016",
                "$.entities[1].start-date": "2016-02-25",
            },
        },
        "Canterbury article 4 direction count": {
            "ticket": "https://trello.com/c/prY4jzj6/14-canterbury-article-4-directions",            
            "query": "?dataset=article-4-direction-area&organisation_entity=75&field=reference",
            "dataset": "article-4-direction-area",
            "assertions": {
                "$.count": 463,
            },
        },        
        "Canterbury scheduled monument": {
            "query": "?geometry=POINT(1.07739 51.277722)&geometry_relation=intersects&dataset=scheduled-monument",
            "dataset": "scheduled-monument",
            "assertions": {
                "$.count": 1,
                "$.entities[0].reference": "1003125",
                "$.entities[0].name": "Vacant land within Roman walls in Adelaide Place",
            },
        },
        "Kent Downs area of outstanding natural beauty": {
            "query": "?dataset=area-of-outstanding-natural-beauty&latitude=51.3869143&longitude=0.4540133",
            "dataset": "area-of-outstanding-natural-beauty",
            "assertions": {
                "$.count": 1,
                "$.entities[0].name": "Kent Downs",
            },
        },
        "Canterbury has no central activities zone": {
            "query": "?dataset=central-activities-zone&geometry_reference=E06000106",
            "dataset": "central-activities-zone",
            "assertions": {
                "$.count": 0,
            },
        },
    },
}
