# "C": [Latitude, Longitude, Structures, Tents, Passenger Vehicles, Other Vehicles]
# not sure what's happening with "R"

{
    "jobIds": ["db07c80e-429d-4828-a73f-28be62efeeb2"],
    "results": [
        {
            "jobId": "db07c80e-429d-4828-a73f-28be62efeeb2",
            "result": {
                "data": {
                    "timestamp": "2026-02-17T06:10:49.11Z",
                    "rootActivityId": "1f2708c9-c623-41a6-af3c-c2a57809eb9c",
                    "descriptor": {
                        "Select": [
                            {
                                "Kind": 1,
                                "Depth": 1,
                                "Value": "G1",
                                "GroupKeys": [
                                    {
                                        "Source": {
                                            "Entity": "Tent Count Database (Sharepoint Connection)",
                                            "Property": "Latitude",
                                        },
                                        "Calc": "G1",
                                        "IsSameAsSelect": true,
                                    }
                                ],
                                "Name": "Tent Count Database (Sharepoint Connection).Latitude",
                            },
                            {
                                "Kind": 1,
                                "Depth": 1,
                                "Value": "G2",
                                "GroupKeys": [
                                    {
                                        "Source": {
                                            "Entity": "Tent Count Database (Sharepoint Connection)",
                                            "Property": "Longitude",
                                        },
                                        "Calc": "G2",
                                        "IsSameAsSelect": true,
                                    }
                                ],
                                "Name": "Tent Count Database (Sharepoint Connection).Longitude",
                            },
                            {
                                "Kind": 1,
                                "Depth": 0,
                                "Value": "G0",
                                "GroupKeys": [
                                    {
                                        "Source": {
                                            "Entity": "Tent Count Database (Sharepoint Connection)",
                                            "Property": "Tent or Vehicle Indicator",
                                        },
                                        "Calc": "G0",
                                        "IsSameAsSelect": true,
                                    }
                                ],
                                "Name": "Tent Count Database (Sharepoint Connection).Tent or Vehicle Indicator",
                            },
                            {
                                "Kind": 2,
                                "Value": "M0",
                                "Format": "0",
                                "Name": "Sum(Tent Count Database (Sharepoint Connection).Structures)",
                            },
                            {
                                "Kind": 2,
                                "Value": "M1",
                                "Format": "0",
                                "Name": "Sum(Tent Count Database (Sharepoint Connection).Tents)",
                            },
                            {
                                "Kind": 2,
                                "Value": "M2",
                                "Format": "0",
                                "Name": "Sum(Tent Count Database (Sharepoint Connection).Passenger Vehicles)",
                            },
                            {
                                "Kind": 2,
                                "Value": "M3",
                                "Format": "0",
                                "Name": "Sum(Tent Count Database (Sharepoint Connection).Other Vehicles)",
                            },
                        ],
                        "Expressions": {
                            "Primary": {
                                "Groupings": [
                                    {
                                        "Keys": [
                                            {
                                                "Source": {
                                                    "Entity": "Tent Count Database (Sharepoint Connection)",
                                                    "Property": "Tent or Vehicle Indicator",
                                                },
                                                "Select": 2,
                                            }
                                        ],
                                        "Member": "DM0",
                                    },
                                    {
                                        "Keys": [
                                            {
                                                "Source": {
                                                    "Entity": "Tent Count Database (Sharepoint Connection)",
                                                    "Property": "Latitude",
                                                },
                                                "Select": 0,
                                            },
                                            {
                                                "Source": {
                                                    "Entity": "Tent Count Database (Sharepoint Connection)",
                                                    "Property": "Longitude",
                                                },
                                                "Select": 1,
                                            },
                                        ],
                                        "Member": "DM1",
                                    },
                                ]
                            }
                        },
                        "Limits": {
                            "Primary": {
                                "Id": "L0",
                                "OverlappingPointsSample": {"Count": 3500},
                            }
                        },
                        "Version": 2,
                    },
                    "metrics": {
                        "Version": "1.0.0",
                        "Events": [
                            {
                                "Id": "e5b75134-fe80-4fc0-9f83-f611ddc72062",
                                "Name": "Execute Semantic Query",
                                "Component": "DSE",
                                "Start": "2026-02-17T06:10:49.1105496Z",
                                "End": "2026-02-17T06:10:49.1730521Z",
                            },
                            {
                                "Id": "19c609a3-2370-480e-b1c9-0dcfa5001af5",
                                "ParentId": "e5b75134-fe80-4fc0-9f83-f611ddc72062",
                                "Name": "Execute DAX Query",
                                "Component": "DSE",
                                "Start": "2026-02-17T06:10:49.1105496Z",
                                "End": "2026-02-17T06:10:49.1730521Z",
                                "Metrics": {"RowCount": 351},
                            },
                            {
                                "Id": "6F540105-0735-4FCF-ABF8-A807EFA6A434",
                                "ParentId": "19c609a3-2370-480e-b1c9-0dcfa5001af5",
                                "Name": "Execute Query",
                                "Component": "AS",
                                "Start": "2026-02-17T06:10:49.157Z",
                                "End": "2026-02-17T06:10:49.167Z",
                            },
                            {
                                "Id": "CCD5C41F-3437-4212-BADA-7883F74F7F64",
                                "ParentId": "6F540105-0735-4FCF-ABF8-A807EFA6A434",
                                "Name": "Serialize Rowset",
                                "Component": "AS",
                                "Start": "2026-02-17T06:10:49.167Z",
                                "End": "2026-02-17T06:10:49.167Z",
                            },
                        ],
                    },
                    "fromCache": false,
                    "dsr": {
                        "Version": 2,
                        "MinorVersion": 1,
                        "DS": [
                            {
                                "N": "DS0",
                                "PH": [
                                    {
                                        "DM0": [
                                            {
                                                "S": [{"N": "G0", "T": 1}],
                                                "G0": "Both Tent and Vehicle",
                                                "M": [
                                                    {
                                                        "DM1": [
                                                            {
                                                                "S": [
                                                                    {"N": "G1", "T": 3},
                                                                    {"N": "G2", "T": 3},
                                                                    {"N": "M0", "T": 4},
                                                                    {"N": "M1", "T": 4},
                                                                    {"N": "M2", "T": 4},
                                                                    {"N": "M3", "T": 4},
                                                                ],
                                                                "C": [
                                                                    "37.71756490852998",
                                                                    "-122.4989517753595",
                                                                    1,
                                                                    0,
                                                                    1,
                                                                    0,
                                                                ],
                                                            },
                                                            {
                                                                "C": [
                                                                    "37.722240233287856",
                                                                    "-122.38849826369839",
                                                                    0,
                                                                    7,
                                                                ],
                                                                "R": 12,
                                                            },
                                                            {
                                                                "C": [
                                                                    "37.723495751696923",
                                                                    "-122.38904719885906",
                                                                    0,
                                                                    2,
                                                                    1,
                                                                    5,
                                                                ]
                                                            },
                                                            {
                                                                "C": [
                                                                    "37.726356909820375",
                                                                    "-122.39751719113195",
                                                                    2,
                                                                    0,
                                                                    5,
                                                                    4,
                                                                ]
                                                            },
                                                            {
                                                                "C": [
                                                                    "37.737850259187262",
                                                                    "-122.39291210449571",
                                                                    1,
                                                                    0,
                                                                ],
                                                                "R": 40,
                                                            },
                                                            {
                                                                "C": [
                                                                    "37.738754281783052",
                                                                    "-122.40696995735405",
                                                                    4,
                                                                    1,
                                                                ],
                                                                "R": 24,
                                                            },
                                                            {
                                                                "C": [
                                                                    "37.73929967774103",
                                                                    "-122.40029633045197",
                                                                    0,
                                                                    2,
                                                                    3,
                                                                ],
                                                                "R": 16,
                                                            },
                                                            {
                                                                "C": [
                                                                    "37.742476697309655",
                                                                    "-122.38489093368797",
                                                                    1,
                                                                    0,
                                                                    1,
                                                                    9,
                                                                ]
                                                            },
                                                            {
                                                                "C": [
                                                                    "37.745442927695166",
                                                                    "-122.39470157772304",
                                                                    2,
                                                                    1,
                                                                    0,
                                                                    2,
                                                                ]
                                                            },
                                                            {
                                                                "C": [
                                                                    "37.752630948091657",
                                                                    "-122.39665137915426",
                                                                    0,
                                                                    3,
                                                                ],
                                                                "R": 24,
                                                            },
                                                            {
                                                                "C": [
                                                                    "37.757808283442742",
                                                                    "-122.39237161898058",
                                                                    1,
                                                                    1,
                                                                ],
                                                                "R": 40,
                                                            },
                                                            {
                                                                "C": [
                                                                    "37.764717994657836",
                                                                    "-122.41339792562358",
                                                                    0,
                                                                    0,
                                                                    2,
                                                                ],
                                                                "R": 8,
                                                            },
                                                        ]
                                                    }
                                                ],
                                            },
                                            {
                                                "G0": "Tent/Structure",
                                                "M": [
                                                    {
                                                        "DM1": [
                                                            {
                                                                "C": [
                                                                    "37.710289791424337",
                                                                    "-122.45694994926453",
                                                                    1,
                                                                    0,
                                                                    0,
                                                                ],
                                                                "R": 16,
                                                            },
                                                            {
                                                                "C": [
                                                                    "37.710542035695546",
                                                                    "-122.4481026828289",
                                                                ],
                                                                "R": 60,
                                                            },
                                                            {
                                                                "C": [
                                                                    "37.711700597723294",
                                                                    "-122.45605643838643",
                                                                ],
                                                                "R": 60,
                                                            },
                                                            {
                                                                "C": [
                                                                    "37.713533700356074",
                                                                    "-122.48419248953343",
                                                                    0,
                                                                    1,
                                                                ],
                                                                "R": 48,
                                                            },
                                                            {
                                                                "C": [
                                                                    "37.714089671202537",
                                                                    "-122.48578142932257",
                                                                ],
                                                                "R": 60,
                                                            },
                                                            {
                                                                "C": [
                                                                    "37.7142533041443",
                                                                    "-122.48480609785894",
                                                                    1,
                                                                    0,
                                                                ],
                                                                "R": 48,
                                                            },
                                                            {
                                                                "C": [
                                                                    "37.718770934619442",
                                                                    "-122.4481238052249",
                                                                    0,
                                                                    2,
                                                                ],
                                                                "R": 48,
                                                            },
                                                            {
                                                                "C": [
                                                                    "37.721100297594035",
                                                                    "-122.41997636420656",
                                                                    1,
                                                                    0,
                                                                ],
                                                                "R": 48,
                                                            },
                                                            {
                                                                "C": [
                                                                    "37.726106577736047",
                                                                    "-122.44594316929579",
                                                                    0,
                                                                    1,
                                                                ],
                                                                "R": 48,
                                                            },
                                                            {
                                                                "C": [
                                                                    "37.728410679649187",
                                                                    "-122.48838340748749",
                                                                    1,
                                                                    0,
                                                                ],
                                                                "R": 48,
                                                            },
                                                            {
                                                                "C": [
                                                                    "37.728721519996292",
                                                                    "-122.50644877552985",
                                                                ],
                                                                "R": 60,
                                                            },
                                                            {
                                                                "C": [
                                                                    "37.734284428894021",
                                                                    "-122.40555144846441",
                                                                    0,
                                                                    1,
                                                                ],
                                                                "R": 48,
                                                            },
                                                            {
                                                                "C": [
                                                                    "37.736164623584223",
                                                                    "-122.50435564666988",
                                                                    1,
                                                                    0,
                                                                ],
                                                                "R": 48,
                                                            },
                                                            {
                                                                "C": [
                                                                    "37.740499879322186",
                                                                    "-122.37667327758147",
                                                                ],
                                                                "R": 60,
                                                            },
                                                            {
                                                                "C": [
                                                                    "37.741852938950316",
                                                                    "-122.40625404274957",
                                                                    1,
                                                                ],
                                                                "R": 52,
                                                            },
                                                            {
                                                                "C": [
                                                                    "37.74263575555446",
                                                                    "-122.40009202667456",
                                                                    0,
                                                                ],
                                                                "R": 52,
                                                            },
                                                            {
                                                                "C": [
                                                                    "37.7447803839782",
                                                                    "-122.3872699647154",
                                                                ],
                                                                "R": 60,
                                                            },
                                                            {
                                                                "C": [
                                                                    "37.745828480001457",
                                                                    "-122.38635393005173",
                                                                    1,
                                                                ],
                                                                "R": 52,
                                                            },
                                                            {
                                                                "C": [
                                                                    "37.74657610947267",
                                                                    "-122.3881643243042",
                                                                    0,
                                                                ],
                                                                "R": 56,
                                                            },
                                                            {
                                                                "C": [
                                                                    "37.746584402140094",
                                                                    "-122.38653212327733",
                                                                ],
                                                                "R": 60,
                                                            },
                                                            {
                                                                "C": [
                                                                    "37.74679279860581",
                                                                    "-122.39098031729618",
                                                                    1,
                                                                    0,
                                                                ],
                                                                "R": 48,
                                                            },
                                                            {
                                                                "C": [
                                                                    "37.747712851837427",
                                                                    "-122.38966840404696",
                                                                ],
                                                                "R": 60,
                                                            },
                                                            {
                                                                "C": [
                                                                    "37.748103802115281",
                                                                    "-122.39090224836318",
                                                                    3,
                                                                ],
                                                                "R": 52,
                                                            },
                                                            {
                                                                "C": [
                                                                    "37.748762631567587",
                                                                    "-122.40675441920757",
                                                                    0,
                                                                ],
                                                                "R": 52,
                                                            },
                                                            {
                                                                "C": [
                                                                    "37.749271513390696",
                                                                    "-122.40457304543961",
                                                                    3,
                                                                    4,
                                                                ],
                                                                "R": 48,
                                                            },
                                                            {
                                                                "C": [
                                                                    "37.749905314393352",
                                                                    "-122.40427160000003",
                                                                    0,
                                                                    1,
                                                                ],
                                                                "R": 48,
                                                            },
                                                            {
                                                                "C": [
                                                                    "37.750106143526018",
                                                                    "-122.39197980077581",
                                                                    1,
                                                                    2,
                                                                ],
                                                                "R": 48,
                                                            },
                                                            {
                                                                "C": [
                                                                    "37.753175947531055",
                                                                    "-122.50545937567948",
                                                                    0,
                                                                ],
                                                                "R": 52,
                                                            },
                                                            {
                                                                "C": [
                                                                    "37.754479528314043",
                                                                    "-122.38327949017894",
                                                                    0,
                                                                    4,
                                                                ],
                                                                "R": 48,
                                                            },
                                                            {
                                                                "C": [
                                                                    "37.756902990367713",
                                                                    "-122.40393374115229",
                                                                    1,
                                                                ],
                                                                "R": 52,
                                                            },
                                                            {
                                                                "C": [
                                                                    "37.7573915212535",
                                                                    "-122.40284409374",
                                                                ],
                                                                "R": 60,
                                                            },
                                                            {
                                                                "C": [
                                                                    "37.763263977266917",
                                                                    "-122.43527099490167",
                                                                    1,
                                                                    0,
                                                                ],
                                                                "R": 48,
                                                            },
                                                            {
                                                                "C": [
                                                                    "37.763942771844142",
                                                                    "-122.47047733515501",
                                                                ],
                                                                "R": 60,
                                                            },
                                                            {
                                                                "C": [
                                                                    "37.764268817077827",
                                                                    "-122.51038558431337",
                                                                ],
                                                                "R": 60,
                                                            },
                                                            {
                                                                "C": [
                                                                    "37.7643970059586",
                                                                    "-122.51024138356597",
                                                                ],
                                                                "R": 60,
                                                            },
                                                            {
                                                                "C": [
                                                                    "37.764436616395543",
                                                                    "-122.50987127453696",
                                                                ],
                                                                "R": 60,
                                                            },
                                                            {
                                                                "C": [
                                                                    "37.764500990833085",
                                                                    "-122.50936630689777",
                                                                ],
                                                                "R": 60,
                                                            },
                                                            {
                                                                "C": [
                                                                    "37.7654017133632",
                                                                    "-122.4984979354993",
                                                                ],
                                                                "R": 60,
                                                            },
                                                            {
                                                                "C": [
                                                                    "37.765734518975833",
                                                                    "-122.4779292350896",
                                                                ],
                                                                "R": 60,
                                                            },
                                                            {
                                                                "C": [
                                                                    "37.765813731753042",
                                                                    "-122.46666558086874",
                                                                ],
                                                                "R": 60,
                                                            },
                                                            {
                                                                "C": [
                                                                    "37.766005974574341",
                                                                    "-122.50934972348271",
                                                                    0,
                                                                    1,
                                                                ],
                                                                "R": 48,
                                                            },
                                                            {
                                                                "C": [
                                                                    "37.766543799215569",
                                                                    "-122.50799291043343",
                                                                    1,
                                                                    0,
                                                                ],
                                                                "R": 48,
                                                            },
                                                            {
                                                                "C": [
                                                                    "37.766983201822725",
                                                                    "-122.41438294338874",
                                                                    1,
                                                                ],
                                                                "R": 52,
                                                            },
                                                            {
                                                                "C": [
                                                                    "37.767575067675558",
                                                                    "-122.50734074007785",
                                                                    0,
                                                                ],
                                                                "R": 56,
                                                            },
                                                            {
                                                                "C": [
                                                                    "37.767955314979105",
                                                                    "-122.4426025434325",
                                                                    1,
                                                                    0,
                                                                ],
                                                                "R": 48,
                                                            },
                                                            {
                                                                "C": [
                                                                    "37.76826233053756",
                                                                    "-122.45770560580969",
                                                                ],
                                                                "R": 60,
                                                            },
                                                            {
                                                                "C": [
                                                                    "37.768436787060487",
                                                                    "-122.44143961710763",
                                                                ],
                                                                "R": 60,
                                                            },
                                                            {
                                                                "C": [
                                                                    "37.768616309770266",
                                                                    "-122.45540792619279",
                                                                    0,
                                                                    1,
                                                                ],
                                                                "R": 48,
                                                            },
                                                            {
                                                                "C": [
                                                                    "37.768886837719521",
                                                                    "-122.47862722724678",
                                                                    1,
                                                                    0,
                                                                ],
                                                                "R": 48,
                                                            },
                                                            {
                                                                "C": [
                                                                    "37.768916398252934",
                                                                    "-122.41848571371303",
                                                                    0,
                                                                    2,
                                                                ],
                                                                "R": 48,
                                                            },
                                                            {
                                                                "C": [
                                                                    "37.769276668233829",
                                                                    "-122.5086434941029",
                                                                    1,
                                                                ],
                                                                "R": 52,
                                                            },
                                                            {
                                                                "C": [
                                                                    "37.769388820586023",
                                                                    "-122.45982039873786",
                                                                    1,
                                                                    0,
                                                                ],
                                                                "R": 48,
                                                            },
                                                            {
                                                                "C": [
                                                                    "37.769930260009019",
                                                                    "-122.44765743613243",
                                                                    2,
                                                                ],
                                                                "R": 56,
                                                            },
                                                            {
                                                                "C": [
                                                                    "37.769972399436583",
                                                                    "-122.40895047783852",
                                                                    0,
                                                                    3,
                                                                ],
                                                                "R": 48,
                                                            },
                                                            {
                                                                "C": [
                                                                    "37.770020634475109",
                                                                    "-122.40811865776777",
                                                                    4,
                                                                ],
                                                                "R": 52,
                                                            },
                                                            {
                                                                "C": [
                                                                    "37.770072844893456",
                                                                    "-122.41900775581598",
                                                                    1,
                                                                ],
                                                                "R": 52,
                                                            },
                                                            {
                                                                "C": [
                                                                    "37.770449602422715",
                                                                    "-122.47247719976328",
                                                                    1,
                                                                    0,
                                                                ],
                                                                "R": 48,
                                                            },
                                                            {
                                                                "C": [
                                                                    "37.7708831600939",
                                                                    "-122.46639497711277",
                                                                ],
                                                                "R": 60,
                                                            },
                                                            {
                                                                "C": [
                                                                    "37.770937359253431",
                                                                    "-122.40850958973168",
                                                                    0,
                                                                    3,
                                                                ],
                                                                "R": 48,
                                                            },
                                                            {
                                                                "C": [
                                                                    "37.771077345893971",
                                                                    "-122.50749944624482",
                                                                    1,
                                                                    0,
                                                                ],
                                                                "R": 48,
                                                            },
                                                            {
                                                                "C": [
                                                                    "37.771581462984344",
                                                                    "-122.50273669931985",
                                                                ],
                                                                "R": 60,
                                                            },
                                                            {
                                                                "C": [
                                                                    "37.77171602926559",
                                                                    "-122.47417158417323",
                                                                ],
                                                                "R": 60,
                                                            },
                                                            {
                                                                "C": [
                                                                    "37.772079605216092",
                                                                    "-122.45397370308638",
                                                                ],
                                                                "R": 60,
                                                            },
                                                            {
                                                                "C": [
                                                                    "37.772113638802168",
                                                                    "-122.47977916908147",
                                                                ],
                                                                "R": 60,
                                                            },
                                                            {
                                                                "C": [
                                                                    "37.772448680148443",
                                                                    "-122.44876159799814",
                                                                ],
                                                                "R": 60,
                                                            },
                                                            {
                                                                "C": [
                                                                    "37.772984378704841",
                                                                    "-122.42119677364826",
                                                                    0,
                                                                    1,
                                                                ],
                                                                "R": 48,
                                                            },
                                                            {
                                                                "C": [
                                                                    "37.774192373436868",
                                                                    "-122.45484733636418",
                                                                    1,
                                                                    0,
                                                                ],
                                                                "R": 48,
                                                            },
                                                            {
                                                                "C": [
                                                                    "37.775880692494773",
                                                                    "-122.39518705755472",
                                                                    0,
                                                                    1,
                                                                ],
                                                                "R": 48,
                                                            },
                                                            {
                                                                "C": [
                                                                    "37.775993055204964",
                                                                    "-122.40565236657858",
                                                                ],
                                                                "R": 60,
                                                            },
                                                            {
                                                                "C": [
                                                                    "37.777118527929247",
                                                                    "-122.41462804377079",
                                                                ],
                                                                "R": 60,
                                                            },
                                                            {
                                                                "C": [
                                                                    "37.778326927884855",
                                                                    "-122.40201294422151",
                                                                    3,
                                                                ],
                                                                "R": 52,
                                                            },
                                                            {
                                                                "C": [
                                                                    "37.778848706759547",
                                                                    "-122.39897232502699",
                                                                    1,
                                                                ],
                                                                "R": 52,
                                                            },
                                                            {
                                                                "C": [
                                                                    "37.780184539292975",
                                                                    "-122.40771196782589",
                                                                    2,
                                                                ],
                                                                "R": 52,
                                                            },
                                                            {
                                                                "C": [
                                                                    "37.780509152757432",
                                                                    "-122.47880257666111",
                                                                    3,
                                                                    0,
                                                                ],
                                                                "R": 48,
                                                            },
                                                            {
                                                                "C": [
                                                                    "37.780777587141422",
                                                                    "-122.4622754752636",
                                                                    2,
                                                                ],
                                                                "R": 56,
                                                            },
                                                            {
                                                                "C": [
                                                                    "37.780821045331024",
                                                                    "-122.40783233195543",
                                                                    0,
                                                                    2,
                                                                ],
                                                                "R": 48,
                                                            },
                                                            {
                                                                "C": [
                                                                    "37.780911671473547",
                                                                    "-122.46308751404285",
                                                                    1,
                                                                    0,
                                                                ],
                                                                "R": 48,
                                                            },
                                                            {
                                                                "C": [
                                                                    "37.780959104410272",
                                                                    "-122.46974509209396",
                                                                ],
                                                                "R": 60,
                                                            },
                                                            {
                                                                "C": [
                                                                    "37.781670859794389",
                                                                    "-122.42043670266867",
                                                                    0,
                                                                    1,
                                                                ],
                                                                "R": 48,
                                                            },
                                                            {
                                                                "C": [
                                                                    "37.78199546673148",
                                                                    "-122.41301234811544",
                                                                ],
                                                                "R": 60,
                                                            },
                                                            {
                                                                "C": [
                                                                    "37.782305233165012",
                                                                    "-122.42170907557012",
                                                                    1,
                                                                ],
                                                                "R": 56,
                                                            },
                                                            {
                                                                "C": [
                                                                    "37.782609433668604",
                                                                    "-122.4694212153554",
                                                                    0,
                                                                ],
                                                                "R": 52,
                                                            },
                                                            {
                                                                "C": [
                                                                    "37.782901973738504",
                                                                    "-122.41327621042727",
                                                                    0,
                                                                    1,
                                                                ],
                                                                "R": 48,
                                                            },
                                                            {
                                                                "C": [
                                                                    "37.783443593782557",
                                                                    "-122.42010746151207",
                                                                    3,
                                                                ],
                                                                "R": 52,
                                                            },
                                                            {
                                                                "C": [
                                                                    "37.783743549946564",
                                                                    "-122.4109111726284",
                                                                    1,
                                                                ],
                                                                "R": 52,
                                                            },
                                                            {
                                                                "C": [
                                                                    "37.784141811417413",
                                                                    "-122.41860508918761",
                                                                    3,
                                                                ],
                                                                "R": 52,
                                                            },
                                                            {
                                                                "C": [
                                                                    "37.784205140887991",
                                                                    "-122.4143685400486",
                                                                    1,
                                                                ],
                                                                "R": 52,
                                                            },
                                                            {
                                                                "C": [
                                                                    "37.784398573662983",
                                                                    "-122.42009505629539",
                                                                ],
                                                                "R": 60,
                                                            },
                                                            {
                                                                "C": [
                                                                    "37.78442189155237",
                                                                    "-122.41274815052748",
                                                                ],
                                                                "R": 60,
                                                            },
                                                            {
                                                                "C": [
                                                                    "37.784470117163856",
                                                                    "-122.43340384215118",
                                                                ],
                                                                "R": 60,
                                                            },
                                                            {
                                                                "C": [
                                                                    "37.784639436506637",
                                                                    "-122.41108819842337",
                                                                ],
                                                                "R": 60,
                                                            },
                                                            {
                                                                "C": [
                                                                    "37.78464897561301",
                                                                    "-122.41861447691917",
                                                                    3,
                                                                ],
                                                                "R": 52,
                                                            },
                                                            {
                                                                "C": [
                                                                    "37.784947072066338",
                                                                    "-122.41618171334267",
                                                                    1,
                                                                ],
                                                                "R": 52,
                                                            },
                                                            {
                                                                "C": [
                                                                    "37.784956346158943",
                                                                    "-122.41195186972618",
                                                                    2,
                                                                ],
                                                                "R": 52,
                                                            },
                                                            {
                                                                "C": [
                                                                    "37.785079558993019",
                                                                    "-122.41873249411583",
                                                                    1,
                                                                ],
                                                                "R": 52,
                                                            },
                                                            {
                                                                "C": [
                                                                    "37.785454495708308",
                                                                    "-122.41294529289006",
                                                                ],
                                                                "R": 60,
                                                            },
                                                            {
                                                                "C": [
                                                                    "37.785475693487008",
                                                                    "-122.41545684635638",
                                                                ],
                                                                "R": 60,
                                                            },
                                                            {
                                                                "C": [
                                                                    "37.78557028850026",
                                                                    "-122.41865169256924",
                                                                    2,
                                                                    0,
                                                                ],
                                                                "R": 48,
                                                            },
                                                            {
                                                                "C": [
                                                                    "37.785945222725964",
                                                                    "-122.4118921905756",
                                                                    0,
                                                                    1,
                                                                ],
                                                                "R": 48,
                                                            },
                                                            {
                                                                "C": [
                                                                    "37.786443630578546",
                                                                    "-122.41929743438959",
                                                                ],
                                                                "R": 60,
                                                            },
                                                            {
                                                                "C": [
                                                                    "37.787217600171616",
                                                                    "-122.4206294864416",
                                                                ],
                                                                "R": 60,
                                                            },
                                                            {
                                                                "C": [
                                                                    "37.7884041081706",
                                                                    "-122.41882033646107",
                                                                    1,
                                                                    0,
                                                                ],
                                                                "R": 48,
                                                            },
                                                            {
                                                                "C": [
                                                                    "37.791112840968289",
                                                                    "-122.38964362902594",
                                                                    0,
                                                                    1,
                                                                ],
                                                                "R": 48,
                                                            },
                                                            {
                                                                "C": [
                                                                    "37.793612276673876",
                                                                    "-122.40788731724024",
                                                                    1,
                                                                    0,
                                                                ],
                                                                "R": 48,
                                                            },
                                                        ]
                                                    }
                                                ],
                                            },
                                            {
                                                "G0": "Vehicle/RV",
                                                "M": [
                                                    {
                                                        "DM1": [
                                                            {
                                                                "C": [
                                                                    "37.708785856655894",
                                                                    "-122.48703327029942",
                                                                    0,
                                                                    2,
                                                                ],
                                                                "R": 40,
                                                            },
                                                            {
                                                                "C": [
                                                                    "37.710406027589833",
                                                                    "-122.48833489010249",
                                                                    1,
                                                                ],
                                                                "R": 44,
                                                            },
                                                            {
                                                                "C": [
                                                                    "37.711274626702419",
                                                                    "-122.45397303253412",
                                                                    0,
                                                                    2,
                                                                ],
                                                                "R": 12,
                                                            },
                                                            {
                                                                "C": [
                                                                    "37.7114804511129",
                                                                    "-122.45638601481915",
                                                                ],
                                                                "R": 60,
                                                            },
                                                            {
                                                                "C": [
                                                                    "37.712459142022553",
                                                                    "-122.48979281354192",
                                                                    1,
                                                                ],
                                                                "R": 28,
                                                            },
                                                            {
                                                                "C": [
                                                                    "37.712492209920327",
                                                                    "-122.48986606430923",
                                                                ],
                                                                "R": 60,
                                                            },
                                                            {
                                                                "C": [
                                                                    "37.712603958604177",
                                                                    "-122.49008122070552",
                                                                ],
                                                                "R": 60,
                                                            },
                                                            {
                                                                "C": [
                                                                    "37.712714870180918",
                                                                    "-122.49016522974635",
                                                                    1,
                                                                ],
                                                                "R": 44,
                                                            },
                                                            {
                                                                "C": [
                                                                    "37.712756599657965",
                                                                    "-122.49029410737049",
                                                                    0,
                                                                ],
                                                                "R": 44,
                                                            },
                                                            {
                                                                "C": [
                                                                    "37.712981863925421",
                                                                    "-122.49056055201554",
                                                                ],
                                                                "R": 60,
                                                            },
                                                            {
                                                                "C": [
                                                                    "37.713019443761446",
                                                                    "-122.49057004281762",
                                                                ],
                                                                "R": 60,
                                                            },
                                                            {
                                                                "C": [
                                                                    "37.713204473338031",
                                                                    "-122.45736770331858",
                                                                    2,
                                                                ],
                                                                "R": 28,
                                                            },
                                                            {
                                                                "C": [
                                                                    "37.713219739043964",
                                                                    "-122.49115489245499",
                                                                    1,
                                                                ],
                                                                "R": 28,
                                                            },
                                                            {
                                                                "C": [
                                                                    "37.713474008121295",
                                                                    "-122.49110430973631",
                                                                ],
                                                                "R": 60,
                                                            },
                                                            {
                                                                "C": [
                                                                    "37.713529033656073",
                                                                    "-122.49131506216717",
                                                                ],
                                                                "R": 60,
                                                            },
                                                            {
                                                                "C": [
                                                                    "37.713605840852885",
                                                                    "-122.41546163334081",
                                                                ],
                                                                "R": 60,
                                                            },
                                                            {
                                                                "C": [
                                                                    "37.7136559319319",
                                                                    "-122.49166596784153",
                                                                ],
                                                                "R": 60,
                                                            },
                                                            {
                                                                "C": [
                                                                    "37.713775984511173",
                                                                    "-122.49147497361393",
                                                                ],
                                                                "R": 60,
                                                            },
                                                            {
                                                                "C": [
                                                                    "37.713977409762634",
                                                                    "-122.49172341474477",
                                                                ],
                                                                "R": 60,
                                                            },
                                                            {
                                                                "C": [
                                                                    "37.714011431502904",
                                                                    "-122.49174933711716",
                                                                ],
                                                                "R": 60,
                                                            },
                                                            {
                                                                "C": [
                                                                    "37.714029769709548",
                                                                    "-122.49189535017805",
                                                                ],
                                                                "R": 60,
                                                            },
                                                            {
                                                                "C": [
                                                                    "37.714138080938653",
                                                                    "-122.39938773214818",
                                                                ],
                                                                "R": 60,
                                                            },
                                                            {
                                                                "C": [
                                                                    "37.714163443179167",
                                                                    "-122.49178067812289",
                                                                ],
                                                                "R": 60,
                                                            },
                                                            {
                                                                "C": [
                                                                    "37.714210339599475",
                                                                    "-122.49198011075944",
                                                                ],
                                                                "R": 60,
                                                            },
                                                            {
                                                                "C": [
                                                                    "37.714304909012547",
                                                                    "-122.46484939008951",
                                                                ],
                                                                "R": 60,
                                                            },
                                                            {
                                                                "C": [
                                                                    "37.714440029228754",
                                                                    "-122.49200275398157",
                                                                ],
                                                                "R": 60,
                                                            },
                                                            {
                                                                "C": [
                                                                    "37.71457944240634",
                                                                    "-122.49209630107406",
                                                                ],
                                                                "R": 60,
                                                            },
                                                            {
                                                                "C": [
                                                                    "37.714612041431728",
                                                                    "-122.47016184031963",
                                                                    2,
                                                                ],
                                                                "R": 28,
                                                            },
                                                            {
                                                                "C": [
                                                                    "37.714824522027889",
                                                                    "-122.41623137859531",
                                                                    1,
                                                                ],
                                                                "R": 28,
                                                            },
                                                            {
                                                                "C": [
                                                                    "37.714824537836208",
                                                                    "-122.49232230941895",
                                                                ],
                                                                "R": 60,
                                                            },
                                                            {
                                                                "C": [
                                                                    "37.714909842777161",
                                                                    "-122.49238173654949",
                                                                    1,
                                                                ],
                                                                "R": 44,
                                                            },
                                                            {
                                                                "C": [
                                                                    "37.715022834965374",
                                                                    "-122.49256790202553",
                                                                    0,
                                                                ],
                                                                "R": 44,
                                                            },
                                                            {
                                                                "C": [
                                                                    "37.715046365898949",
                                                                    "-122.38894977403675",
                                                                    2,
                                                                ],
                                                                "R": 28,
                                                            },
                                                            {
                                                                "C": [
                                                                    "37.715050447950865",
                                                                    "-122.49256837325244",
                                                                    1,
                                                                ],
                                                                "R": 28,
                                                            },
                                                            {
                                                                "C": [
                                                                    "37.715117868885756",
                                                                    "-122.49266166625335",
                                                                ],
                                                                "R": 60,
                                                            },
                                                            {
                                                                "C": [
                                                                    "37.7152297503609",
                                                                    "-122.39954899996519",
                                                                ],
                                                                "R": 60,
                                                            },
                                                            {
                                                                "C": [
                                                                    "37.715249860398039",
                                                                    "-122.49299565003828",
                                                                ],
                                                                "R": 60,
                                                            },
                                                            {
                                                                "C": [
                                                                    "37.715345913772481",
                                                                    "-122.49297678765554",
                                                                ],
                                                                "R": 60,
                                                            },
                                                            {
                                                                "C": [
                                                                    "37.7154121176493",
                                                                    "-122.49328100690052",
                                                                ],
                                                                "R": 60,
                                                            },
                                                            {
                                                                "C": [
                                                                    "37.7155196303803",
                                                                    "-122.49347677162197",
                                                                ],
                                                                "R": 60,
                                                            },
                                                            {
                                                                "C": [
                                                                    "37.715519639465391",
                                                                    "-122.47074153274298",
                                                                ],
                                                                "R": 60,
                                                            },
                                                            {
                                                                "C": [
                                                                    "37.715641263678172",
                                                                    "-122.49320856140351",
                                                                ],
                                                                "R": 60,
                                                            },
                                                            {
                                                                "C": [
                                                                    "37.715690522834386",
                                                                    "-122.49363532984883",
                                                                ],
                                                                "R": 60,
                                                            },
                                                            {
                                                                "C": [
                                                                    "37.715729233804282",
                                                                    "-122.49369932415863",
                                                                ],
                                                                "R": 60,
                                                            },
                                                            {
                                                                "C": [
                                                                    "37.715733662340376",
                                                                    "-122.49386560815316",
                                                                ],
                                                                "R": 60,
                                                            },
                                                            {
                                                                "C": [
                                                                    "37.715785089910277",
                                                                    "-122.49396645026071",
                                                                ],
                                                                "R": 60,
                                                            },
                                                            {
                                                                "C": [
                                                                    "37.715819278835284",
                                                                    "-122.49411786005616",
                                                                ],
                                                                "R": 60,
                                                            },
                                                            {
                                                                "C": [
                                                                    "37.715893887916891",
                                                                    "-122.494358723262",
                                                                ],
                                                                "R": 60,
                                                            },
                                                            {
                                                                "C": [
                                                                    "37.715932577675794",
                                                                    "-122.49445615818112",
                                                                ],
                                                                "R": 60,
                                                            },
                                                            {
                                                                "C": [
                                                                    "37.716030120970153",
                                                                    "-122.4946259580819",
                                                                ],
                                                                "R": 60,
                                                            },
                                                            {
                                                                "C": [
                                                                    "37.716047802494643",
                                                                    "-122.49474486094067",
                                                                ],
                                                                "R": 60,
                                                            },
                                                            {
                                                                "C": [
                                                                    "37.7160696471697",
                                                                    "-122.49497824051645",
                                                                ],
                                                                "R": 60,
                                                            },
                                                            {
                                                                "C": [
                                                                    "37.716102862141256",
                                                                    "-122.47171819210052",
                                                                ],
                                                                "R": 60,
                                                            },
                                                            {
                                                                "C": [
                                                                    "37.716425687703179",
                                                                    "-122.49640288672931",
                                                                    1,
                                                                ],
                                                                "R": 44,
                                                            },
                                                            {
                                                                "C": [
                                                                    "37.716529335844044",
                                                                    "-122.4003992602229",
                                                                    0,
                                                                ],
                                                                "R": 44,
                                                            },
                                                            {
                                                                "C": [
                                                                    "37.716712872987422",
                                                                    "-122.49707270885337",
                                                                ],
                                                                "R": 60,
                                                            },
                                                            {
                                                                "C": [
                                                                    "37.717313938416076",
                                                                    "-122.49857764525501",
                                                                ],
                                                                "R": 60,
                                                            },
                                                            {
                                                                "C": [
                                                                    "37.717442837371685",
                                                                    "-122.49867304651485",
                                                                ],
                                                                "R": 60,
                                                            },
                                                            {
                                                                "C": [
                                                                    "37.71746260875377",
                                                                    "-122.49875671601856",
                                                                ],
                                                                "R": 60,
                                                            },
                                                            {
                                                                "C": [
                                                                    "37.717496583956347",
                                                                    "-122.47725527733564",
                                                                ],
                                                                "R": 60,
                                                            },
                                                            {
                                                                "C": [
                                                                    "37.71764944119839",
                                                                    "-122.49895697737561",
                                                                ],
                                                                "R": 60,
                                                            },
                                                            {
                                                                "C": [
                                                                    "37.717667213056735",
                                                                    "-122.49901691485891",
                                                                ],
                                                                "R": 60,
                                                            },
                                                            {
                                                                "C": [
                                                                    "37.717688547859993",
                                                                    "-122.4991956757023",
                                                                ],
                                                                "R": 60,
                                                            },
                                                            {
                                                                "C": [
                                                                    "37.717724699677781",
                                                                    "-122.49916128052689",
                                                                ],
                                                                "R": 60,
                                                            },
                                                            {
                                                                "C": [
                                                                    "37.71776308622492",
                                                                    "-122.49910622197834",
                                                                ],
                                                                "R": 60,
                                                            },
                                                            {
                                                                "C": [
                                                                    "37.717828149235118",
                                                                    "-122.49926074364899",
                                                                ],
                                                                "R": 60,
                                                            },
                                                            {
                                                                "C": [
                                                                    "37.717850723534248",
                                                                    "-122.49901806304297",
                                                                ],
                                                                "R": 60,
                                                            },
                                                            {
                                                                "C": [
                                                                    "37.717943543659111",
                                                                    "-122.49934732425099",
                                                                ],
                                                                "R": 60,
                                                            },
                                                            {
                                                                "C": [
                                                                    "37.717958670014951",
                                                                    "-122.49947536183282",
                                                                ],
                                                                "R": 60,
                                                            },
                                                            {
                                                                "C": [
                                                                    "37.718139096820551",
                                                                    "-122.49962246783517",
                                                                ],
                                                                "R": 60,
                                                            },
                                                            {
                                                                "C": [
                                                                    "37.718172570159304",
                                                                    "-122.49950472740852",
                                                                ],
                                                                "R": 60,
                                                            },
                                                            {
                                                                "C": [
                                                                    "37.718874942690732",
                                                                    "-122.41085517676751",
                                                                ],
                                                                "R": 60,
                                                            },
                                                            {
                                                                "C": [
                                                                    "37.718972494839321",
                                                                    "-122.40045625716448",
                                                                    2,
                                                                ],
                                                                "R": 28,
                                                            },
                                                            {
                                                                "C": [
                                                                    "37.718992798419684",
                                                                    "-122.41045920577784",
                                                                    1,
                                                                ],
                                                                "R": 28,
                                                            },
                                                            {
                                                                "C": [
                                                                    "37.719062705603434",
                                                                    "-122.41018017060594",
                                                                ],
                                                                "R": 60,
                                                            },
                                                            {
                                                                "C": [
                                                                    "37.719235420813135",
                                                                    "-122.4095197409369",
                                                                ],
                                                                "R": 60,
                                                            },
                                                            {
                                                                "C": [
                                                                    "37.719249904455687",
                                                                    "-122.48486135154964",
                                                                    2,
                                                                    2,
                                                                ],
                                                                "R": 12,
                                                            },
                                                            {
                                                                "C": [
                                                                    "37.719373757170771",
                                                                    "-122.44875513017179",
                                                                    0,
                                                                ],
                                                                "R": 44,
                                                            },
                                                            {
                                                                "C": [
                                                                    "37.719969616009628",
                                                                    "-122.42436651251828",
                                                                    1,
                                                                ],
                                                                "R": 28,
                                                            },
                                                            {
                                                                "C": [
                                                                    "37.720041020055689",
                                                                    "-122.46140778064728",
                                                                ],
                                                                "R": 60,
                                                            },
                                                            {
                                                                "C": [
                                                                    "37.72005480169021",
                                                                    "-122.42465112790289",
                                                                ],
                                                                "R": 60,
                                                            },
                                                            {
                                                                "C": [
                                                                    "37.720077112193955",
                                                                    "-122.42478317922408",
                                                                ],
                                                                "R": 60,
                                                            },
                                                            {
                                                                "C": [
                                                                    "37.720235506369477",
                                                                    "-122.42542537277319",
                                                                ],
                                                                "R": 60,
                                                            },
                                                            {
                                                                "C": [
                                                                    "37.720918483820085",
                                                                    "-122.48515391688818",
                                                                ],
                                                                "R": 60,
                                                            },
                                                            {
                                                                "C": [
                                                                    "37.721185821625589",
                                                                    "-122.4851623835341",
                                                                ],
                                                                "R": 60,
                                                            },
                                                            {
                                                                "C": [
                                                                    "37.721415244649023",
                                                                    "-122.48514000746717",
                                                                    2,
                                                                ],
                                                                "R": 28,
                                                            },
                                                            {
                                                                "C": [
                                                                    "37.721540049460451",
                                                                    "-122.38899838593841",
                                                                    4,
                                                                ],
                                                                "R": 28,
                                                            },
                                                            {
                                                                "C": [
                                                                    "37.721573979421436",
                                                                    "-122.48516765195139",
                                                                    1,
                                                                ],
                                                                "R": 28,
                                                            },
                                                            {
                                                                "C": [
                                                                    "37.721904923304606",
                                                                    "-122.48520728819221",
                                                                    3,
                                                                ],
                                                                "R": 28,
                                                            },
                                                            {
                                                                "C": [
                                                                    "37.722229551549148",
                                                                    "-122.39179066882009",
                                                                    1,
                                                                ],
                                                                "R": 28,
                                                            },
                                                            {
                                                                "C": [
                                                                    "37.722300404731214",
                                                                    "-122.48519948439734",
                                                                ],
                                                                "R": 60,
                                                            },
                                                            {
                                                                "C": [
                                                                    "37.722678947988619",
                                                                    "-122.48521367783833",
                                                                ],
                                                                "R": 60,
                                                            },
                                                            {
                                                                "C": [
                                                                    "37.722695608895961",
                                                                    "-122.41761098713933",
                                                                ],
                                                                "R": 60,
                                                            },
                                                            {
                                                                "C": [
                                                                    "37.722882169051431",
                                                                    "-122.48520999068521",
                                                                ],
                                                                "R": 60,
                                                            },
                                                            {
                                                                "C": [
                                                                    "37.723430452398837",
                                                                    "-122.39193712989271",
                                                                    2,
                                                                    4,
                                                                ],
                                                                "R": 12,
                                                            },
                                                            {
                                                                "C": [
                                                                    "37.723583035114558",
                                                                    "-122.41937354207039",
                                                                    0,
                                                                    1,
                                                                ],
                                                                "R": 12,
                                                            },
                                                            {
                                                                "C": [
                                                                    "37.723637009112338",
                                                                    "-122.41381450379878",
                                                                ],
                                                                "R": 60,
                                                            },
                                                            {
                                                                "C": [
                                                                    "37.723684178437317",
                                                                    "-122.391080406707",
                                                                    4,
                                                                ],
                                                                "R": 28,
                                                            },
                                                            {
                                                                "C": [
                                                                    "37.724463478812112",
                                                                    "-122.39070697813426",
                                                                    3,
                                                                ],
                                                                "R": 28,
                                                            },
                                                            {
                                                                "C": [
                                                                    "37.724602290668727",
                                                                    "-122.48494214958644",
                                                                    1,
                                                                ],
                                                                "R": 28,
                                                            },
                                                            {
                                                                "C": [
                                                                    "37.724814822569094",
                                                                    "-122.39067132246728",
                                                                ],
                                                                "R": 60,
                                                            },
                                                            {
                                                                "C": [
                                                                    "37.724847038719972",
                                                                    "-122.48486907384822",
                                                                ],
                                                                "R": 60,
                                                            },
                                                            {
                                                                "C": [
                                                                    "37.724900440019184",
                                                                    "-122.39315573558673",
                                                                    5,
                                                                ],
                                                                "R": 28,
                                                            },
                                                            {
                                                                "C": [
                                                                    "37.72519636234103",
                                                                    "-122.4847149474035",
                                                                    1,
                                                                ],
                                                                "R": 28,
                                                            },
                                                            {
                                                                "C": [
                                                                    "37.725196362341087"
                                                                ],
                                                                "R": 62,
                                                            },
                                                            {
                                                                "C": [
                                                                    "37.725309935196911",
                                                                    "-122.4846828960823",
                                                                    1,
                                                                    0,
                                                                ],
                                                                "R": 12,
                                                            },
                                                            {
                                                                "C": [
                                                                    "37.725338721323929",
                                                                    "-122.38097740134916",
                                                                    0,
                                                                    4,
                                                                ],
                                                                "R": 12,
                                                            },
                                                            {
                                                                "C": [
                                                                    "37.72535883928898",
                                                                    "-122.39229036989023",
                                                                    2,
                                                                ],
                                                                "R": 28,
                                                            },
                                                            {
                                                                "C": [
                                                                    "37.725398670534531",
                                                                    "-122.48464818041926",
                                                                    1,
                                                                ],
                                                                "R": 28,
                                                            },
                                                            {
                                                                "C": [
                                                                    "37.725481238799162",
                                                                    "-122.49914024538562",
                                                                    1,
                                                                    0,
                                                                ],
                                                                "R": 12,
                                                            },
                                                            {
                                                                "C": [
                                                                    "37.725566484400481",
                                                                    "-122.38279255913736",
                                                                    0,
                                                                    1,
                                                                ],
                                                                "R": 12,
                                                            },
                                                            {
                                                                "C": [
                                                                    "37.725613597342367",
                                                                    "-122.47516818344594",
                                                                    3,
                                                                ],
                                                                "R": 28,
                                                            },
                                                            {
                                                                "C": [
                                                                    "37.725739875444511",
                                                                    "-122.4844749347471",
                                                                    1,
                                                                ],
                                                                "R": 28,
                                                            },
                                                            {
                                                                "C": [
                                                                    "37.726066058754931",
                                                                    "-122.48438375551102",
                                                                ],
                                                                "R": 60,
                                                            },
                                                            {
                                                                "C": [
                                                                    "37.726289924147061",
                                                                    "-122.38404314932613",
                                                                    7,
                                                                ],
                                                                "R": 28,
                                                            },
                                                            {
                                                                "C": [
                                                                    "37.726337765504923",
                                                                    "-122.3922001684856",
                                                                    2,
                                                                ],
                                                                "R": 28,
                                                            },
                                                            {
                                                                "C": [
                                                                    "37.726387969823442",
                                                                    "-122.38251796264692",
                                                                    6,
                                                                ],
                                                                "R": 28,
                                                            },
                                                            {
                                                                "C": [
                                                                    "37.72647440419852",
                                                                    "-122.38103014395075",
                                                                    1,
                                                                    2,
                                                                ],
                                                                "R": 12,
                                                            },
                                                            {
                                                                "C": [
                                                                    "37.726481614380013",
                                                                    "-122.50097522258191",
                                                                    0,
                                                                ],
                                                                "R": 28,
                                                            },
                                                            {
                                                                "C": [
                                                                    "37.726624963862065",
                                                                    "-122.38974506765483",
                                                                    0,
                                                                    2,
                                                                ],
                                                                "R": 12,
                                                            },
                                                            {
                                                                "C": [
                                                                    "37.726682469800217",
                                                                    "-122.38340913266785",
                                                                ],
                                                                "R": 60,
                                                            },
                                                            {
                                                                "C": [
                                                                    "37.726835075055106",
                                                                    "-122.3804955011077",
                                                                    10,
                                                                ],
                                                                "R": 28,
                                                            },
                                                            {
                                                                "C": [
                                                                    "37.726910294172647",
                                                                    "-122.3860196399142",
                                                                    2,
                                                                ],
                                                                "R": 28,
                                                            },
                                                            {
                                                                "C": [
                                                                    "37.726970926751164",
                                                                    "-122.38682119219781",
                                                                    4,
                                                                    0,
                                                                ],
                                                                "R": 12,
                                                            },
                                                            {
                                                                "C": [
                                                                    "37.726987998166237",
                                                                    "-122.40020583142712",
                                                                    0,
                                                                    5,
                                                                ],
                                                                "R": 12,
                                                            },
                                                            {
                                                                "C": [
                                                                    "37.7278468721786",
                                                                    "-122.38046347670921",
                                                                    1,
                                                                    2,
                                                                ],
                                                                "R": 12,
                                                            },
                                                            {
                                                                "C": [
                                                                    "37.727960178690758",
                                                                    "-122.38028413215136",
                                                                    0,
                                                                    4,
                                                                ],
                                                                "R": 12,
                                                            },
                                                            {
                                                                "C": [
                                                                    "37.728123811895436",
                                                                    "-122.44386076927184",
                                                                    1,
                                                                ],
                                                                "R": 28,
                                                            },
                                                            {
                                                                "C": [
                                                                    "37.728428235257681",
                                                                    "-122.45144102722406",
                                                                ],
                                                                "R": 60,
                                                            },
                                                            {
                                                                "C": [
                                                                    "37.728537487936208",
                                                                    "-122.49279532581569",
                                                                    2,
                                                                ],
                                                                "R": 28,
                                                            },
                                                            {
                                                                "C": [
                                                                    "37.729027001599377",
                                                                    "-122.49350074678659",
                                                                    1,
                                                                ],
                                                                "R": 28,
                                                            },
                                                            {
                                                                "C": [
                                                                    "37.729239936381191",
                                                                    "-122.44273960590361",
                                                                    1,
                                                                    2,
                                                                ],
                                                                "R": 12,
                                                            },
                                                            {
                                                                "C": [
                                                                    "37.729554962058693",
                                                                    "-122.44141962379217",
                                                                    0,
                                                                ],
                                                                "R": 44,
                                                            },
                                                            {
                                                                "C": [
                                                                    "37.73041438135548",
                                                                    "-122.50197988003492",
                                                                    1,
                                                                    0,
                                                                ],
                                                                "R": 12,
                                                            },
                                                            {
                                                                "C": [
                                                                    "37.732245088868353",
                                                                    "-122.49432787299155",
                                                                    0,
                                                                    1,
                                                                ],
                                                                "R": 12,
                                                            },
                                                            {
                                                                "C": [
                                                                    "37.733102885984621",
                                                                    "-122.47792314738037",
                                                                    2,
                                                                ],
                                                                "R": 28,
                                                            },
                                                            {
                                                                "C": [
                                                                    "37.733703205474349",
                                                                    "-122.47934572398663",
                                                                    1,
                                                                ],
                                                                "R": 28,
                                                            },
                                                            {
                                                                "C": [
                                                                    "37.736773137798075",
                                                                    "-122.50631667673588",
                                                                    1,
                                                                    0,
                                                                ],
                                                                "R": 12,
                                                            },
                                                            {
                                                                "C": [
                                                                    "37.736903324721133",
                                                                    "-122.49356981366874",
                                                                    0,
                                                                    1,
                                                                ],
                                                                "R": 12,
                                                            },
                                                            {
                                                                "C": [
                                                                    "37.737026882770394",
                                                                    "-122.40909565240143",
                                                                ],
                                                                "R": 60,
                                                            },
                                                            {
                                                                "C": [
                                                                    "37.737385621607487",
                                                                    "-122.39042978188117",
                                                                ],
                                                                "R": 60,
                                                            },
                                                            {
                                                                "C": [
                                                                    "37.7377072437853",
                                                                    "-122.42091044783592",
                                                                    3,
                                                                ],
                                                                "R": 28,
                                                            },
                                                            {
                                                                "C": [
                                                                    "37.738388782397479",
                                                                    "-122.39049752620529",
                                                                    9,
                                                                ],
                                                                "R": 28,
                                                            },
                                                            {
                                                                "C": [
                                                                    "37.738645315086643",
                                                                    "-122.50661976635455",
                                                                    1,
                                                                ],
                                                                "R": 28,
                                                            },
                                                            {
                                                                "C": [
                                                                    "37.740130138068871",
                                                                    "-122.3854696711436",
                                                                    2,
                                                                    6,
                                                                ],
                                                                "R": 12,
                                                            },
                                                            {
                                                                "C": [
                                                                    "37.741087397394068",
                                                                    "-122.50680184525761",
                                                                    0,
                                                                    1,
                                                                ],
                                                                "R": 12,
                                                            },
                                                            {
                                                                "C": [
                                                                    "37.74141380758531",
                                                                    "-122.40253328073702",
                                                                    2,
                                                                ],
                                                                "R": 28,
                                                            },
                                                            {
                                                                "C": [
                                                                    "37.742260410858556",
                                                                    "-122.41228748112918",
                                                                    1,
                                                                ],
                                                                "R": 28,
                                                            },
                                                            {
                                                                "C": [
                                                                    "37.742464558415115",
                                                                    "-122.50707138329743",
                                                                    2,
                                                                ],
                                                                "R": 44,
                                                            },
                                                            {
                                                                "C": [
                                                                    "37.743223346085763",
                                                                    "-122.49451495707035",
                                                                    0,
                                                                ],
                                                                "R": 44,
                                                            },
                                                            {
                                                                "C": [
                                                                    "37.743330986194493",
                                                                    "-122.5072219222784",
                                                                    2,
                                                                ],
                                                                "R": 28,
                                                            },
                                                            {
                                                                "C": [
                                                                    "37.743555280105326",
                                                                    "-122.50711999833582",
                                                                ],
                                                                "R": 60,
                                                            },
                                                            {
                                                                "C": [
                                                                    "37.743718187676961",
                                                                    "-122.39932650074638",
                                                                    10,
                                                                ],
                                                                "R": 28,
                                                            },
                                                            {
                                                                "C": [
                                                                    "37.744329433535775",
                                                                    "-122.50732250511646",
                                                                    3,
                                                                ],
                                                                "R": 28,
                                                            },
                                                            {
                                                                "C": [
                                                                    "37.744771121556937",
                                                                    "-122.47966390103102",
                                                                    1,
                                                                ],
                                                                "R": 28,
                                                            },
                                                            {
                                                                "C": [
                                                                    "37.7449185812056",
                                                                    "-122.38842577051989",
                                                                    9,
                                                                ],
                                                                "R": 28,
                                                            },
                                                            {
                                                                "C": [
                                                                    "37.74700449623829",
                                                                    "-122.39854109145446",
                                                                    7,
                                                                ],
                                                                "R": 28,
                                                            },
                                                            {
                                                                "C": [
                                                                    "37.747284133069464",
                                                                    "-122.50739458948374",
                                                                    2,
                                                                ],
                                                                "R": 28,
                                                            },
                                                            {
                                                                "C": [
                                                                    "37.748071350894136",
                                                                    "-122.39004851258146",
                                                                    3,
                                                                    4,
                                                                ],
                                                                "R": 12,
                                                            },
                                                            {
                                                                "C": [
                                                                    "37.748328655422547",
                                                                    "-122.48425215482712",
                                                                    1,
                                                                    1,
                                                                ],
                                                                "R": 12,
                                                            },
                                                            {
                                                                "C": [
                                                                    "37.749112830678968",
                                                                    "-122.39037425637507",
                                                                    4,
                                                                    0,
                                                                ],
                                                                "R": 12,
                                                            },
                                                            {
                                                                "C": [
                                                                    "37.749456404883219",
                                                                    "-122.50799372792245",
                                                                    1,
                                                                    1,
                                                                ],
                                                                "R": 12,
                                                            },
                                                            {
                                                                "C": [
                                                                    "37.749946194916355",
                                                                    "-122.39034901027696",
                                                                    5,
                                                                ],
                                                                "R": 28,
                                                            },
                                                            {
                                                                "C": [
                                                                    "37.751511706604433",
                                                                    "-122.48172383755445",
                                                                    0,
                                                                ],
                                                                "R": 28,
                                                            },
                                                            {
                                                                "C": [
                                                                    "37.751877265210666",
                                                                    "-122.38667875539733",
                                                                    0,
                                                                    3,
                                                                ],
                                                                "R": 12,
                                                            },
                                                            {
                                                                "C": [
                                                                    "37.752325866320426",
                                                                    "-122.38676389555812",
                                                                    1,
                                                                ],
                                                                "R": 28,
                                                            },
                                                            {
                                                                "C": [
                                                                    "37.752737584628292",
                                                                    "-122.38680404947097",
                                                                ],
                                                                "R": 60,
                                                            },
                                                            {
                                                                "C": [
                                                                    "37.75397872701943",
                                                                    "-122.5085588320952",
                                                                ],
                                                                "R": 60,
                                                            },
                                                            {
                                                                "C": [
                                                                    "37.754193748557292",
                                                                    "-122.38668962294622",
                                                                    1,
                                                                    0,
                                                                ],
                                                                "R": 12,
                                                            },
                                                            {
                                                                "C": [
                                                                    "37.754501476817467",
                                                                    "-122.39861993819044",
                                                                    0,
                                                                    1,
                                                                ],
                                                                "R": 12,
                                                            },
                                                            {
                                                                "C": [
                                                                    "37.754564378914488",
                                                                    "-122.50867230779103",
                                                                ],
                                                                "R": 60,
                                                            },
                                                            {
                                                                "C": [
                                                                    "37.754735067144551",
                                                                    "-122.3978829023149",
                                                                    1,
                                                                    2,
                                                                ],
                                                                "R": 12,
                                                            },
                                                            {
                                                                "C": [
                                                                    "37.755582376893877",
                                                                    "-122.50881012529135",
                                                                    1,
                                                                ],
                                                                "R": 28,
                                                            },
                                                            {
                                                                "C": [
                                                                    "37.757899664172413",
                                                                    "-122.50908974558115",
                                                                ],
                                                                "R": 60,
                                                            },
                                                            {
                                                                "C": [
                                                                    "37.759336600296272",
                                                                    "-122.50928990542889",
                                                                    3,
                                                                ],
                                                                "R": 28,
                                                            },
                                                            {
                                                                "C": [
                                                                    "37.759363902077489",
                                                                    "-122.50898681581022",
                                                                    0,
                                                                ],
                                                                "R": 28,
                                                            },
                                                            {
                                                                "C": [
                                                                    "37.759549182831378",
                                                                    "-122.50933650881052",
                                                                    2,
                                                                ],
                                                                "R": 44,
                                                            },
                                                            {
                                                                "C": [
                                                                    37.760633878336,
                                                                    "-122.41267413843647",
                                                                    0,
                                                                    2,
                                                                ],
                                                                "R": 12,
                                                            },
                                                            {
                                                                "C": [
                                                                    "37.760672785359539",
                                                                    "-122.50944513827561",
                                                                    1,
                                                                    1,
                                                                ],
                                                                "R": 12,
                                                            },
                                                            {
                                                                "C": [
                                                                    "37.761571021432047",
                                                                    "-122.41268439790647",
                                                                    0,
                                                                    3,
                                                                ],
                                                                "R": 12,
                                                            },
                                                            {
                                                                "C": [
                                                                    "37.762179907408978",
                                                                    "-122.50927481800319",
                                                                    1,
                                                                ],
                                                                "R": 28,
                                                            },
                                                            {
                                                                "C": [
                                                                    "37.763039494200974",
                                                                    "-122.41055528898117",
                                                                ],
                                                                "R": 60,
                                                            },
                                                            {
                                                                "C": [
                                                                    "37.763122978407239",
                                                                    "-122.40908252038302",
                                                                ],
                                                                "R": 60,
                                                            },
                                                            {
                                                                "C": [
                                                                    "37.763216798029219",
                                                                    "-122.50974152237177",
                                                                    1,
                                                                    2,
                                                                ],
                                                                "R": 12,
                                                            },
                                                            {
                                                                "C": [
                                                                    "37.7632391585547",
                                                                    "-122.41028605821197",
                                                                    0,
                                                                    1,
                                                                ],
                                                                "R": 12,
                                                            },
                                                            {
                                                                "C": [
                                                                    "37.763535106771677",
                                                                    "-122.41122451975039",
                                                                    2,
                                                                ],
                                                                "R": 28,
                                                            },
                                                            {
                                                                "C": [
                                                                    "37.763586874398953",
                                                                    "-122.41224613043485",
                                                                    1,
                                                                    3,
                                                                ],
                                                                "R": 12,
                                                            },
                                                            {
                                                                "C": [
                                                                    "37.763979613698787",
                                                                    "-122.50620938837528",
                                                                    0,
                                                                    1,
                                                                ],
                                                                "R": 12,
                                                            },
                                                            {
                                                                "C": [
                                                                    "37.764096235275993",
                                                                    "-122.50867802649735",
                                                                    1,
                                                                    2,
                                                                ],
                                                                "R": 12,
                                                            },
                                                            {
                                                                "C": [
                                                                    "37.764366319540741",
                                                                    "-122.50403512269258",
                                                                    3,
                                                                    0,
                                                                ],
                                                                "R": 12,
                                                            },
                                                            {
                                                                "C": [
                                                                    "37.76439908416031",
                                                                    "-122.5024856589753",
                                                                    0,
                                                                    1,
                                                                ],
                                                                "R": 12,
                                                            },
                                                            {
                                                                "C": [
                                                                    "37.764563468470762",
                                                                    "-122.49850545606033",
                                                                ],
                                                                "R": 60,
                                                            },
                                                            {
                                                                "C": [
                                                                    "37.764596115680305",
                                                                    "-122.49784156680107",
                                                                    2,
                                                                ],
                                                                "R": 28,
                                                            },
                                                            {
                                                                "C": [
                                                                    "37.764735795337813",
                                                                    "-122.49506782740355",
                                                                    3,
                                                                ],
                                                                "R": 28,
                                                            },
                                                            {
                                                                "C": [
                                                                    "37.7648970629921",
                                                                    "-122.49162671891754",
                                                                    1,
                                                                ],
                                                                "R": 28,
                                                            },
                                                            {
                                                                "C": [
                                                                    "37.764997593373245",
                                                                    "-122.41138379492084",
                                                                ],
                                                                "R": 60,
                                                            },
                                                            {
                                                                "C": [
                                                                    "37.765159603538045",
                                                                    "-122.48572167009115",
                                                                    1,
                                                                    0,
                                                                ],
                                                                "R": 12,
                                                            },
                                                            {
                                                                "C": [
                                                                    "37.765370570806979",
                                                                    "-122.48097666918403",
                                                                ],
                                                                "R": 60,
                                                            },
                                                            {
                                                                "C": [
                                                                    "37.76544903213285",
                                                                    "-122.47929509729147",
                                                                    0,
                                                                    2,
                                                                ],
                                                                "R": 12,
                                                            },
                                                            {
                                                                "C": [
                                                                    "37.765676829448779",
                                                                    "-122.47409655144888",
                                                                    1,
                                                                ],
                                                                "R": 28,
                                                            },
                                                            {
                                                                "C": [
                                                                    "37.765761783370465",
                                                                    "-122.47291848063469",
                                                                    1,
                                                                    0,
                                                                ],
                                                                "R": 12,
                                                            },
                                                            {
                                                                "C": [
                                                                    "37.765921334536131",
                                                                    "-122.46834842050409",
                                                                    0,
                                                                    1,
                                                                ],
                                                                "R": 12,
                                                            },
                                                            {
                                                                "C": [
                                                                    "37.766664665284338",
                                                                    "-122.40567234957589",
                                                                    1,
                                                                ],
                                                                "R": 44,
                                                            },
                                                            {
                                                                "C": [
                                                                    "37.767199395871948",
                                                                    "-122.40480381721289",
                                                                    3,
                                                                ],
                                                                "R": 28,
                                                            },
                                                            {
                                                                "C": [
                                                                    "37.767220709647923",
                                                                    "-122.4057106434566",
                                                                    0,
                                                                    4,
                                                                ],
                                                                "R": 12,
                                                            },
                                                            {
                                                                "C": [
                                                                    "37.767240676567106",
                                                                    "-122.40766197985201",
                                                                    1,
                                                                ],
                                                                "R": 28,
                                                            },
                                                            {
                                                                "C": [
                                                                    "37.767669822417481",
                                                                    "-122.41327624874044",
                                                                    2,
                                                                ],
                                                                "R": 28,
                                                            },
                                                            {
                                                                "C": [
                                                                    "37.768184755638913",
                                                                    "-122.41235072182037",
                                                                    1,
                                                                    1,
                                                                ],
                                                                "R": 12,
                                                            },
                                                            {
                                                                "C": [
                                                                    "37.768237143051849",
                                                                    "-122.405644219085",
                                                                ],
                                                                "R": 60,
                                                            },
                                                            {
                                                                "C": [
                                                                    "37.76837472783513",
                                                                    "-122.43898661273069",
                                                                    0,
                                                                ],
                                                                "R": 28,
                                                            },
                                                            {
                                                                "C": [
                                                                    "37.770300503088777",
                                                                    "-122.44477406144141",
                                                                    0,
                                                                    1,
                                                                ],
                                                                "R": 12,
                                                            },
                                                            {
                                                                "C": [
                                                                    "37.7703082523366",
                                                                    "-122.51033220597934",
                                                                    1,
                                                                ],
                                                                "R": 44,
                                                            },
                                                            {
                                                                "C": [
                                                                    "37.771397970073295",
                                                                    "-122.5082203745842",
                                                                    2,
                                                                    0,
                                                                ],
                                                                "R": 12,
                                                            },
                                                            {
                                                                "C": [
                                                                    "37.771578185263316",
                                                                    "-122.50968385487793",
                                                                    0,
                                                                    1,
                                                                ],
                                                                "R": 12,
                                                            },
                                                            {
                                                                "C": [
                                                                    "37.7715975318679",
                                                                    "-122.50500977039337",
                                                                    2,
                                                                ],
                                                                "R": 44,
                                                            },
                                                            {
                                                                "C": [
                                                                    "37.771786492273918",
                                                                    "-122.50078663229942",
                                                                    0,
                                                                ],
                                                                "R": 44,
                                                            },
                                                            {
                                                                "C": [
                                                                    "37.772247097804218",
                                                                    "-122.4406887218356",
                                                                ],
                                                                "R": 60,
                                                            },
                                                            {
                                                                "C": [
                                                                    "37.772337999477216",
                                                                    "-122.48802132904531",
                                                                ],
                                                                "R": 60,
                                                            },
                                                            {
                                                                "C": [
                                                                    "37.772487492054076",
                                                                    "-122.44323046518809",
                                                                ],
                                                                "R": 60,
                                                            },
                                                            {
                                                                "C": [
                                                                    "37.772596392835347",
                                                                    "-122.48228508979082",
                                                                    1,
                                                                    0,
                                                                ],
                                                                "R": 12,
                                                            },
                                                            {
                                                                "C": [
                                                                    "37.77275760395375",
                                                                    "-122.44775400116453",
                                                                ],
                                                                "R": 60,
                                                            },
                                                            {
                                                                "C": [
                                                                    "37.772902810307613",
                                                                    "-122.44662042630463",
                                                                ],
                                                                "R": 60,
                                                            },
                                                            {
                                                                "C": [
                                                                    "37.773139413472734",
                                                                    "-122.47066006064415",
                                                                    3,
                                                                ],
                                                                "R": 28,
                                                            },
                                                            {
                                                                "C": [
                                                                    "37.773150366839559",
                                                                    "-122.44463039581251",
                                                                    0,
                                                                ],
                                                                "R": 28,
                                                            },
                                                            {
                                                                "C": [
                                                                    "37.773556322068494",
                                                                    "-122.44162390023325",
                                                                    1,
                                                                ],
                                                                "R": 28,
                                                            },
                                                            {
                                                                "C": [
                                                                    "37.774078149351325",
                                                                    "-122.45975046406195",
                                                                    0,
                                                                ],
                                                                "R": 28,
                                                            },
                                                            {
                                                                "C": [
                                                                    "37.775000000000013",
                                                                    "-122.41830000000002",
                                                                    3,
                                                                    5,
                                                                ],
                                                                "R": 12,
                                                            },
                                                            {
                                                                "C": [
                                                                    "37.775772569725625",
                                                                    "-122.51170054078102",
                                                                    0,
                                                                    1,
                                                                ],
                                                                "R": 12,
                                                            },
                                                            {
                                                                "C": [
                                                                    "37.77926501423083",
                                                                    "-122.50263568013908",
                                                                ],
                                                                "R": 60,
                                                            },
                                                            {
                                                                "C": [
                                                                    "37.77945051012113",
                                                                    "-122.50295385718347",
                                                                ],
                                                                "R": 60,
                                                            },
                                                            {
                                                                "C": [
                                                                    "37.779580886954044",
                                                                    "-122.50517942011358",
                                                                ],
                                                                "R": 60,
                                                            },
                                                            {
                                                                "C": [
                                                                    "37.781289279204664",
                                                                    "-122.50150110572575",
                                                                ],
                                                                "R": 60,
                                                            },
                                                            {
                                                                "C": [
                                                                    "37.781413823085906",
                                                                    "-122.49951593577863",
                                                                    1,
                                                                    2,
                                                                ],
                                                                "R": 12,
                                                            },
                                                            {
                                                                "C": [
                                                                    "37.784075037188821",
                                                                    "-122.44733422994612",
                                                                    0,
                                                                ],
                                                                "R": 44,
                                                            },
                                                        ]
                                                    }
                                                ],
                                            },
                                        ]
                                    }
                                ],
                                "IC": true,
                                "HAD": true,
                            }
                        ],
                    },
                }
            },
        }
    ],
}
