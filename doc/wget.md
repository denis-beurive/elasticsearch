# Using wget instead of curl

Examples:

```shell
wget -O- -q --header='Content-Type: application/json' --post-data='
{
    "query": {
        "match_all": {}
    }
}
' "localhost:9200/_search?pretty&size=2000"
```

```shell
wget -O- -q --header='Content-Type: application/json' "localhost:9200/_cat/indices?v&s=index"
```
