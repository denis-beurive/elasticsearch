# Select all documents from an index

```shell
INDEX_NAME="my_documents"
$ curl -X GET "localhost:9200/${INDEX_NAME}/_search?pretty" -H 'Content-Type: application/json' -d'
{
    "query": {
        "match_all": {}
    }
}
'
{
  "took" : 361,
  "timed_out" : false,
  "_shards" : {
    "total" : 1,
    "successful" : 1,
    "skipped" : 0,
    "failed" : 0
  },
  "hits" : {
    "total" : {
      "value" : 2,
      "relation" : "eq"
    },
    "max_score" : 1.0,
    "hits" : [
      {
        "_index" : "my_documents",
        "_type" : "_doc",
        "_id" : "lLRgOXsBgWOABKkzVnWZ",
        "_score" : 1.0,
        "_source" : {
          "a" : 1,
          "b" : 2
        }
      },
      {
        "_index" : "my_documents",
        "_type" : "_doc",
        "_id" : "lbRgOXsBgWOABKkzj3Wu",
        "_score" : 1.0,
        "_source" : {
          "a" : 1,
          "b" : 2
        }
      }
    ]
  }
}
```

Please note that you can see that the document contents are located under the keys "`.hits.hits[]._source`":

```shell
$ curl -s -X GET "localhost:9200/${INDEX_NAME}/_search?pretty" -H 'Content-Type: application/json' -d'
{
    "query": {
        "match_all": {}
    }
}
' | jq '.hits.hits[]._source'
{
  "a": 1,
  "b": 2
}
{
  "a": 1,
  "b": 2
}
```
