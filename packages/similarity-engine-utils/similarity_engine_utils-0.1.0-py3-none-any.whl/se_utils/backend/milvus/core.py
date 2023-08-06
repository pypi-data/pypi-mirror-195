import json
import os.path
import re
import numpy as np
import pandas as pd
import requests
from pymilvus import (Collection, CollectionSchema, DataType, FieldSchema,
                      connections, utility)

from ...exceptions import (
    BadCredentialsError, MilvusInsertDataSchemaError, SchemaValidationError,
    MilvusFieldDescriptionAbsentError)
from .conf import DEFAULT_SCHEMA_URL, DEFAULT_SEARCH_PARAMS, VECTOR_SIM_THRESHOLDS


def setup_connection(milvus_credentials: dict):
    if milvus_credentials.keys() != {"host", "port", "alias"}:
        message = f"Provided credentials are incorrect: {milvus_credentials}"
        raise BadCredentialsError(message=message)

    connections.connect(**milvus_credentials)
    return True


def milvus_dtype_mapping(x: str):
    res = None
    if re.match(r"VARCHAR\(\d+\)$", x):
        max_length = re.findall(r".*\((\d+)\).*", x)[0]
        res = {"dtype": DataType.VARCHAR, "max_length": max_length}

    elif re.match(r"FLOAT_VECTOR\(\d+\)$", x):
        dim = re.findall(r".*\((\d+)\).*", x)[0]
        res = {"dtype": DataType.FLOAT_VECTOR, "dim": dim}

    elif re.match(r"INT\d+$", x):
        bits = int(re.findall(r".*?(\d+)", x)[0])
        if bits in {8, 16, 32, 64}:
            res = {"dtype": DataType[x]}

    elif re.match(r"FLOAT$|DOUBLE$", x):
        res = {"dtype": DataType[x]}

    else:
        formats = ['VARCHAR(int)', 'FLOAT_VECTOR(int)' 'INT8', 'INT16',
                   'INT32', 'INT64']
        raise ValueError(f"Bad input: {x}. Available formats: {formats}")

    return res


def read_schema_json(x: str):
    if os.path.exists(x):
        with open(x) as f:
            schema_json = json.load(f)
    else:
        schema_json = json.loads(x)
    validate_schema(schema_json)
    return schema_json


def validate_schema(schema: list[dict]):
    pk, msg = None, None
    available_keys = {'name', 'dtype', 'is_primary', 'description',
                      'index_params'}
    for item in schema:
        keys = set(item.keys())
        if not keys.issubset(available_keys):
            msg = f"Wrong schema keys: {keys}"
            break
        if item.get('is_primary'):
            if pk is None:
                pk = item['name']
            else:
                msg = f"Can't have more then 1 primary_key: `{pk}, {item['name']}`"
                break
        if re.match(r"FLOAT_VECTOR\(\d+\)$", item.get('dtype', '')):
            index_params_keys = {'metric_type', 'index_type', 'params'}
            if item.get('is_primary'):
                msg = f"Vector `{item['name']}` can't be a primary_key"
                break
            if not item.get('index_params'):
                msg = f"Vector `{item['name']}` doesn't have `index_params`"
                break
            keys = set(item.get('index_params').keys())
            if not keys.issubset(index_params_keys):
                msg = f"Vector `{item['name']} has wrong " \
                      f"index_params_keys keys: {keys}"
                break
        try:
            milvus_dtype_mapping(item['dtype'])
        except ValueError as e:
            msg = f"`dtype` validation error: {e}"
    if pk is None:
        msg = "Primary key is absent"
    if msg is not None:
        raise SchemaValidationError(message=msg)
    return True


def parse_schema(schema: list):
    validate_schema(schema)
    fields, index_params = [], {}
    for item in schema:
        if item.get('index_params'):
            index_params.update({item['name']: item['index_params']})
            item.pop('index_params')
        item.update(milvus_dtype_mapping(item['dtype']))
        fields.append(FieldSchema(**item))

    return fields, index_params


def open_schema_url(url):
    schema = json.loads(requests.get(url).content.decode())
    validate_schema(schema)
    return schema


def generate_schema(
        tag: str = None,
        schema: list = None
) -> (CollectionSchema, dict):
    if tag == 'yp':
        schema = open_schema_url(DEFAULT_SCHEMA_URL)
    elif schema is None:
        raise ValueError(f"Such tag is not supported: `{tag}`. "
                         f"Either provide existing tag, "
                         f"or provide valid schema")
    fields, index_params = parse_schema(schema)

    collection_schema = CollectionSchema(
        fields=fields,
        description='test collection')

    return collection_schema, index_params


def create_milvus_collection(
        collection_name,
        tag: str = 'yp',
        drop_existing: bool = True,
        schema: CollectionSchema = None,
        indices: list[dict] = None
):
    if schema is None and indices is None:
        schema, indices = generate_schema(tag)

    if utility.has_collection(collection_name):
        if drop_existing:
            utility.drop_collection(collection_name)
        else:
            collection = Collection(collection_name)
            collection.load()
            return collection
    collection = Collection(name=collection_name, schema=schema)

    for field_name, index_params in indices.items():
        collection.create_index(field_name=field_name,
                                index_params=index_params)
    return collection


def insert2milvus(data: list[dict], collection_name):
    df = pd.DataFrame(data)
    collection = Collection(collection_name)
    collection_fields = [_.name for _ in collection.schema.fields]
    data_fields = df.columns

    absent_fields = [_ for _ in data_fields if _ not in collection_fields]
    redundant_fields = [_ for _ in collection_fields if _ not in data_fields]

    if set(data_fields) == set(collection_fields):
        collection.insert(df[collection_fields])
        return True
    if len(absent_fields) > 0:
        msg = f"Such fields are absent " \
              f"in provided df: {absent_fields}"
    elif len(redundant_fields) > 0:
        msg = f"Such fields are redundant " \
              f"in provided df: {redundant_fields}"
    else:
        msg = f"No data fields provided: {data_fields}"
    raise MilvusInsertDataSchemaError(message=msg)


def query_milvus_data(collection_name,
                      output_fields,
                      expr: str,
                      limit: int = 10):
    collection = Collection(collection_name)
    collection.load()
    res = collection.query(
        expr=expr,
        offset=0,
        limit=limit,
        output_fields=output_fields,
        consistency_level="Strong"
    )
    return res


def search_similar_vector(
        collection_name,
        field_name,
        data,
        output_fields,
        limit=10,
        expr=None,
        search_params=DEFAULT_SEARCH_PARAMS

):
    collection = Collection(collection_name)
    collection.load()

    results = collection.search(
        data=[data],
        anns_field=field_name,
        param=search_params,
        limit=limit,
        expr=expr,
        output_fields=output_fields,
        consistency_level="Strong"
    )
    res = [{
        "distance": i.score,
        "values": {j: i.entity.get(j) for j in output_fields}  # i.entity._row_data
    }
        for i in results[0]]
    return res


def l2_dist(a, b):
    return np.linalg.norm(a - b)


# def get_cluster_id(collection_name, emb, emb_label, cluster_label):
#     # todo: use this function after this is merged https://github.com/milvus-io/milvus/issues/16538
#     # todo: get model name from search results
#     model_name = "google/vit-large-patch16-224-in21k"
#     results = search_similar_vector(
#         collection_name=collection_name,
#         field_name=emb_label,
#         data=emb,
#         output_fields=[cluster_label, emb_label],
#         limit=1
#     )
#     if len(results) > 0:
#         cluster_id = results[0]['values'][cluster_label]
#         closest_vector = results[0]['values'][cluster_label]
#         if l2_dist(emb, closest_vector) < VECTOR_SIM_THRESHOLDS[model_name]:
#             return cluster_id


def get_cluster_id(collection_name, emb, emb_label, cluster_label):
    model_name = [item
                  for item in Collection(collection_name).schema.fields
                  if item.name == emb_label]
    if len(model_name) == 0:
        raise MilvusFieldDescriptionAbsentError(
            message=f"Field `{emb_label}` doesn't have description")
    model_name = model_name[0].description
    results = search_similar_vector(
        collection_name=collection_name,
        field_name=emb_label,
        data=emb,
        output_fields=[cluster_label],
        limit=1
    )
    if len(results) > 0:
        distance = results[0]['distance']
        cluster_id = results[0]['values'][cluster_label]
        if distance < VECTOR_SIM_THRESHOLDS[model_name]:
            return cluster_id


def get_increment_cluster_id(collection_name, cluster_label):
    results = query_milvus_data(collection_name,
                                [cluster_label],
                                f"{cluster_label} != -999")
    results = pd.DataFrame(results)
    if len(results) > 0:
        max_cluster_value = results[cluster_label].max()
    else:
        max_cluster_value = 0
    return max_cluster_value + 1
