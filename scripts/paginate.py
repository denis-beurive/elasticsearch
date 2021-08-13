# This script illustrates the pagination.
#
# See:
#      https://www.elastic.co/guide/en/elasticsearch/reference/6.8/search-request-from-size.html
#      https://www.elastic.co/guide/en/elasticsearch/reference/6.8/search-request-scroll.html
#      https://www.elastic.co/guide/en/elasticsearch/reference/6.8/search-request-search-after.html

from typing import List
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


def select_all_paginate_basic(es: Elasticsearch, index_name: str, custom_query: dict) -> List[dict]:
    """
    Select all records from the database using the basic pagination technique.

    See: https://www.elastic.co/guide/en/elasticsearch/reference/6.8/search-request-from-size.html

    :param es: the ElasticSearch handler.
    :param index_name: the name of the index.
    :param custom_query: the custom query.
    :return: the list of all records.
    """
    query = {
        "query": {
            **custom_query
        }
    }
    from_val: int = 0
    size_val: int = 10
    result: List[dict] = []

    while True:
        res: dict = es.search(index=index_name, body=query, from_=from_val, size=size_val)
        from_val += size_val
        if res['_shards']['successful'] < 1:
            raise Exception("An error occurred while searching for a document (using a custom query)!")
        if not len(res['hits']['hits']):
            break
        result.extend(f['_source'] for f in res['hits']['hits'])

    return result


def select_all_paginate_scroll(es: Elasticsearch, index_name: str, custom_query: dict) -> List[dict]:
    """
    Select all records from the database using the scrolling pagination technique.

    See: https://www.elastic.co/guide/en/elasticsearch/reference/6.8/search-request-scroll.html

    :param es: the ElasticSearch handler.
    :param index_name: the name of the index.
    :param custom_query: the custom query.
    :return: the list of all records.
    """
    query = {
        "query": {
            **custom_query
        }
    }
    result: List[dict] = []

    # Perform a first request in order to get the "scroll" ID.
    res: dict = es.search(index=index_name, body=query, size=10, scroll='1m')
    if res['_shards']['successful'] < 1:
        raise Exception("An error occurred while searching for a document (using a custom query)!")
    if not len(res['hits']['hits']):
        return []
    result.extend(f['_source'] for f in res['hits']['hits'])
    scroll_id = res['_scroll_id']

    while True:
        res: dict = es.scroll(scroll_id=scroll_id, scroll='1m')
        if res['_shards']['successful'] < 1:
            raise Exception("An error occurred while searching for a document (using a custom query)!")
        if not len(res['hits']['hits']):
            break
        result.extend(f['_source'] for f in res['hits']['hits'])
        scroll_id = res['_scroll_id']

    return result


def select_all_paginate_search_after(es: Elasticsearch, index_name: str) -> List[dict]:
    """
    Select all records from the database using the "search after" pagination technique.

    See: https://www.elastic.co/guide/en/elasticsearch/reference/6.8/search-request-search-after.html

    :param es: the ElasticSearch handler.
    :param index_name: the name of the index.
    :return: the list of all records.
    """
    custom_query: dict = {
        "query": {
            "range": {
                "key1": {"gte": 0}
            },
        },
        "sort": [
            {"_id": "asc"}
        ]
    }
    result: List[dict] = []
    res: dict = es.search(index=index_name, body=custom_query, size=10)
    if res['_shards']['successful'] < 1:
        raise Exception("An error occurred while searching for a document (using a custom query)!")
    if not len(res['hits']['hits']):
        return []
    result.extend(f['_source'] for f in res['hits']['hits'])

    last_id = res['hits']['hits'][-1]['_id']
    while True:
        custom_query['search_after'] = [last_id]
        res: dict = es.search(index=index_name, body=custom_query, size=10)
        if res['_shards']['successful'] < 1:
            raise Exception("An error occurred while searching for a document (using a custom query)!")
        if not len(res['hits']['hits']):
            break
        result.extend(f['_source'] for f in res['hits']['hits'])
        last_id = res['hits']['hits'][-1]['_id']
    return result


def main() -> None:
    count: int = 100
    index: str = 'example'

    # -------------------------------------------------------------------------
    # Inject document
    # -------------------------------------------------------------------------
    es: Elasticsearch = Elasticsearch([{'host': ES_HOST, 'port': ES_PORT}])
    inject(es, index, count)

    # -------------------------------------------------------------------------
    # Select page per page, using the basic technique
    # -------------------------------------------------------------------------
    custom_query: dict = {
        "range": {
            "key1": {"gte": 0}
        }
    }
    res = select_all_paginate_basic(es, index, custom_query)
    pprint(res)

    # -------------------------------------------------------------------------
    # Select page per page, using the scroll technique
    # -------------------------------------------------------------------------
    custom_query: dict = {
        "range": {
            "key1": {"gte": 0}
        }
    }
    res = select_all_paginate_scroll(es, index, custom_query)
    pprint(res)

    # -------------------------------------------------------------------------
    # Select page per page, using the search after technique
    # -------------------------------------------------------------------------
    select_all_paginate_search_after(es, index)
    pprint(res)

main()
