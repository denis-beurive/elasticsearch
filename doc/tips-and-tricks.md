# Tips and tricks

## Get the list of all indexes

```bash
$ wget -O- -q --header='Content-Type: application/json' "localhost:9200/_cat/indices?v&s=index"
health status index            uuid                   pri rep docs.count docs.deleted store.size pri.store.size
green  open   .geoip_databases i92UTybUSSedbV6tO3bWtg   1   0         42           41     42.9mb         42.9mb
yellow open   example          nvLkjUBZQWm3F1CO7aKLaA   1   1        100            0      6.2kb          6.2kb
yellow open   my-index-test1   ET59bzrEQL2EvmwcRBsQJg   1   1         12            0       20kb           20kb
yellow open   my_documents     b2XqfYptTUCaNfOG6YCgFA   1   1          2            0      3.5kb          3.5kb
yellow open   test-index       xWlC7EtGRzSZO4zV16lZZQ   1   1         10            0      3.8kb          3.8kb
yellow open   test1            W36zKWnrQouH6NYdl8H-UQ   1   1         10            0     14.1kb         14.1kb
```

## Get the list of index "my(_|-)?.+" 

```bash
$ wget -O- -q --header='Content-Type: application/json' "localhost:9200/_cat/indices?v&s=index" | head -n 1 && wget -O- -q --header='Content-Type: application/json' "localhost:9200/_cat/indices?v&s=index" | egrep '\s+my(_|-)?.+'
health status index            uuid                   pri rep docs.count docs.deleted store.size pri.store.size
yellow open   my-index-test1   ET59bzrEQL2EvmwcRBsQJg   1   1         12            0       20kb           20kb
yellow open   my_documents     b2XqfYptTUCaNfOG6YCgFA   1   1          2            0      3.5kb          3.5kb
```

> The command prints the header line that describes the columns. A common regex is "`logstash-[0-9]{4}\.[0-9]{2}\.[0-9]{2}`" 

## Get the mapping for a given index

The mapping of the index `test-index`:

```bash
INDEX="test-index"
wget -O- -q --header='Content-Type: application/json' "localhost:9200/${INDEX}/_mapping?pretty" > mapping.json
xclip -sel clip < mapping.json
```


## Get the mapping for a given field (within a given index)


Print the mapping for a given index:

```bash
$ INDEX="test1"
$ wget -O- -q --header='Content-Type: application/json' "localhost:9200/${INDEX}/_mapping?pretty"
{
  "test1" : {
    "mappings" : {
      "properties" : {
        "details" : {
          "properties" : {
            "a" : {
              "type" : "long"
            },
            "b" : {
              "properties" : {
                "Evelyn" : {
                  "type" : "long"
                },
                "Mia" : {
                  "type" : "long"
                },
                "Oliver" : {
                  "type" : "long"
                }
              }
            },
            "c" : {
              "type" : "long"
            }
          }
        },
        "note" : {
          "type" : "text",
          "fields" : {
            "keyword" : {
              "type" : "keyword",
              "ignore_above" : 256
            }
          }
        },
        "results" : {
          "properties" : {
            "Alexander" : {
              "type" : "long"
            },
            "Amelia" : {
              "type" : "long"
            },
            "Ava" : {
              "type" : "long"
            },
            "Benjamin" : {
              "type" : "long"
            },
            "Charlotte" : {
              "type" : "long"
            },
            "Elijah" : {
              "type" : "long"
            },
            "Emma" : {
              "type" : "long"
            },
            "Evelyn" : {
              "type" : "long"
            },
            "Harper" : {
              "type" : "long"
            },
            "Henry" : {
              "type" : "long"
            },
            "Isabella" : {
              "type" : "long"
            },
            "James" : {
              "type" : "long"
            },
            "Liam" : {
              "type" : "long"
            },
            "Lucas" : {
              "type" : "long"
            },
            "Mia" : {
              "type" : "long"
            },
            "Noah" : {
              "type" : "long"
            },
            "Oliver" : {
              "type" : "long"
            },
            "Olivia" : {
              "type" : "long"
            },
            "Sophia" : {
              "type" : "long"
            },
            "William" : {
              "type" : "long"
            }
          }
        },
        "students" : {
          "type" : "text",
          "fields" : {
            "keyword" : {
              "type" : "keyword",
              "ignore_above" : 256
            }
          }
        }
      }
    }
  }
}
```

Print the mapping for the field `key1` within the index `test-index`:

```bash
$ INDEX="test1"
$ FIELD="students"
$ wget -O- -q --header='Content-Type: application/json' "localhost:9200/${INDEX}/_mapping/field/${FIELD}?pretty"
{
  "test1" : {
    "mappings" : {
      "students" : {
        "full_name" : "students",
        "mapping" : {
          "students" : {
            "type" : "text",
            "fields" : {
              "keyword" : {
                "type" : "keyword",
                "ignore_above" : 256
              }
            }
          }
        }
      }
    }
  }
}
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

## text or keyword, and what are the consequences ?

Please read [this document](https://www.elastic.co/fr/blog/strings-are-dead-long-live-strings).

When you declare a field to be a string, ElasticSearch will create 2 mappings:
* one mapping for the type "text".
* one mapping for the type "keyword".

Example:

```bash
$ INDEX="test1"
$ FIELD="students"
$ wget -O- -q --header='Content-Type: application/json' "localhost:9200/${INDEX}/_mapping/field/${FIELD}?pretty"
{
  "test1" : {
    "mappings" : {
      "students" : {
        "full_name" : "students",
        "mapping" : {
          "students" : {
            "type" : "text",
            "fields" : {
              "keyword" : {
                "type" : "keyword",
                "ignore_above" : 256
              }
            }
          }
        }
      }
    }
  }
}
```

Do you see the parameter "`ignore_above`" ?

> Strings longer than the ignore_above setting will not be indexed or stored ([source](https://www.elastic.co/guide/en/elasticsearch/reference/current/ignore-above.html)).

In:

```
"keyword" : {
  "type" : "keyword",
  "ignore_above" : 256
}
```

The value `ignore_above` applies to the type `keyword`.
This means that values longer than 256 characters are not indexed or stored **as keywords**.

> The above explanation applies to keywords.

## Is a field searchable ?

Is the field `students` within the index `test1` searchable ?

```bash
$ INDEX="test1"
$ FIELD_NAME="students"
$ wget -O- -q --header='Content-Type: application/json' "localhost:9200/${INDEX}/_field_caps?fields=${FIELD_NAME}&pretty"
{
  "indices" : [
    "test1"
  ],
  "fields" : {
    "students" : {
      "text" : {
        "type" : "text",
        "metadata_field" : false,
        "searchable" : true,
        "aggregatable" : false
      }
    }
  }
}

```


