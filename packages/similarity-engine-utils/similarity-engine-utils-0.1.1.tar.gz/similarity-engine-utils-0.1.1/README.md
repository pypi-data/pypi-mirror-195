# similarity-engine-utils

Utility tools for easier management of feature-vector database and similar 
vector comparison

## Installation
---------------

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install library.

```bash
pip install similarity-engine-utils
```

## Setup backend connection (milvus)
---------------------------

```python
from se_utils.backend.milvus.core import setup_connection
milvus_credentials = {
    "alias": "default",
    "host": "localhost",
    "port": "19530"
}
collection_name = 'test_collection'

c = setup_connection(milvus_credentials)
```

## Create collection
---------------------------

```python
from se_utils.backend.milvus.core import create_milvus_collection, generate_schema, read_schema_json

collection_name = 'test_collection'

schema_path = "/path/to/schema.json"
tag = "some_tag"

# existing tag
collection1 = create_milvus_collection(collection_name, tag=tag)

# parse json schema
collection_schema, index_params = generate_schema(tag=tag, 
                                                  schema=read_schema_json(schema_path))
collection2 = create_milvus_collection(collection_name, 
                                       schema=collection_schema, 
                                       indices=index_params)
```


## Insert data to collection
---------------------------

```python
from se_utils.backend.milvus.core import insert2milvus

collection_name = 'test_collection'
kwargs = {
    "id": 1,
    "name": "name",
    "emb": [1,1,1,1]
}

insert2milvus(data=[kwargs], 
              collection_name=collection_name)
```

## Find the closest cluster id
---------------------------

```python
import numpy as np
from se_utils.backend.milvus.core import get_cluster_id, get_increment_cluster_id

collection_name = 'test_collection'
emb_label = 'emb'
emb = [np.random.uniform(low=-1, high=1, size=(1024,)).tolist() 
       for _ in range(1)][0]
cluster_label = 'group_id'

cluster_id = get_cluster_id(collection_name=collection_name, 
                            emb=emb, 
                            emb_label=emb_label, 
                            cluster_label=cluster_label)

if cluster_id is None:
    cluster_id = get_increment_cluster_id(collection_name=collection_name, 
                                          cluster_label=cluster_label)

```