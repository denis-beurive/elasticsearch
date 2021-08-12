# ElasticSearch management (Ubuntu)

## Start / Stop

**Start**:

```shell
$ sudo systemctl start elasticsearch.service
$ curl -XGET localhost:9200/
{
  "name" : "labo",
  "cluster_name" : "elasticsearch",
  "cluster_uuid" : "Bys2fCRMRqiHZCN3vTrahg",
  "version" : {
    "number" : "7.14.0",
    "build_flavor" : "default",
    "build_type" : "deb",
    "build_hash" : "dd5a0a2acaa2045ff9624f3729fc8a6f40835aa1",
    "build_date" : "2021-07-29T20:49:32.864135063Z",
    "build_snapshot" : false,
    "lucene_version" : "8.9.0",
    "minimum_wire_compatibility_version" : "6.8.0",
    "minimum_index_compatibility_version" : "6.0.0-beta1"
  },
  "tagline" : "You Know, for Search"
}
```

**Stop**:

```shell
sudo systemctl stop elasticsearch.service
```

## Show indexes

> An index can be thought of as an optimized collection of documents and each document is a collection of fields, 
> which are the key-value pairs that contain your data. By default, Elasticsearch indexes all data in every field 
> and each indexed field has a dedicated, optimized data structure 
> ([source](https://www.elastic.co/guide/en/elasticsearch/reference/current/documents-indices.html)).

```shell
$ curl http://localhost:9200/_aliases?pretty=true
{ }
```

## Show shards

> The shard is the unit at which Elasticsearch distributes data around the cluster. The speed at which Elasticsearch 
> can move shards around when rebalancing data, e.g. following a failure, will depend on the size and number of 
> shards as well as network and disk performance.
> ([source](https://www.elastic.co/blog/how-many-shards-should-i-have-in-my-elasticsearch-cluster)).

```shell
$ curl http://localhost:9200/_cat/shards
.geoip_databases 0 p STARTED 42 44mb 127.0.0.1 labo
```
