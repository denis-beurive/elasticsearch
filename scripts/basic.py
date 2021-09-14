"""
    Use the provide script "scripts/generate_data.py" to inject data into the index "test1".

    $ INDEX_NAME="test1"
    $ python3 scripts/generate_data.py | while IFS= read line
    do
      curl -X POST "localhost:9200/${INDEX_NAME}/_doc?pretty" -H 'Content-Type: application/json' -d "$line"
    done
"""
from typing import List, Dict, NewType, Optional, Tuple
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
            'key2': 2 * i
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


FieldName = NewType('FieldName', str)


def get_all_fields_from_index(es: Elasticsearch, index_name: str) -> List[List[str]]:
    """
    Return the list of all fully qualified field names within a given index.
    :param es: the ElasticSearch handler.
    :param index_name: the ElasticSearch index to use.
    :return: a list of fully qualified field names.
             Each (fully qualified) field name is represented by a list of "path elements".
             Ex: the field name "a.b.c" is represented by the list ['a', 'b', 'b'].
    """

    def walk_properties(mapping_data: dict) -> Dict[FieldName, dict]:
        """
        Filter data from the index mapping.

        This function implements the Depth-first search tree traversal algorithm.

        :param mapping_data: the index mapping.
        :return: a new tree that contains only relevant data.
        """
        fields: Dict[FieldName, dict] = {}
        field: str
        spec: dict
        for field, spec in mapping_data.items():
            if "properties" in spec:
                fields[FieldName(field)] = {
                    'leaf': False,
                    'next': walk_properties(spec["properties"])
                }
                continue
            fields[FieldName(field)] = {
                'leaf': True,
                'next': None
            }
        return fields

    def flatter(mapping_data: dict) -> List[List[str]]:
        """
        Extract fully qualified field names from the data extracted from the index mapping.
        :param mapping_data: filtered data from the mapping data.
        :return: a list of fully qualified field names.
                 Each (fully qualified) field name is represented by a list of "path elements".
                 Ex: the field name "a.b.c" is represented by the list ['a', 'b', 'b'].
        """

        def walk_fields(in_fields: Dict[FieldName, dict],
                        in_path: List[str],
                        in_precedent: Optional[Tuple[dict, FieldName]] = None) -> bool:
            keys = list(in_fields.keys())
            if len(keys) == 0:
                if in_precedent is not None:
                    # Please note: `del dict` is not a valid expression.
                    #              `del dict[key]` is a valid expression.
                    p_dict: dict = in_precedent[0]
                    p_key: str = in_precedent[1]
                    del p_dict[p_key]
                return False

            in_field = keys[0]
            in_path.append(in_field)
            if in_fields[in_field]['leaf']:
                del in_fields[in_field]
                return True

            next_tree: Optional[dict] = in_fields[in_field]['next']
            next_tree = {} if next_tree is None else next_tree
            return walk_fields(next_tree, in_path, (in_fields, in_field))

        result: List[List[str]] = []
        while True:
            path: List[str] = []
            keep = walk_fields(mapping_data, path)
            if len(path) == 0:
                break
            if keep:
                result.append(path.copy())
        return result

    mapping: dict = es.indices.get_mapping(index=index_name)
    pprint(mapping)
    properties: dict = mapping[index_name]['mappings']['properties']
    pprint(properties)
    all_fields_dict = walk_properties(properties)
    return flatter(all_fields_dict)


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

    index_fields = get_all_fields_from_index(es, 'test1')
    print("=" * 60)
    print("\n".join(['.'.join(p) for p in index_fields]))
    print("=" * 60)

main()
