import json
from typing import List, Dict, Any
from pprint import pprint
from elasticsearch import Elasticsearch

ES_HOST: str = 'localhost'
ES_PORT: int = 9200


def inject(es: Elasticsearch, index_name: str, count: int) -> None:
    """
    Inject a given number of documents in a given index.
    :param es: the ElasticSearch handler.
    :param index_name: the name of the index.
    :param count: the number of document to inject.
    """
    for i in range(count):
        doc: dict = {
            'key1': i,
            'key2': 2*i
        }
        res: dict = es.index(index=index_name, id=i, body=doc)

        # Example value:
        #
        #   {'_id': '9',
        #    '_index': 'example',
        #    '_primary_term': 1,
        #    '_seq_no': 9,
        #    '_shards': {'failed': 0, 'successful': 1, 'total': 2},
        #    '_type': '_doc',
        #    '_version': 1,
        #    'result': 'created'}
        #
        # For testing the status, see:
        # https://www.elastic.co/guide/en/elasticsearch/reference/current/docs-index_.html#docs-index-api-response-body

        if res['_shards']['successful'] < 1:
            raise Exception("An error occurred while indexing a document!")


def get_by_id(es: Elasticsearch, index_name: str, doc_id: str) -> dict:
    """
    Get a document using its unique ID as identifier.
    :param es: the ElasticSearch handler.
    :param index_name: the name of the index.
    :param doc_id: the unique ID of the document.
    :return: the document
    """
    query = {
        "query": {
            "match": {
                "_id": doc_id
            }
        }
    }
    res: dict = es.search(index=index_name, body=query, size=10)

    # Example value:
    #
    #   {'_shards': {'failed': 0, 'skipped': 0, 'successful': 1, 'total': 1},
    #    'hits': {'hits': [{'_id': '9',
    #                       '_index': 'example',
    #                       '_score': 1.0,
    #                       '_source': {'key1': 9, 'key2': 18},
    #                       '_type': '_doc'}],
    #             'max_score': 1.0,
    #             'total': {'relation': 'eq', 'value': 1}},
    #    'timed_out': False,
    #    'took': 1}
    #
    # For testing the status, see:
    # https://www.elastic.co/guide/en/elasticsearch/reference/current/docs-index_.html#docs-index-api-response-body

    if res['_shards']['successful'] < 1:
        raise Exception("An error occurred while searching for a document (using the document ID)!")
    return res['hits']['hits'][0]['_source']


def get_by_custom_query(es: Elasticsearch, index_name: str, custom_query: dict) -> List[dict]:
    """
    Select document using a custom provided query.
    :param es: the ElasticSearch handler.
    :param index_name: the name of the index.
    :param custom_query: the custom query.
    :return: the list of selected documents.
    """
    query = {
        "query": {
            **custom_query
        }
    }
    res: dict = es.search(index=index_name, body=query, size=10)
    if res['_shards']['successful'] < 1:
        raise Exception("An error occurred while searching for a document (using a custom query)!")
    return [r['_source'] for r in res['hits']['hits']]


def main() -> None:
    count: int = 10
    index: str = 'example'

    # -------------------------------------------------------------------------
    # Inject document
    # -------------------------------------------------------------------------
    es: Elasticsearch = Elasticsearch([{'host': ES_HOST, 'port': ES_PORT}])
    inject(es, index, count)

    # -------------------------------------------------------------------------
    # Select documents by unique ID
    # -------------------------------------------------------------------------
    for i in range(count):
        res = get_by_id(es, index, str(i))
        pprint(res)

    # -------------------------------------------------------------------------
    # Select document using custom requests
    # -------------------------------------------------------------------------
    custom_query: dict = {
        "match": {
            "key1": "2"
        }
    }
    res = get_by_custom_query(es, index, custom_query)
    pprint(res)

    # Select documents which value for "key1" is between 0 (included) and 5 (included).
    # See: https://www.elastic.co/guide/en/elasticsearch/reference/current/query-dsl-range-query.html#query-dsl-range-query
    custom_query: dict = {
        "range": {
            "key1": {"gte": 0, "lte": 5, "boost": 2.0}
        }
    }
    res = get_by_custom_query(es, index, custom_query)
    pprint(res)

    # Select documents which value for "key1" is between 0 (included) and 5 (included) OR greater than or equal to 8.
    # See: https://www.elastic.co/guide/en/elasticsearch/reference/6.8/query-dsl-bool-query.html
    custom_query: dict = {
        "bool": {
            "should": [
                {"range": {"key1": {"gte": 0, "lte": 5}}},
                {"range": {"key1": {"gte": 8}}}
            ]
        }
    }
    res = get_by_custom_query(es, index, custom_query)
    pprint(res)

    # Same request as the previous one, but we add a condition: the value of "key2" must be greater than 10.
    # See: https://www.elastic.co/guide/en/elasticsearch/reference/6.8/query-dsl-bool-query.html
    custom_query: dict = {
        "bool": {
            "must": {
                "range": {"key2": {"gte": 10}},
            },
            "should": [
                {"range": {"key1": {"gte": 0, "lte": 5}}},
                {"range": {"key1": {"gte": 8}}}
            ]
        }
    }
    res = get_by_custom_query(es, index, custom_query)
    pprint(res)


main()
