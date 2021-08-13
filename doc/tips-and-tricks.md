# Tips and tricks

## Get the list of all indexes

```shell
wget -O- -q --header='Content-Type: application/json' "elasticsearch:9200/_cat/indices?v&s=index"
```

## Use "jq" to print only parts of the results

Print only one field:

```shell
wget -O- -q --header='Content-Type: application/json' --post-data='
{
    "query": {
        "terms": {
          "_index": [".kibana*"] 
        }
    }
}
' "localhost:9200/_search?pretty&size=10000" | jq '.hits.hits[]._index' | sort | uniq
".kibana-6"
".kibana_7"
".kibana_task_manager"
```

Print multiple fields, and format the result as CSV records:

```shell
wget -O- -q --header='Content-Type: application/json' --post-data='
{
    "query": {
        "match_all": {}    }
}
' "localhost:9200/_search?pretty&size=2000" | jq '.hits.hits[] | [._index, ._id] | @csv'
```

Print only the result payloads:

```shell
wget -O- -q --header='Content-Type: application/json' --post-data='
{
    "query": {
        "match_all": {}    }
}
' "localhost:9200/_search?pretty&size=2000" | jq '.hits.hits[]._source'
```
