# Insert a document into ElasticSearch

The general command is ([source](https://www.elastic.co/guide/en/elasticsearch/reference/current/getting-started.html#add-single-document)):

```shell
$ INDEX_NAME="my_documents"
$ curl -X POST "localhost:9200/${INDEX_NAME}/_doc?pretty" -H 'Content-Type: application/json' -d'
{
  ...
}
'
```

> You can then see that an index has been created: `curl http://localhost:9200/_aliases?pretty=true`
> 
> The description of the response is given [here](https://www.elastic.co/guide/en/elasticsearch/reference/current/docs-index_.html#docs-index-api-response-body)


Example:

```bash
$ INDEX_NAME="test1"
$ python3 scripts/generate_data.py | while IFS= read line
do
  curl -X POST "localhost:9200/${INDEX_NAME}/_doc?pretty" -H 'Content-Type: application/json' -d "$line"
done
````

> You can find the script `generate_data.py` [here](scripts/generate_data.py).






