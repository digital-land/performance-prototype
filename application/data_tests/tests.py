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
        "Lambeth Stockwell Bus Garage": {
            "query": "?geometry=POINT(-0.12412339 51.47398582)&geometry_relation=intersects&dataset=listed-building-outline",
            "dataset": "listed-building-outline",
            "assertions": {
                "$.count": 1,
                "$.entities[0].name": "Stockwell Bus Garage, Binfield Road",
                "$.entities[0].organisation-entity": "192",
                "$.entities[0].listed-building-grade": "II*",
            },
        },
        "Lambeth Former Annie McCall Hospital": {
            "query": "?geometry=POINT(-0.12798257 51.47063541)&geometry_relation=intersects&dataset=listed-building-outline",
            "dataset": "listed-building-outline",
            "assertions": {
                "$.count": 1,
                "$.entities[0].organisation-entity": "192",
                "$.entities[0].listed-building-grade": "II",
            },
        },
        "Lambeth central activities zone": {
            "ticket": "https://trello.com/c/golBkjM7/39-central-activities-zone",
            "query": "?geometry=POINT(-0.1198903 51.4922191)&geometry_relation=intersects&dataset=central-activities-zone",
            "dataset": "central-activities-zone",
            "assertions": {
                "$.count": 1,
                "$.entities[0].reference": "CAZ00000001",
            },
        },
        "Albert Embankment conservation area": {
            "ticket": "https://trello.com/c/CXgfYGUR/19-lambeth-conservation-areas",
            "query": "?geometry=POINT(-0.1198903 51.4922191)&geometry_relation=intersects&dataset=conservation-area",
            "dataset": "conservation-area",
            "assertions": {
                "$.count": 1,
                "$.entities[0].reference": "CA57",
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
            "query": "?dataset=article-4-direction-area&organisation_entity=192",
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
                "$.count": 1,
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
            "ticket": "https://trello.com/c/xhCLfQ7r/38-scheduled-monuments",
            "query": "?dataset=scheduled-monument&geometry_reference=E09000022",
            "dataset": "scheduled-monument",
            "assertions": {
                "$.count": 0,
            },
        },
        "Lambeth has no areas of outstanding natural beauty": {
            "ticket": "https://trello.com/c/fwcRbQFr/40-area-of-outstanding-natural-beauty",
            "query": "?dataset=area-of-outstanding-natural-beauty&geometry_reference=E09000022",
            "dataset": "area-of-outstanding-natural-beauty",
            "assertions": {
                "$.count": 0,
            },
        },
        "Lambeth has no SSSI": {
            "ticket": "https://trello.com/c/r3wV6tXO/50-sites-of-special-and-or-scientific-interest",
            "query": "?dataset=site-of-special-scientific-interest&geometry_reference=E09000022",
            "dataset": "site-of-special-scientific-interest",
            "assertions": {
                "$.count": 0,
            },
        },
        "Dulwich college tree preservation zones": {
            "ticket": "https://trello.com/c/elSRI6Hs/21-lambeth-tree-preservation-orders",
            "query": "?geometry=POINT(-0.084859 51.441301)&geometry_relation=intersects&dataset=tree-preservation-zone",
            "dataset": "tree-preservation-zone",
            "assertions": {
                "$.count": 2,
                "$.entities[0].name": "Dulwich College",
                "$.entities[0].tree-preservation-order": "481",
                "$.entities[1].name": "Dulwich College, College Road",
                "$.entities[1].tree-preservation-order": "279",
            },
        },
        "Lambeth Tree Zone count": {
            "query": "?dataset=tree-preservation-zone&organisation_entity=192&field=reference",
            "dataset": "tree-preservation-zone",
            "assertions": {
                "$.count": 226,
            },
        },
        "Lambeth Tree Zone Lasso Query": {
            "ticket": "https://trello.com/c/elSRI6Hs/21-lambeth-tree-preservation-orders",
            "query": "?geometry=POLYGON((-0.12076377868652344 51.44405766006079,-0.12149333953857419 51.44090126223807,-0.11007785797119139 51.438547196427265,-0.10737419128417967 51.442051500267695,-0.11994838714599608 51.44515432349104,-0.12076377868652344 51.44405766006079))&geometry_relation=intersects&dataset=tree-preservation-zone",  # noqa: E501
            "dataset": "tree-preservation-zone",
            "assertions": {
                "$.count": 5,
            },
        },
        "Lambeth Tree Clarence Avenue": {
            "ticket": "https://trello.com/c/elSRI6Hs/21-lambeth-tree-preservation-orders",
            "query": "?geometry=POINT(-0.133976 51.451147)&geometry_relation=intersects&dataset=tree",
            "dataset": "tree",
            "assertions": {
                "$.count": 1,
                "$.entities[0].address-text": "77A Clarence Avenue London SW4 8LQ",
                "$.entities[0].tree-preservation-order": "105",
                "$.entities[0].tree-preservation-order-tree": "4",
            },
        },
        "Lambeth Tree Lasso Query": {
            "ticket": "https://trello.com/c/elSRI6Hs/21-lambeth-tree-preservation-orders",
            "query": "?geometry=POLYGON((-0.11108636856079102 51.50523659640538,-0.10985255241394042 51.50249181873096,-0.1077711582183838 51.50236492720043,-0.10615110397338867 51.502885848073674,-0.10615110397338867 51.50368725317429,-0.10556101799011232 51.50508300007536,-0.11079668998718263 51.50538351414963,-0.11108636856079102 51.50523659640538))&geometry_relation=intersects&dataset=tree",  # noqa: E501
            "dataset": "tree",
            "assertions": {
                "$.count": 5,
            },
        },
        "Lambeth organisation tree point count": {
            "query": "?dataset=tree&organisation_entity=192",
            "dataset": "tree",
            "assertions": {
                "$.count": 2551,
            },
        },
        "Lambeth district tree point count": {
            "query": "?dataset=tree&geometry_reference=E09000022",
            "dataset": "tree",
            "warnings": {
                "$.count": 2551,
            },
        },
        "Lambeth has no world heritage sites": {
            "ticket": "https://trello.com/c/pGDJsPmN/49-world-heritage-sites",
            "query": "?dataset=world-heritage-site&geometry_reference=E09000022",
            "dataset": "world-heritage-site",
            "assertions": {
                "$.count": 0,
            },
        },
        "Lambeth has no world heritage site buffer zones": {
            "ticket": "https://trello.com/c/pGDJsPmN/49-world-heritage-sites",
            "query": "?dataset=world-heritage-site-buffer-zone&geometry_reference=E09000022",
            "dataset": "world-heritage-site-buffer-zone",
            "assertions": {
                "$.count": 0,
            },
        },
        "Historic Parks and Gardens Norwood Grove": {
            "ticket": "https://trello.com/c/JSTZgrsQ/53-historic-parks-and-gardens",
            "query": "?geometry=POINT(-0.11646267 51.42093317)&geometry_relation=intersects&dataset=park-and-garden",
            "dataset": "park-and-garden",
            "assertions": {
                "$.count": 1,
                "$.entities[0].reference": "1000823",
                "$.entities[0].name": "NORWOOD GROVE",
                "$.entities[0].park-and-garden-grade": "II",
            },
        },
        "Lambeth has no national parks": {
            "ticket": "https://trello.com/c/qUHnNjO2/54-national-park",
            "query": "?dataset=national-park&geometry_reference=E09000022",
            "dataset": "national-park",
            "assertions": {
                "$.count": 0,
            },
        },
    },
    "local-authority-eng:BUC": {
        "Chilterns area of outstanding natural beauty": {
            "ticket": "https://trello.com/c/fwcRbQFr/40-area-of-outstanding-natural-beauty",
            "query": "?geometry=POINT(-0.8463452 51.6682134)&geometry_relation=intersects&dataset=area-of-outstanding-natural-beauty",
            "dataset": "area-of-outstanding-natural-beauty",
            "assertions": {
                "$.count": 1,
                "$.entities[0].reference": "5",
                "$.entities[0].name": "Chilterns",
                "$.entities[0].organisation-entity": "501910",
            },
        },
        "Chilterns area of outstanding natural beauty - RIPA intersection with Tudor Equestrian Center": {
            "ticket": "https://trello.com/c/fwcRbQFr/40-area-of-outstanding-natural-beauty",
            "query": "?geometry=POINT(-0.6303688+51.7342939)&geometry_relation=intersects&dataset=area-of-outstanding-natural-beauty",
            "dataset": "area-of-outstanding-natural-beauty",
            "assertions": {
                "$.count": 1,
                "$.entities[0].reference": "5",
                "$.entities[0].name": "Chilterns",
                "$.entities[0].organisation-entity": "501910",
            },
        },
        "Chilterns article 4 direction": {
            "ticket": "https://trello.com/c/ZGBAQhVP/10-buckinghamshire-article-4-directions",
            "query": "?geometry=POINT(-0.845119 51.667878)&geometry_relation=intersects&dataset=article-4-direction-area",
            "dataset": "article-4-direction-area",
            "assertions": {
                "$.count": 1,
                "$.entities[0].name": "Former Wycombe Rural District - Poultry Production",
                "$.entities[0].description": "Certain structures used for production of poultry or eggs - refer to Order & GDO 1950",
            },
        },
        "Chorleywood Article 4 direction, outside of Buckinghamshire": {
            "ticket": "https://trello.com/c/ZGBAQhVP/10-buckinghamshire-article-4-directions",
            "query": "?geometry=POINT(-0.53418646 51.65627576)&geometry_relation=intersects&dataset=article-4-direction-area",
            "dataset": "article-4-direction-area",
            "warnings": {
                "$.count": 1,
            },
        },
        "Land north of Burton's Lane Article 4 direction, outside of Buckinghamshire": {
            "ticket": "https://trello.com/c/ZGBAQhVP/10-buckinghamshire-article-4-directions",
            "query": "?geometry=POINT(-0.51872219 51.66143563)&geometry_relation=intersects&dataset=article-4-direction-area",
            "dataset": "article-4-direction-area",
            "warnings": {
                "$.count": 1,
            },
        },
        "Buckinghamshire Article 4 Direction NE of Wycombe Heath Farm": {
            "ticket": "https://trello.com/c/ZGBAQhVP/10-buckinghamshire-article-4-directions",
            "query": "?geometry=POINT(-0.70412678 51.67024811)&geometry_relation=intersects&dataset=article-4-direction-area",
            "dataset": "article-4-direction-area",
            "assertions": {
                "$.count": 3,
                "$.entities[0].name": "Whole District excluding the Town of Chesham - Poultry production.",
                "$.entities[1].name": "Land at Spurlands End, Beech Tree Road cross-roads - means of enclosure.",
                "$.entities[2].name": "Land at Spurlands End, Beech Tree Road cross-roads - caravan sites.",
            },
        },
        "South Buckinghamshire Development Article 4 Direction hacked into the name": {
            "ticket": "https://trello.com/c/ZGBAQhVP/10-buckinghamshire-article-4-directions",
            "query": "?dataset=article-4-direction-area&organisation=local-authority-eng:BUC&reference=DO.34",
            "dataset": "article-4-direction-area",
            "assertions": {
                "$.count": 1,
                "$.entities[0].name": "Land West of Mansion Lane, Immediately South of Iverdale Close, Iver - Development",
            },
        },
        "South Buckinghamshire Argricultural Article 4 Direction hacked into the name": {
            "ticket": "https://trello.com/c/ZGBAQhVP/10-buckinghamshire-article-4-directions",
            "query": "?dataset=article-4-direction-area&organisation=local-authority-eng:BUC&reference=DO.7",
            "dataset": "article-4-direction-area",
            "assertions": {
                "$.count": 1,
                "$.entities[0].name": "Land on the North Side of Seven Hills Road, Iver - Agricultural",
            },
        },
        "Article 4 Land off Copperkins Lane (should have areas for rules Means of enclosure and Caravan Sites)": {
            "ticket": "https://trello.com/c/ZGBAQhVP/10-buckinghamshire-article-4-directions",
            "query": "?geometry=POINT(-0.62319097 51.68831210)&geometry_relation=intersects&dataset=article-4-direction-area",
            "dataset": "article-4-direction-area",
            "warnings": {
                "$.count": 3,
            },
        },
        "Article 4 Alderbourne Farm (shape disagreement)": {
            "ticket": "https://trello.com/c/ZGBAQhVP/10-buckinghamshire-article-4-directions",
            "query": "?geometry=POINT(-0.62319097 51.68831210)&geometry_relation=intersects&dataset=article-4-direction-area",
            "dataset": "article-4-direction-area",
            "warnings": {
                "$.count": 1,
            },
        },
        "Article 4 Land West of Mansion Lane - immediately to the west and south row of cottages No's 110-148": {
            "ticket": "https://trello.com/c/ZGBAQhVP/10-buckinghamshire-article-4-directions",
            "query": "?geometry=POINT(-0.52649740 51.51431737)&geometry_relation=intersects&dataset=article-4-direction-area",
            "dataset": "article-4-direction-area",
            "warnings": {
                "$.count": 1,
            },
        },
        "Article 4 Land West of Mansion Lane - 'dev type' patch values check": {
            "ticket": "https://trello.com/c/ZGBAQhVP/10-buckinghamshire-article-4-directions",
            "query": "?geometry=POINT(-0.52649001 51.51644676)&geometry_relation=intersects&dataset=article-4-direction-area",
            "dataset": "article-4-direction-area",
            "warnings": {
                "$.count": 1,
                "$.entities[0].name": "Land West of Mansion Lane, Immediately South of Iverdale Close, Iver - Development",
            },
        },
        "Buckinghamshire scheduled monument": {
            "ticket": "https://trello.com/c/xhCLfQ7r/38-scheduled-monuments",
            "query": "?geometry=POINT (-0.835789 51.724111)&geometry_relation=intersects&dataset=scheduled-monument",
            "dataset": "scheduled-monument",
            "assertions": {
                "$.count": 1,
                "$.entities[0].reference": "1006951",
                "$.entities[0].name": "The Mount",
            },
        },
        "Buckinghamshire has no central activities zone": {
            "ticket": "https://trello.com/c/golBkjM7/39-central-activities-zone",
            "query": "?dataset=central-activities-zone&geometry_reference=E06000060",
            "dataset": "central-activities-zone",
            "assertions": {
                "$.count": 0,
            },
        },
        "Whiteleaf tree preservation zone": {
            "ticket": "https://trello.com/c/VEYLoXrJ/13-buckinghamshire-tree-preservation-orders",
            "query": "?geometry=POINT(-0.813461 51.732499)&geometry_relation=intersects&dataset=tree-preservation-zone",
            "dataset": "tree-preservation-zone",
            "assertions": {
                "$.count": 1,
            },
        },
        "High Wycombe tree preservation zone": {
            "ticket": "https://trello.com/c/VEYLoXrJ/13-buckinghamshire-tree-preservation-orders",
            "query": "?geometry=POINT(-0.895052 51.558892)&geometry_relation=intersects&dataset=tree-preservation-zone",
            "dataset": "tree-preservation-zone",
            "assertions": {
                "$.count": 2,
                "$.entities[0].tree-preservation-order": "04/1952",
                "$.entities[1].tree-preservation-order": "01/1955",
            },
        },
        "Tree Preservation Zone South Bucks": {
            "ticket": "https://trello.com/c/VEYLoXrJ/13-buckinghamshire-tree-preservation-orders",
            "query": "?geometry=POINT(-0.65957350 51.55059663)&geometry_relation=intersects&dataset=tree-preservation-zone",
            "dataset": "tree-preservation-zone",
            "assertions": {
                "$.count": 1,
                "$.entities[0].tree-preservation-order": "TPO/SBDC/2012/06",
            },
        },
        "Tree Preservation Zone Wycombe": {
            "ticket": "https://trello.com/c/VEYLoXrJ/13-buckinghamshire-tree-preservation-orders",
            "query": "?geometry=POINT(-0.70629442 51.60474864)&geometry_relation=intersects&dataset=tree-preservation-zone",
            "dataset": "tree-preservation-zone",
            "assertions": {
                "$.count": 1,
                "$.entities[0].tree-preservation-order": "07/1951",
            },
        },
        "Tree Preservation Zone Chiltern": {
            "ticket": "https://trello.com/c/VEYLoXrJ/13-buckinghamshire-tree-preservation-orders",
            "query": "?geometry=POINT(-0.57478739 51.67255292)&geometry_relation=intersects&dataset=tree-preservation-zone",
            "dataset": "tree-preservation-zone",
            "assertions": {
                "$.count": 1,
                "$.entities[0].tree-preservation-order": "TPO/1949/010",
            },
        },
        "Tree Preservation Zone Aylebury Vale": {
            "ticket": "https://trello.com/c/VEYLoXrJ/13-buckinghamshire-tree-preservation-orders",
            "query": "?geometry=POINT(-0.91122750 51.94784157)&geometry_relation=intersects&dataset=tree-preservation-zone",
            "dataset": "tree-preservation-zone",
            "assertions": {
                "$.count": 1,
                "$.entities[0].tree-preservation-order": "(Amendment Order) No. 1 1961",
            },
        },
        "Great Missenden conservation area": {
            "ticket": "https://trello.com/c/Z5qZj1w7/11-buckinghamshire-conservation-areas",
            "query": "?geometry=POINT(-0.700567 51.699685)&geometry_relation=intersects&dataset=conservation-area",
            "dataset": "conservation-area",
            "assertions": {
                "$.count": 1,
                "$.entities[0].name": "Great Missenden",
            },
            "warnings": {
                "$.entities[0].organisation-entity": "67",
            },
        },
        "Buckinghamshire Tree lasso query Beaconsfield Gregories Road": {
            "ticket": "https://trello.com/c/VEYLoXrJ/13-buckinghamshire-tree-preservation-orders",
            "query": "?geometry=POLYGON((-0.6642436981201171 51.61042174813102,-0.6646513938903809 51.609369035138144,-0.6634712219238282 51.60950895409454,-0.6625807285308838 51.60978879071354,-0.6615400314331055 51.61006196289202,-0.6606495380401611 51.610161903522226,-0.6599736213684081 51.61026850661858,-0.6598341464996339 51.61023519317786,-0.6593406200408936 51.61082150616335,-0.6593728065490723 51.61096808322645,-0.6642436981201171 51.61042174813102))&geometry_relation=intersects&dataset=tree",  # noqa: E501
            "dataset": "tree",
            "assertions": {
                "$.count": 48,
            },
        },
        "Listed Building Lasso query": {
            "ticket": "https://trello.com/c/HrxISbnM/44-buckinghamshire-listed-building-outlines",
            "query": "?geometry=POLYGON%28%28-0.7748794555664062%2051.679793621379986%2C-0.7728195190429689%2051.62526373476129%2C-0.7137680053710938%2051.6220665895049%2C-0.6804656982421875%2051.63613234359897%2C-0.7048416137695312%2051.655092894606554%2C-0.6832122802734374%2051.66254711886705%2C-0.6928253173828126%2051.67723899831586%2C-0.7250976562500001%2051.666806125075425%2C-0.7429504394531249%2051.647850474028985%2C-0.751190185546875%2051.65296289102838%2C-0.7436370849609375%2051.67638742526901%2C-0.7748794555664062%2051.679793621379986%29%29&geometry_relation=intersects&dataset=listed-building-outline",  # noqa: E501
            "dataset": "listed-building-outline",
            "assertions": {
                "$.count": 180,
            },
        },
        "Listed Building Lasso query Aylesbury": {
            "ticket": "https://trello.com/c/HrxISbnM/44-buckinghamshire-listed-building-outlines",
            "query": "?geometry=POLYGON%28%28-0.824146270751953%2051.82967793410063%2C-0.8313560485839843%2051.82904140792331%2C-0.840625762939453%2051.832064827148116%2C-0.8463764190673827%2051.830155322830194%2C-0.8505821228027342%2051.82734396080437%2C-0.8610534667968749%2051.82681349546081%2C-0.8547019958496093%2051.81949243574658%2C-0.8365917205810547%2051.80930463429536%2C-0.8321285247802732%2051.8073410953632%2C-0.8297252655029294%2051.80351990955802%2C-0.8269786834716796%2051.80219303316994%2C-0.8266353607177733%2051.79932684689146%2C-0.8237171173095702%2051.79661972587732%2C-0.821399688720703%2051.7960888987767%2C-0.8215713500976561%2051.79322232445378%2C-0.8084392547607422%2051.79279763127906%2C-0.7793426513671874%2051.80123765798905%2C-0.7634639739990234%2051.806014331445056%2C-0.7657814025878906%2051.814558007036936%2C-0.7718753814697265%2051.82198597374219%2C-0.7626056671142577%2051.824691571614494%2C-0.7644081115722655%2051.83291346974673%2C-0.7765102386474608%2051.83885352017006%2C-0.7965946197509763%2051.834186403659885%2C-0.7946205139160155%2051.82973097754268%2C-0.7991695404052733%2051.83020836571001%2C-0.804920196533203%2051.83991416100463%2C-0.8338451385498044%2051.83768678639302%2C-0.824146270751953%2051.82967793410063%29%29&geometry_relation=intersects&dataset=listed-building-outline",  # noqa: E501
            "dataset": "listed-building-outline",
            "assertions": {
                "$.count": 202,
            },
        },
        "Listed Building The White Hart": {
            "ticket": "https://trello.com/c/HrxISbnM/44-buckinghamshire-listed-building-outlines",
            "query": "?geometry=POINT(-0.83952570 51.80430260)&geometry_relation=intersects&dataset=listed-building-outline",
            "dataset": "listed-building-outline",
            "assertions": {
                "$.count": 1,
                "$.entities[0].listed-building-grade": "II",
            },
            "warnings": {
                "$.entities[0].name": "The White Hart",
            },
        },
        "Listed Building Lasso query 108 high Street Amersham": {
            "ticket": "https://trello.com/c/HrxISbnM/44-buckinghamshire-listed-building-outlines",
            "query": "?geometry=POLYGON+((-0.621533542871487+51.6675929991994,+-0.6214410066604732+51.667565550332085,+-0.6216515600681422+51.66731351904605,+-0.6217360496521112+51.66733847270126,+-0.6217011809349176+51.667383389246,+-0.6217132508754845+51.66741000643671,+-0.6216582655906793+51.667472390416094,+-0.621533542871487+51.6675929991994))&geometry_relation=intersects&dataset=listed-building-outline",
            "dataset": "listed-building-outline",
            "assertions": {
                "$.count": 2,
                "$.entities[0].listed-building-grade": "II",
                "$.entities[1].listed-building-grade": "II",
            },
        },
        "Listed Building Johnsons Farm Chesham": {
            "ticket": "https://trello.com/c/HrxISbnM/44-buckinghamshire-listed-building-outlines",
            "query": "?geometry=POINT(-0.6303688+51.7342939)&geometry_relation=intersects&dataset=listed-building-outline",
            "dataset": "listed-building-outline",
            "assertions": {
                "$.count": 1,
                "$.entities[0].listed-building-grade": "II",
            },
        },
        "Listed Building Projection Error (should not be present)": {
            "ticket": "https://trello.com/c/HrxISbnM/44-buckinghamshire-listed-building-outlines",
            "query": "?geometry=POINT(-0.78024744 51.75966723)&geometry_relation=intersects&dataset=listed-building-outline",
            "dataset": "listed-building-outline",
            "assertions": {
                "$.count": 0,
            },
        },
        "Bacombe and Coombe Hills SSSI": {
            "ticket": "https://trello.com/c/r3wV6tXO/50-sites-of-special-and-or-scientific-interest",
            "query": "?longitude=-0.765907&latitude=51.75339&dataset=site-of-special-scientific-interest",
            "dataset": "site-of-special-scientific-interest",
            "assertions": {
                "$.count": 1,
                "$.entities[0].reference": "SP852067",
                "$.entities[0].name": "Bacombe and Coombe Hills",
            },
        },
        "Ashridge Commons and Woods SSSI": {
            "ticket": "https://trello.com/c/r3wV6tXO/50-sites-of-special-and-or-scientific-interest",
            "query": "?geometry=POINT(-0.58446024 51.81259055)&geometry_relation=intersects&dataset=site-of-special-scientific-interest",
            "dataset": "site-of-special-scientific-interest",
            "assertions": {
                "$.count": 1,
                "$.entities[0].name": "Ashridge Commons and Woods",
            },
        },
        "Grangelands & Pulpit Hill SSSI": {
            "ticket": "https://trello.com/c/r3wV6tXO/50-sites-of-special-and-or-scientific-interest",
            "query": "?geometry=POINT(-0.80011162 51.73627579)&geometry_relation=intersects&dataset=site-of-special-scientific-interest",
            "dataset": "site-of-special-scientific-interest",
            "assertions": {
                "$.count": 1,
                "$.entities[0].name": "Grangelands & Pulpit Hill",
            },
        },
        "SSSI Overall Count": {
            "ticket": "https://trello.com/c/r3wV6tXO/50-sites-of-special-and-or-scientific-interest",
            "query": "?dataset=site-of-special-scientific-interest&field=reference",
            "dataset": "site-of-special-scientific-interest",
            "assertions": {
                "$.count": 9608,
            },
        },
        "Buckinghamshire has no world heritage sites": {
            "ticket": "https://trello.com/c/pGDJsPmN/49-world-heritage-sites",
            "query": "?dataset=world-heritage-site&geometry_reference=E06000060",
            "dataset": "world-heritage-site",
            "assertions": {
                "$.count": 0,
            },
        },
        "Buckinghamshire has no world heritage site buffer zones": {
            "ticket": "https://trello.com/c/pGDJsPmN/49-world-heritage-sites",
            "query": "?dataset=world-heritage-site-buffer-zone&geometry_reference=E06000060",
            "dataset": "world-heritage-site-buffer-zone",
            "assertions": {
                "$.count": 0,
            },
        },
        "Historic Parks and Gardens Cliveden, Dropmore and Hedsor Lasso query": {
            "ticket": "https://trello.com/c/JSTZgrsQ/53-historic-parks-and-gardens",
            "query": "?geometry=POLYGON((-0.6853151321411134 51.56351904151961,-0.6875038146972657 51.56098454382348,-0.6801223754882814 51.55847658600979,-0.6766033172607422 51.560557667154285,-0.6821393966674806 51.56373246645586,-0.6853151321411134 51.56351904151961))&geometry_relation=intersects&dataset=park-and-garden",
            "dataset": "park-and-garden",
            "assertions": {
                "$.count": 3,
                "$.entities[0].reference": "1000323",
                "$.entities[0].name": "CLIVEDEN",
                "$.entities[0].park-and-garden-grade": "I",
                "$.entities[1].reference": "1000599",
                "$.entities[1].name": "DROPMORE",
                "$.entities[1].park-and-garden-grade": "II",
                "$.entities[2].reference": "1001373",
                "$.entities[2].name": "HEDSOR HOUSE",
                "$.entities[2].park-and-garden-grade": "II",
            },
        },
        "Park and Garden Overall Count": {
            "ticket": "https://trello.com/c/JSTZgrsQ/53-historic-parks-and-gardens",
            "query": "?dataset=park-and-garden",
            "dataset": "park-and-garden",
            "assertions": {
                "$.count": 1699,
            },
        },
        "Buckinghamshire has no national parks": {
            "ticket": "https://trello.com/c/qUHnNjO2/54-national-park",
            "query": "?dataset=national-park&geometry_reference=E06000060",
            "dataset": "national-park",
            "assertions": {
                "$.count": 0,
            },
        },
    },
    "local-authority-eng:SWK": {
        "Southwark central activities zone": {
            "ticket": "https://trello.com/c/golBkjM7/39-central-activities-zone",
            "query": "?geometry=POINT(-0.0909083 51.5070023)&geometry_relation=intersects&dataset=central-activities-zone",
            "dataset": "central-activities-zone",
            "assertions": {
                "$.count": 1,
                "$.entities[0].reference": "CAZ00000002",
            },
        },
        "Southwark conservation area (Borough High Street)": {
            "ticket": "https://trello.com/c/mdJYWSdO/42-southwark-conservation-areas",
            "query": "?geometry=POINT(-0.0909083 51.5070023)&geometry_relation=intersects&dataset=conservation-area",
            "dataset": "conservation-area",
            "assertions": {
                "$.count": 1,
                "$.entities[0].reference": "3",
                "$.entities[0].name": "Borough High Street",
                "$.entities[0].organisation-entity": "329",
            },
        },
        "Southwark conservation area (Sunray Estate)": {
            "ticket": "https://trello.com/c/mdJYWSdO/42-southwark-conservation-areas",
            "query": "?geometry=POINT(-0.0915479+51.4582278)&geometry_relation=intersects&dataset=conservation-area",
            "dataset": "conservation-area",
            "assertions": {
                "$.count": 1,
                "$.entities[0].name": "Sunray Estate",
            },
        },
        "Southwark scheduled monument (Clink Street)": {
            "ticket": "https://trello.com/c/xhCLfQ7r/38-scheduled-monuments",
            "query": "?geometry=POINT(-0.0909083 51.5070023)&geometry_relation=intersects&dataset=scheduled-monument",
            "dataset": "scheduled-monument",
            "assertions": {
                "$.count": 1,
                "$.entities[0].reference": "1002054",
                "$.entities[0].name": "Remains of Winchester Palace, Clink Street and waterfront",
            },
        },
        "Southwark scheduled monument (Abbey Buildings Bermondsey Projection check - should be present)": {
            "ticket": "https://trello.com/c/xhCLfQ7r/38-scheduled-monuments",
            "query": "?geometry=POINT(-0.08158144 51.49728412)&geometry_relation=intersects&dataset=scheduled-monument",
            "dataset": "scheduled-monument",
            "assertions": {
                "$.count": 1,
                "$.entities[0].reference": "1001984",
                "$.entities[0].name": "Abbey buildings, Bermondsey",
            },
        },
        "Southwark scheduled monument (Abbey Buildings Bermondsey Projection check - should not be present)": {
            "ticket": "https://trello.com/c/xhCLfQ7r/38-scheduled-monuments",
            "query": "?geometry=POINT(-0.08187930 51.49727324)&geometry_relation=intersects&dataset=scheduled-monument",
            "dataset": "scheduled-monument",
            "assertions": {
                "$.count": 0,
            },
        },
        "Southwark scheduled monument": {
            "ticket": "https://trello.com/c/xhCLfQ7r/38-scheduled-monuments",
            "query": "?geometry=POINT(-0.052963 51.501611)&geometry_relation=intersects&dataset=scheduled-monument",
            "dataset": "scheduled-monument",
            "assertions": {
                "$.count": 1,
                "$.entities[0].reference": "1005556",
                "$.entities[0].name": "Pumping engine house for Brunel's Thames tunnel",
            },
        },
        "Southwark listed building (Church of St Peter)": {
            "query": "?geometry=POINT(-0.092645 51.486573)&geometry_relation=intersects&dataset=listed-building-outline",
            "dataset": "listed-building-outline",
            "assertions": {
                "$.count": 1,
                "$.entities[0].name": "Church of St Peter",
                "$.entities[0].listed-building-grade": "I",
            },
        },
        "Southwark grade II listed building (Cobourg Road) - point search": {
            "ticket": "https://trello.com/c/KYZUfnWw/5-add-tests-for-ripa-sample-addresses-expected-constraints",
            "query": "?entries=current&geometry=POINT(-0.0760466 51.4859056)&geometry_relation=intersects&limit=100&dataset=article-4-direction-area&dataset=central-activities-zone&dataset=listed-building&dataset=listed-building-outline&dataset=locally-listed-building&dataset=conservation-area&dataset=area-of-outstanding-natural-beauty&dataset=national-park&dataset=world-heritage-site&dataset=scheduled-monument&dataset=tree-preservation-zone&dataset=site-of-special-scientific-interest",  # noqa: E501
            "dataset": "listed-building-outline",
            "assertions": {
                "$.count": 2,
                "$.entities[0].name": "Cobourg Road",
                "$.entities[0].dataset": "conservation-area",
                "$.entities[1].dataset": "listed-building-outline",
                "$.entities[1].listed-building-grade": "II",
            },
        },
        "Southwark grade II listed building (Cobourg Road) - lasso search": {
            "ticket": "https://trello.com/c/KYZUfnWw/5-add-tests-for-ripa-sample-addresses-expected-constraints",
            "query": "?entries=current&geometry=POLYGON ((-0.07629960316337962 51.48596216740805, -0.07631450428819368 51.485912060522, -0.07554858463920969 51.48584896289475, -0.07553666367387485 51.48590092561696, -0.07629960316337962 51.48596216740805))&geometry_relation=intersects&limit=100&dataset=article-4-direction-area&dataset=central-activities-zone&dataset=listed-building&dataset=listed-building-outline&dataset=locally-listed-building&dataset=conservation-area&dataset=area-of-outstanding-natural-beauty&dataset=national-park&dataset=world-heritage-site&dataset=scheduled-monument&dataset=tree-preservation-zone&dataset=site-of-special-scientific-interest",  # noqa: E501
            "dataset": "listed-building-outline",
            "assertions": {
                "$.count": 4,
                "$.entities[0].name": "Cobourg Road",
                "$.entities[0].dataset": "conservation-area",
                "$.entities[1].name": "School Nature Area, Cobourg Road",
                "$.entities[1].dataset": "tree-preservation-zone",
                "$.entities[1].tree-preservation-order": "228",
                "$.entities[2].name": "47, COBOURG ROAD",
                "$.entities[2].dataset": "listed-building",
                "$.entities[3].dataset": "listed-building-outline",
                "$.entities[3].listed-building-grade": "II",
            },
        },
        "Southwark grade II listed building (Clandon House, Boyfield Street estate) - RIPA lasso search": {
            "ticket": "https://trello.com/c/KYZUfnWw/5-add-tests-for-ripa-sample-addresses-expected-constraints",
            "query": "?entries=current&geometry=POLYGON+((-0.10233910674591064+51.500670381103276,+-0.10251613254089353+51.500593575307306,+-0.10211380118865966+51.50023292027359,+-0.10193677539367675+51.500316405488945,+-0.10233910674591064+51.500670381103276))&geometry_relation=intersects&limit=100&dataset=listed-building-outline",
            "dataset": "listed-building-outline",
            "assertions": {
                "$.count": 1,
                "$.entities[0].name": "Clandon House, Boyfield Street estate",
                "$.entities[0].dataset": "listed-building-outline",
                "$.entities[0].listed-building-grade": "II",
            },
        },
        "Southwark grade I listed building (Southwark Cathedral) - RIPA lasso search": {
            "ticket": "https://trello.com/c/KYZUfnWw/5-add-tests-for-ripa-sample-addresses-expected-constraints",
            "query": "?entries=current&geometry=POLYGON+((-0.08992591415557859+51.506488463344624,+-0.09011903320465087+51.50615790576995,+-0.08914807354125977+51.50592083774984,+-0.08899250541839598+51.50608778718822,+-0.08936265026245116+51.50617793963059,+-0.08928218399200438+51.50638495567512,+-0.08992591415557859+51.506488463344624))&geometry_relation=intersects&limit=100&dataset=listed-building-outline",
            "dataset": "listed-building-outline",
            "assertions": {
                "$.count": 1,
                "$.entities[0].name": "Cathedral church of St Saviour and St Mary Overie (Southwark Cathedral)",
                "$.entities[0].dataset": "listed-building-outline",
                "$.entities[0].listed-building-grade": "I",
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
                "$.entities[2].description": "Demolition of commercial buildings and construction of new dwellinghouses is restricted",
                "$.entities[2].organisation-entity": "329",
                "$.entities[3].name": "Bankside and Borough District Town Centre",
                "$.entities[3].description": "Demolition of commercial buildings and construction of new dwellinghouses is restricted",
                "$.entities[3].organisation-entity": "329",
                "$.entities[4].name": "Central Activities Zone",
                "$.entities[4].description": "Change of use from Class E to residential is restricted",
                "$.entities[4].organisation-entity": "329",
                "$.entities[5].name": "Bankside and Borough District Town Centre",
                "$.entities[5].description": "Change of use from Class E to residential is restricted",
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
                "$.entities[1].description": "Demolition of commercial buildings and construction of new dwellinghouses is restricted",
                "$.entities[1].organisation-entity": "329",
                "$.entities[2].name": "Old Kent Road North District Town Centre",
                "$.entities[2].description": "Change of use from Class E to residential is restricted",
                "$.entities[2].organisation-entity": "329",
                "$.entities[3].name": "Protected shopping frontage SF24: Old Kent Road, East Street and Dunton Road",
                "$.entities[3].description": "Change of use from Class E to residential is restricted",
                "$.entities[3].organisation-entity": "329",
            },
        },
        "Southwark article 4 direction (Railway arches)": {
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
                "$.entities[2].description": "Demolition of commercial buildings and construction of new dwellinghouses is restricted",
                "$.entities[3].name": "Site allocation NSP20: Southwark Station and 1 Joan Street",
                "$.entities[3].description": "Demolition of commercial buildings and construction of new dwellinghouses is restricted",
                "$.entities[4].name": "Bankside and Borough District Town Centre",
                "$.entities[4].description": "Demolition of commercial buildings and construction of new dwellinghouses is restricted",
                "$.entities[5].name": "Central Activities Zone",
                "$.entities[5].description": "Change of use from Class E to residential is restricted",
                "$.entities[6].name": "Site allocation NSP20: Southwark Station and 1 Joan Street",
                "$.entities[7].name": "Bankside and Borough District Town Centre",
                "$.entities[7].description": "Change of use from Class E to residential is restricted",
                "$.entities[8].name": "Railway Arches",
                "$.entities[8].description": "Change of use from Class E to residential is restricted",
            },
        },
        "Southwark has no areas of outstanding natural beauty": {
            "ticket": "https://trello.com/c/fwcRbQFr/40-area-of-outstanding-natural-beauty",
            "query": "?dataset=area-of-outstanding-natural-beauty&geometry_reference=E09000028",
            "dataset": "area-of-outstanding-natural-beauty",
            "assertions": {
                "$.count": 0,
            },
        },
        "Southwark has no SSSI": {
            "ticket": "https://trello.com/c/r3wV6tXO/50-sites-of-special-and-or-scientific-interest",
            "query": "?dataset=site-of-special-scientific-interest&geometry_reference=E09000028",
            "dataset": "site-of-special-scientific-interest",
            "assertions": {
                "$.count": 0,
            },
        },
        "Southwark has no world heritage sites": {
            "ticket": "https://trello.com/c/pGDJsPmN/49-world-heritage-sites",
            "query": "?dataset=world-heritage-site&geometry_reference=E09000028",
            "dataset": "world-heritage-site",
            "assertions": {
                "$.count": 0,
            },
        },
        "Southwark has no world heritage site buffer zones": {
            "ticket": "https://trello.com/c/pGDJsPmN/49-world-heritage-sites",
            "query": "?dataset=world-heritage-site-buffer-zone&geometry_reference=E09000028",
            "dataset": "world-heritage-site-buffer-zone",
            "assertions": {
                "$.count": 0,
            },
        },
        "St Josephs School tree preservation zone": {
            "ticket": "https://trello.com/c/1tSMgQDH/25-southwark-tree-preservation-orders",
            "query": "?geometry=POINT(-0.069719 51.499471)&geometry_relation=intersects&dataset=tree-preservation-zone",
            "dataset": "tree-preservation-zone",
            "assertions": {
                "$.count": 1,
                "$.entities[0].name": "St Josephs Primary School, George Row",
                "$.entities[0].tree-preservation-order": "252",
            },
        },
        "Southwark Tree Overall Count": {
            "ticket": "https://trello.com/c/wfDMDuPV/46-southwark-tree-preservation-orders",
            "query": "?dataset=tree&organisation_entity=329&field=reference",
            "dataset": "tree",
            "assertions": {
                "$.count": 0,
            },
        },
        "Historic Parks and Gardens SOUTHWARK PARK": {
            "ticket": "https://trello.com/c/JSTZgrsQ/53-historic-parks-and-gardens",
            "query": "?geometry=POINT(-0.05105192 51.49368638)&geometry_relation=intersects&dataset=park-and-garden",
            "dataset": "park-and-garden",
            "assertions": {
                "$.count": 1,
                "$.entities[0].reference": "1000838",
                "$.entities[0].name": "SOUTHWARK PARK",
                "$.entities[0].park-and-garden-grade": "II",
            },
        },
        "Southwark has no national parks": {
            "ticket": "https://trello.com/c/qUHnNjO2/54-national-park",
            "query": "?dataset=national-park&geometry_reference=E09000028",
            "dataset": "national-park",
            "assertions": {
                "$.count": 0,
            },
        },
    },
    "local-authority-eng:CAT": {
        "Canterbury article 4 direction (Kemberland Wood)": {
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
        "Canterbury article 4 direction (Herne Bay)": {
            "ticket": "https://trello.com/c/prY4jzj6/14-canterbury-article-4-directions",
            "query": "?dataset=article-4-direction-area&longitude=1.12258974&latitude=51.36587529",
            "dataset": "article-4-direction-area",
            "assertions": {
                "$.count": 1,
                "$.entities[0].name": "Dwelling houses in Herne Bay Conservation Area",
                "$.entities[0].organisation-entity": "75",
                "$.entities[0].start-date": "1997-06-29",
                "$.entities[0].organisation-entity": "75",
                "$.entities[0].notes": "Check to see if A4D applies",
                "$.entities[0].reference": "73408",
            },
        },
        "Canterbury article 4 direction (Simplification)": {
            "ticket": "https://trello.com/c/prY4jzj6/14-canterbury-article-4-directions",
            "query": "?dataset=article-4-direction-area&longitude=1.12258755&latitude=51.36586015",
            "dataset": "article-4-direction-area",
            "assertions": {
                "$.count": 0,
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
            "ticket": "https://trello.com/c/xhCLfQ7r/38-scheduled-monuments",
            "query": "?geometry=POINT(1.07739 51.277722)&geometry_relation=intersects&dataset=scheduled-monument",
            "dataset": "scheduled-monument",
            "assertions": {
                "$.count": 1,
                "$.entities[0].reference": "1003125",
                "$.entities[0].name": "Vacant land within Roman walls in Adelaide Place",
            },
        },
        "Kent Downs area of outstanding natural beauty": {
            "ticket": "https://trello.com/c/fwcRbQFr/40-area-of-outstanding-natural-beauty",
            "query": "?dataset=area-of-outstanding-natural-beauty&latitude=51.3869143&longitude=0.4540133",
            "dataset": "area-of-outstanding-natural-beauty",
            "assertions": {
                "$.count": 1,
                "$.entities[0].name": "Kent Downs",
            },
        },
        "Canterbury has no central activities zone": {
            "ticket": "https://trello.com/c/golBkjM7/39-central-activities-zone",
            "query": "?dataset=central-activities-zone&geometry_reference=E07000106",
            "dataset": "central-activities-zone",
            "assertions": {
                "$.count": 0,
            },
        },
        "Whitstable town conservation area": {
            "ticket": "https://trello.com/c/9TaHoPOe/15-canterbury-conservation-areas",
            "query": "?geometry=POINT(1.023993 51.35794)&geometry_relation=intersects&dataset=conservation-area",
            "dataset": "conservation-area",
            "assertions": {
                "$.count": 1,
                "$.entities[0].reference": "175",
                "$.entities[0].name": "WHITSTABLE TOWN",
                "$.entities[0].organisation-entity": "75",
            },
        },
        "Canterbury conservation area publisher count": {
            "ticket": "https://trello.com/c/9TaHoPOe/15-canterbury-conservation-areas",
            "query": "?dataset=conservation-area&organisation_entity=75",
            "dataset": "conservation-area",
            "warnings": {
                "$.count": 97,
            },
        },
        "Canterbury conservation area count": {
            "ticket": "https://trello.com/c/9TaHoPOe/15-canterbury-conservation-areas",
            "query": "?dataset=conservation-area&geometry_reference=E07000106",
            "dataset": "conservation-area",
            "warnings": {
                "$.count": 97,
            },
        },
        "Canterbury Conservation Area - Martyrs Field": {
            "ticket": "https://trello.com/c/9TaHoPOe/15-canterbury-conservation-areas",
            "query": "?geometry=POINT(1.07541065 51.27274810)&geometry_relation=intersects&dataset=conservation-area",
            "dataset": "conservation-area",
            "assertions": {
                "$.count": 1,
            },
            "warnings": {
                "$.entities[0].reference": "180",
                "$.entities[0].name": "MARTYRS FIELD",
                "$.entities[0].organisation-entity": "75",
            },
        },
        "Canterbury Conservation Area - Scotland Hills Lasso Query": {
            "ticket": "https://trello.com/c/9TaHoPOe/15-canterbury-conservation-areas",
            "query": "?geometry=POLYGON((1.101851463317871 51.2796355780913,1.1080741882324219 51.27195743631006,1.1237382888793945 51.2739979068692,1.1287164688110352 51.28733927660818,1.101851463317871 51.2796355780913))&geometry_relation=intersects&dataset=conservation-area",  # noqa: E501
            "dataset": "conservation-area",
            "assertions": {
                "$.count": 3,
                "$.entities[0].reference": "107",
                "$.entities[0].name": "ST MARTINS HOSPITAL ( CANTERBURY )",
                "$.entities[0].organisation-entity": "75",
                "$.entities[1].reference": "108",
                "$.entities[1].name": "MOUNT HOSPITAL",
                "$.entities[1].organisation-entity": "75",
                "$.entities[2].reference": "155",
                "$.entities[2].name": "LITTLE BARTON FARM ( CANTERBURY )",
                "$.entities[2].organisation-entity": "75",
            },
        },
        "tree preservation zone": {
            "ticket": "https://trello.com/c/qVcURTVE/17-canterbury-tree-preservation-orders",
            "query": "?geometry=POINT(1.149543 51.277888)&geometry_relation=intersects&dataset=tree-preservation-zone",
            "dataset": "tree-preservation-zone",
            "assertions": {
                "$.count": 1,
                "$.entities[0].name": "Land Next To Littlebourne Solar Farm Swanton Lane Littlbourne",
                "$.entities[0].tree-preservation-order": "5/1991/LIT",
            },
        },
        "Canterbury Tree Preservation Zone (Forstal Road)": {
            "ticket": "https://trello.com/c/qVcURTVE/17-canterbury-tree-preservation-orders",
            "query": "?dataset=tree-preservation-zone&longitude=1.19443759&latitude=51.20739400",
            "dataset": "tree-preservation-zone",
            "assertions": {
                "$.count": 1,
                "$.entities[0].name": "Land Surrounding Old Post Office Forstal Road Womenswold CT4 6SU",
                "$.entities[0].organisation-entity": "75",
                "$.entities[0].tree-preservation-order": "6/1970/WOM",
                "$.entities[0].reference": "6/1970/WOM/A1",
            },
        },
        "Canterbury Tree Preservation Zone (Various Locations 2 records)": {
            "ticket": "https://trello.com/c/qVcURTVE/17-canterbury-tree-preservation-orders",
            "query": "?dataset=tree-preservation-zone&longitude=1.01569482&latitude=51.33891848",
            "dataset": "tree-preservation-zone",
            "assertions": {
                "$.count": 2,
                "$.entities[0].name": "Various Locations Near To Broadview Wraik Hill Whitstable CT5 3BY",
                "$.entities[0].organisation-entity": "75",
                "$.entities[0].tree-preservation-order": "1/1965/WHI",
                "$.entities[1].name": "Various Locations Along Willow Road Whitstable CT5 3DW",
                "$.entities[1].organisation-entity": "75",
                "$.entities[1].tree-preservation-order": "2/1989/WHI",
            },
        },
        "Canterbury Tree Preservation Zone (16 Albion Lane)": {
            "ticket": "https://trello.com/c/qVcURTVE/17-canterbury-tree-preservation-orders",
            "query": "?dataset=tree-preservation-zone&longitude=1.13448673&latitude=51.34722172",
            "dataset": "tree-preservation-zone",
            "assertions": {
                "$.count": 1,
                "$.entities[0].name": "16 Albion Lane Herne Herne Bay Kent CT6 7LP",
                "$.entities[0].organisation-entity": "75",
                "$.entities[0].tree-preservation-order": "TPO/04/2021/HER",
            },
        },
        "Canterbury Tree Zone Lasso Query Rochester Avenue": {
            "ticket": "https://trello.com/c/qVcURTVE/17-canterbury-tree-preservation-orders",
            "query": "?geometry=POLYGON((1.0909509658813474 51.27260180522353,1.0920882225036619 51.27319246878923,1.0932898521423338 51.27371600514732,1.095006465911865 51.2730716518594,1.0947489738464353 51.272736047609754,1.0962724685668943 51.27148757828044,1.0944914817810056 51.26979604959158,1.0926675796508787 51.27116538714043,1.0909509658813474 51.27260180522353))&geometry_relation=intersects&dataset=tree-preservation-zone",  # noqa: E501
            "dataset": "tree-preservation-zone",
            "assertions": {
                "$.count": 4,
            },
        },
        "Canterbury Tree Zone Lasso Query Chaucer Court": {
            "ticket": "https://trello.com/c/qVcURTVE/17-canterbury-tree-preservation-orders",
            "query": "?geometry=POLYGON((1.0897278785705564 51.27324616510049,1.0877537727355955 51.272776320249136,1.087667942047119 51.272977682916604,1.0883545875549314 51.27323274102855,1.0887193679809568 51.2733401334942,1.0896205902099607 51.27350122172206,1.0897278785705564 51.27324616510049))&geometry_relation=intersects&dataset=tree-preservation-zone",  # noqa: E501
            "dataset": "tree-preservation-zone",
            "assertions": {
                "$.count": 6,
            },
        },
        "Canterbury Tree Preservation Zone Overall Count": {
            "ticket": "https://trello.com/c/qVcURTVE/17-canterbury-tree-preservation-orders",
            "query": "?dataset=tree-preservation-zone&organisation_entity=75&field=reference",
            "dataset": "tree-preservation-zone",
            "assertions": {
                "$.count": 1573,
            },
        },
        "Canterbury Tree Preservation Zone (Lasso polygon around Cherry Avenue)": {
            "ticket": "https://trello.com/c/qVcURTVE/17-canterbury-tree-preservation-orders",
            "query": "?geometry=POLYGON%20((1.05943637247152%2051.2888303021592,1.05970135818629%2051.289536050302,1.06080859267814%2051.2897450342821,1.06165081394246%2051.2892482651408,1.06138579958004%2051.2885425218673,1.06027859260043%2051.2883335428658,1.05943637247152%2051.2888303021592))&geometry_relation=intersects&dataset=tree-preservation-zone",  # noqa: E501
            "dataset": "tree-preservation-zone",
            "assertions": {
                "$.count": 44,
            },
        },
        "Canterbury Tree Overall Count": {
            "ticket": "https://trello.com/c/qVcURTVE/17-canterbury-tree-preservation-orders",
            "query": "?dataset=tree&organisation_entity=75&field=reference",
            "dataset": "tree",
            "assertions": {
                "$.count": 0,
            },
        },
        "Canterbury Listed Building (Herne Bay)": {
            "ticket": "https://trello.com/c/TghyQSq1/16-canterbury-listed-buildings",
            "query": "?dataset=listed-building-outline&longitude=1.13294186&latitude=51.34991609",
            "dataset": "listed-building-outline",
            "assertions": {
                "$.count": 1,
                "$.entities[0].name": "HERNE STREET (WEST SIDE) HERNE, THE PARISH CHURCH OF ST MARTIN HERNE",
                "$.entities[0].organisation-entity": "75",
                "$.entities[0].listed-building-grade": "I",
            },
        },
        "Canterbury Listed Building (Church Lane)": {
            "ticket": "https://trello.com/c/TghyQSq1/16-canterbury-listed-buildings",
            "query": "?dataset=listed-building-outline&longitude=1.19202956&latitude=51.33433666",
            "dataset": "listed-building-outline",
            "assertions": {
                "$.count": 1,
                "$.entities[0].name": "CHURCH LANE, CHURCH OF ST MARY THE VIRGIN",
                "$.entities[0].organisation-entity": "75",
                "$.entities[0].listed-building-grade": "I",
            },
        },
        "Canterbury Listed Building (Swalecliffe Court Drive)": {
            "ticket": "https://trello.com/c/TghyQSq1/16-canterbury-listed-buildings",
            "query": "?dataset=listed-building-outline&longitude=1.06666622&latitude=51.36456171",
            "dataset": "listed-building-outline",
            "assertions": {
                "$.count": 1,
                "$.entities[0].name": "Church of St John the Baptist, Swalecliffe Court Drive, Swalecliffe, Whitstable, Kent, CT5 2LZ",
                "$.entities[0].organisation-entity": "75",
                "$.entities[0].listed-building-grade": "II",
            },
        },
        "Canterbury Listed Building (St Bartholomew)": {
            "ticket": "https://trello.com/c/TghyQSq1/16-canterbury-listed-buildings",
            "query": "?dataset=listed-building-outline&longitude=1.02240110&latitude=51.19619623",
            "dataset": "listed-building-outline",
            "assertions": {
                "$.count": 1,
                "$.entities[0].name": "CHURCH LANE, CHURCH OF ST BARTHOLOMEW",
                "$.entities[0].organisation-entity": "75",
                "$.entities[0].listed-building-grade": "I",
            },
        },
        "Canterbury Listed Building (Barham Court)": {
            "ticket": "https://trello.com/c/TghyQSq1/16-canterbury-listed-buildings",
            "query": "?dataset=listed-building-outline&longitude=1.16233540&latitude=51.20689897",
            "dataset": "listed-building-outline",
            "assertions": {
                "$.count": 1,
                "$.entities[0].name": "THE STREET (EAST SIDE), BARHAM COURT AND ANNE COURT",
                "$.entities[0].organisation-entity": "75",
            },
            "warnings": {
                "$.entities[0].listed-building-grade": "II*",
            },
        },
        "Canterbury Listed Building (Church of St Dunstan's - grade B in CAT source, should be I by Historic England listing)": {
            "ticket": "https://trello.com/c/TghyQSq1/16-canterbury-listed-buildings",
            "query": "?dataset=listed-building-outline&geometry=POINT(1.07091959 51.28365020)&geometry_relation=intersects",
            "dataset": "listed-building-outline",
            "assertions": {
                "$.count": 1,
                "$.entities[0].name": "ST DUNSTANS STREET (SOUTH WEST SIDE), THE CHURCH OF ST DUNSTANS WITHOUT THE WEST GATE",
                "$.entities[0].organisation-entity": "75",
                "$.entities[0].reference": "{A4C9CA0E-DB41-4D3B-8115-68D996A6FFE7}",
            },
            "warnings": {
                "$.entities[0].listed-building-grade": "I",
            },
        },
        "Canterbury Listed Building Pear Tree Cottage (with geometry)": {
            "ticket": "https://trello.com/c/TghyQSq1/16-canterbury-listed-buildings",
            "query": "?dataset=listed-building-outline&longitude=1.16071104&latitude=51.34140336",
            "dataset": "listed-building-outline",
            "assertions": {
                "$.count": 1,
                "$.entities[0].name": "Maypole Road, Hoath, Pear Tree Cottage",
                "$.entities[0].organisation-entity": "75",
                "$.entities[0].listed-building-grade": "II",
                "$.entities[0].reference": "{1A820F8B-007B-476A-BF64-9CAB627A100C}",
            },
        },
        "Canterbury Listed Building Overall Count": {
            "ticket": "https://trello.com/c/TghyQSq1/16-canterbury-listed-buildings",
            "query": "?dataset=listed-building-outline&organisation_entity=75&field=reference",
            "dataset": "listed-building-outline",
            "assertions": {
                "$.count": 1778,
            },
        },
        "Ellenden Wood SSSI": {
            "ticket": "https://trello.com/c/r3wV6tXO/50-sites-of-special-and-or-scientific-interest",
            "query": "?longitude=1.014626&latitude=51.321928&dataset=site-of-special-scientific-interest",
            "dataset": "site-of-special-scientific-interest",
            "assertions": {
                "$.count": 1,
                "$.entities[0].reference": "TR101624",
                "$.entities[0].name": "Ellenden Wood",
            },
        },
        "West Blean and Thornden Woods SSSI": {
            "ticket": "https://trello.com/c/r3wV6tXO/50-sites-of-special-and-or-scientific-interest",
            "query": "?geometry=POINT(1.08231671 51.32957921)&geometry_relation=intersects&dataset=site-of-special-scientific-interest",
            "dataset": "site-of-special-scientific-interest",
            "assertions": {
                "$.count": 1,
                "$.entities[0].name": "West Blean and Thornden Woods",
                "$.entities[0].reference": "TR152633",
            },
        },
        "East Blean Woods SSSI": {
            "ticket": "https://trello.com/c/r3wV6tXO/50-sites-of-special-and-or-scientific-interest",
            "query": "?geometry=POINT(1.14128119 51.33971800)&geometry_relation=intersects&dataset=site-of-special-scientific-interest",
            "dataset": "site-of-special-scientific-interest",
            "assertions": {
                "$.count": 1,
                "$.entities[0].name": "East Blean Woods",
                "$.entities[0].reference": "TR188642",
            },
        },
        # this kind of test belongs against the dataset, not Canterbury
        "World heritage site count": {
            "ticket": "https://trello.com/c/pGDJsPmN/49-world-heritage-sites",
            "query": "?dataset=world-heritage-site",
            "dataset": "world-heritage-site",
            "assertions": {
                "$.count": 20,
            },
        },
        "Canterbury Cathedral world heritage site": {
            "ticket": "https://trello.com/c/pGDJsPmN/49-world-heritage-sites",
            "query": "?latitude=51.2797844&longitude=1.0824708&dataset=world-heritage-site",
            "dataset": "world-heritage-site",
            "assertions": {
                "$.count": 1,
                "$.entities[0].reference": "1000093",
                "$.entities[0].name": "Canterbury Cathedral, St. Augustine's Abbey and St. Martin's Church",
                "$.entities[0].notes": "Core Area",
            },
        },
        "Canterbury Cathedral buffer zone": {
            "ticket": "https://trello.com/c/pGDJsPmN/49-world-heritage-sites",
            "query": "?geometry=POINT(1.0869648 51.2806414)&geometry_relation=intersects&dataset=world-heritage-site-buffer-zone",
            "dataset": "world-heritage-site-buffer-zone",
            "assertions": {
                "$.count": 1,
                "$.entities[0].name": "Canterbury Cathedral, St. Augustine's Abbey and St. Martin's Church",
                "$.entities[0].notes": "Buffer Zone",
                "$.entities[0].world-heritage-site": "1000093",
            },
        },
        "Historic Parks and Gardens DANE JOHN GARDENS": {
            "ticket": "https://trello.com/c/JSTZgrsQ/53-historic-parks-and-gardens",
            "query": "?geometry=POINT(1.07820562 51.27491139)&geometry_relation=intersects&dataset=park-and-garden",
            "dataset": "park-and-garden",
            "assertions": {
                "$.count": 1,
                "$.entities[0].reference": "1001360",
                "$.entities[0].name": "DANE JOHN GARDENS",
                "$.entities[0].park-and-garden-grade": "II",
            },
        },
        "Canterbury has no national parks": {
            "ticket": "https://trello.com/c/qUHnNjO2/54-national-park",
            "query": "?dataset=national-park&geometry_reference=E07000106",
            "dataset": "national-park",
            "assertions": {
                "$.count": 0,
            },
        },
        "National Park Overall Count": {
            "ticket": "https://trello.com/c/qUHnNjO2/54-national-park",
            "query": "?dataset=national-park",
            "dataset": "national-park",
            "assertions": {
                "$.count": 10,
            },
        },
    },
}
