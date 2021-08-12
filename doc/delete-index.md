# Delete an index

The general command is ([source](https://www.elastic.co/guide/en/elasticsearch/reference/current/indices-delete-index.html#indices-delete-index)):

```shell
INDEX_NAME="my_documents"
$ curl -X DELETE "localhost:9200/${INDEX_NAME}?pretty"
{
  "acknowledged" : true
}
```

> You can then see that an index has been deleted: `curl http://localhost:9200/_aliases?pretty=true`
