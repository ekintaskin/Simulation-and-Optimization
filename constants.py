import numpy as np

TIME_INTERVALS = [
    (0, 1200),  # 0-20min
    (1200, 2400),  # 20-40min
    (2400, 3600),  # 40-60min
]

GROUP_IDS = {"G1", "G2", "G3"}
STORAGE_IDS = {"MSN", "ASN1", "ASN2"}
MOVIES_IDS = {0, 1, 2, 3, 4, 5, 6, 7, 8, 9}

GROUP_ACTIVITIES = {
    "G1": [0.8, 1.2, 0.5],
    "G2": [0.9, 1.3, 0.3],
    "G3": [0.7, 1.5, 0.4],
}

GROUP_STORAGE_OPTIONS = {
    "G1": ["MSN", "ASN1"],
    "G2": ["MSN", "ASN1", "ASN2"],
    "G3": ["MSN", "ASN2"],
}

GROUP_MOVIE_POPULARITIES = {
    "G1": { 0:2, 1:4, 2:9, 3:8, 4:1, 5:3, 6:5, 7:7, 8:10, 9:6 },
    "G2": { 0:6, 1:1, 2:3, 3:4, 4:7, 5:9, 6:2, 7:5, 8:8, 9:10 },
    "G3": { 0:4, 1:7, 2:3, 3:6, 4:1, 5:10, 6:2, 7:9, 8:8, 9:5 },
}

RHO_SEND_TIME  = {
    "G1": {"MSN": 0.5, "ASN1": 0.2},
    "G2": {"MSN": 0.5, "ASN1": 0.3, "ASN2": 0.4},
    "G3": {"MSN": 0.5, "ASN2": 0.2},
}

MOVIE_SIZES = {
    0: 850, 1: 950, 2: 1000, 3: 1200, 4: 800,
    5: 900, 6: 1000, 7: 750, 8: 700, 9: 1100
}

# 1st baseline movie hashset
INITIAL_MOVIE_HASHSET = {
    "MSN": {0, 1, 2, 3, 4, 5, 6, 7, 8, 9},
    "ASN1": {2, 3, 9},
    "ASN2": {2, 3, 9}
}

# # 2nd baseline movie hashset
# INITIAL_MOVIE_HASHSET = {
#     "MSN": {0, 1, 2, 3, 4, 5, 6, 7, 8, 9},
#     "ASN1": {2, 3, 9},
#     "ASN2": {2, 3, 9}
# }

STORAGE_SIZES = {
    "MSN": np.inf,
    "ASN1": 3500,
    "ASN2": 3500,
}

MU_SERVE_TIME = {
    "G1": {
        "MSN": {"small": 9, "medium": 12, "large": 15},
        "ASN1": {"small": 3, "medium": 4, "large": 5},
    },
    "G2": {
        "MSN": {"small": 8, "medium": 11, "large": 14},
        "ASN1": {"small": 4, "medium": 5, "large": 6},
        "ASN2": {"small": 5, "medium": 6, "large": 7},
    },
    "G3": {
        "MSN": {"small": 10, "medium": 13, "large": 16},
        "ASN2": {"small": 4, "medium": 5, "large": 6},
    },
}

BOUND_SERVE_TIME = (0.3, 0.7)

STORAGE_HANDLE_TIME_BETA = 0.5