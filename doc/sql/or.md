```shell
# Inject documents into the index "my-index-test1"
curl -s -X POST "localhost:9200/my-index-test1/_doc?pretty" -H 'Content-Type: application/json' -d' { "v1": "10", "v2": 1 }'
curl -s -X POST "localhost:9200/my-index-test1/_doc?pretty" -H 'Content-Type: application/json' -d' { "v1": "10", "v2": 2 }'
curl -s -X POST "localhost:9200/my-index-test1/_doc?pretty" -H 'Content-Type: application/json' -d' { "v1": "10", "v2": 3 }'
curl -s -X POST "localhost:9200/my-index-test1/_doc?pretty" -H 'Content-Type: application/json' -d' { "v1": "20", "v2": 1 }'
curl -s -X POST "localhost:9200/my-index-test1/_doc?pretty" -H 'Content-Type: application/json' -d' { "v1": "20", "v2": 2 }'
curl -s -X POST "localhost:9200/my-index-test1/_doc?pretty" -H 'Content-Type: application/json' -d' { "v1": "20", "v2": 3 }'
# Review the content of the index
curl -s -X POST "localhost:9200/my-index-test1/_search?pretty" -H 'Content-Type: application/json' -d' {"query": {"match_all": {}}}' | jq '.hits.hits[]._source'
# Perform queries
curl -s -X POST "localhost:9200/my-index-test1/_search?pretty" -H 'Content-Type: application/json' -d'
{
    "query": {
        "bool": {
            "should": [
                { "term": {"v1": "10"} },
                { "term": {"v2": "1"} }
            ]
        }
    }
}' | jq '.hits.hits[]._source'
```