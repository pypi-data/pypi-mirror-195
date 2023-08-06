DEFAULT_SCHEMA_URL = 'https://raw.githubusercontent.com/dsakovych/similarity-engine-utils/main/examples/schema_yp.json'

DEFAULT_SEARCH_PARAMS = {
    "metric_type": "L2",
    "params": {
        "nprobe": 1
    },
    "offset": 0
}

# L2 distances
VECTOR_SIM_THRESHOLDS = {
    "google/vit-large-patch16-224-in21k": 1.4
}
