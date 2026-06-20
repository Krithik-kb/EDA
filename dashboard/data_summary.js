const edaDataSummary = {
    "metrics": {
        "totalCustomers": 1000,
        "churnCount": 148,
        "churnRate": 14.8,
        "avgTenure": 36.24,
        "avgMonthlyCharges": 59.19,
        "avgAge": 46.51
    },
    "raw_vs_cleaned": {
        "raw_shape": [
            1015,
            10
        ],
        "cleaned_shape": [
            1000,
            10
        ],
        "raw_duplicates": 15,
        "cleaned_duplicates": 0,
        "raw_nulls": {
            "CustomerID": 0,
            "Gender": 0,
            "Age": 20,
            "Tenure": 0,
            "PaymentMethod": 0,
            "ContractType": 0,
            "MonthlyCharges": 0,
            "TotalCharges": 30,
            "SupportCalls": 0,
            "Churn": 0
        },
        "cleaned_nulls": {
            "CustomerID": 0,
            "Gender": 0,
            "Age": 0,
            "Tenure": 0,
            "PaymentMethod": 0,
            "ContractType": 0,
            "MonthlyCharges": 0,
            "TotalCharges": 0,
            "SupportCalls": 0,
            "Churn": 0
        }
    },
    "distributions": {
        "age": {
            "labels": [
                "18-23",
                "23-29",
                "29-34",
                "34-40",
                "40-46",
                "46-51",
                "51-57",
                "57-62",
                "62-68",
                "68-74"
            ],
            "values": [
                96,
                102,
                85,
                110,
                78,
                128,
                95,
                78,
                116,
                112
            ]
        },
        "tenure": {
            "labels": [
                "1-8",
                "8-15",
                "15-22",
                "22-29",
                "29-36",
                "36-43",
                "43-50",
                "50-57",
                "57-64",
                "64-71"
            ],
            "values": [
                86,
                94,
                108,
                108,
                90,
                97,
                108,
                95,
                108,
                106
            ]
        },
        "monthlyCharges": {
            "labels": [
                "16-25",
                "25-34",
                "34-44",
                "44-53",
                "53-62",
                "62-72",
                "72-81",
                "81-91",
                "91-100",
                "100-109"
            ],
            "values": [
                97,
                110,
                121,
                120,
                110,
                110,
                105,
                94,
                86,
                47
            ]
        }
    },
    "segments": {
        "gender": {
            "counts": {
                "Female": {
                    "0": 429,
                    "1": 81
                },
                "Male": {
                    "0": 423,
                    "1": 67
                }
            },
            "rates": {
                "Female": 15.88,
                "Male": 13.67
            }
        },
        "payment": {
            "counts": {
                "Bank Transfer": {
                    "0": 310,
                    "1": 47
                },
                "Credit Card": {
                    "0": 326,
                    "1": 59
                },
                "PayPal": {
                    "0": 216,
                    "1": 42
                }
            },
            "rates": {
                "Bank Transfer": 13.17,
                "Credit Card": 15.32,
                "PayPal": 16.28
            }
        },
        "contract": {
            "counts": {
                "Month-to-month": {
                    "0": 375,
                    "1": 123
                },
                "One year": {
                    "0": 222,
                    "1": 20
                },
                "Two year": {
                    "0": 255,
                    "1": 5
                }
            },
            "rates": {
                "Month-to-month": 24.7,
                "One year": 8.26,
                "Two year": 1.92
            }
        },
        "support": {
            "counts": {
                "0": {
                    "0": 192,
                    "1": 18
                },
                "1": {
                    "0": 299,
                    "1": 34
                },
                "2": {
                    "0": 212,
                    "1": 47
                },
                "3": {
                    "0": 106,
                    "1": 30
                },
                "4": {
                    "0": 28,
                    "1": 8
                },
                "5": {
                    "0": 11,
                    "1": 10
                },
                "6": {
                    "0": 3,
                    "1": 1
                },
                "7": {
                    "0": 1,
                    "1": 0
                }
            },
            "rates": {
                "0": 8.57,
                "1": 10.21,
                "2": 18.15,
                "3": 22.06,
                "4": 22.22,
                "5": 47.62,
                "6": 25.0,
                "7": 0.0
            }
        },
        "age_group": {
            "counts": {
                "Under 25": {
                    "0": 113,
                    "1": 13
                },
                "25-34": {
                    "0": 153,
                    "1": 19
                },
                "35-44": {
                    "0": 151,
                    "1": 22
                },
                "45-54": {
                    "0": 168,
                    "1": 23
                },
                "55-64": {
                    "0": 127,
                    "1": 41
                },
                "65+": {
                    "0": 140,
                    "1": 30
                }
            },
            "rates": {
                "Under 25": 10.32,
                "25-34": 11.05,
                "35-44": 12.72,
                "45-54": 12.04,
                "55-64": 24.4,
                "65+": 17.65
            }
        }
    },
    "correlation": {
        "features": [
            "Age",
            "Tenure",
            "MonthlyCharges",
            "TotalCharges",
            "SupportCalls",
            "Churn"
        ],
        "values": [
            [
                1.0,
                0.008,
                -0.025,
                -0.007,
                -0.073,
                0.103
            ],
            [
                0.008,
                1.0,
                0.019,
                0.766,
                0.021,
                -0.376
            ],
            [
                -0.025,
                0.019,
                1.0,
                0.572,
                0.034,
                0.115
            ],
            [
                -0.007,
                0.766,
                0.572,
                1.0,
                0.034,
                -0.239
            ],
            [
                -0.073,
                0.021,
                0.034,
                0.034,
                1.0,
                0.179
            ],
            [
                0.103,
                -0.376,
                0.115,
                -0.239,
                0.179,
                1.0
            ]
        ]
    }
};
