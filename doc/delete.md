# Delete a document

Example: we insert a document, and then we delete it: 

```shell
$ INDEX_NAME="my_documents"
$ curl -X POST "localhost:9200/${INDEX_NAME}/_doc?pretty" -H 'Content-Type: application/json' -d'
{
    "a": 1,
    "b": 2
}
'
{
  "_index" : "my_documents",
  "_type" : "_doc",
  "_id" : "k7RYOXsBgWOABKkzUnW3",
  ...
}
```

> You can see that the unique ID of the injected document is: `k7RYOXsBgWOABKkzUnW3` (key `_id`).

```shell
$ ID="k7RYOXsBgWOABKkzUnW3"
$ INDEX_NAME="my_documents"
$ curl -X DELETE "localhost:9200/${INDEX_NAME}/_doc/${ID}?pretty"
{
  "_index" : "my_documents",
  "_type" : "_doc",
  "_id" : "k7RYOXsBgWOABKkzUnW3",
  "_version" : 2,
  "result" : "deleted",
  ...
}
```
