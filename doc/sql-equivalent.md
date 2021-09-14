# SQL equivalent

## WHERE cond1 AND cond2 AND...

```
{
    "query": {
        "bool": {
            "must": [
                { <cond1> },
                { <cond2> },
                ...
            ]
        }
    }
}
```

Example: [click here](sql/and.md)

## WHERE cond1 OR cond2 OR...

```
{
    "query": {
        "bool": {
            "should": [
                { <cond1> },
                { <cond2> },
                ...
            ]
        }
    }
}
```

Example: [click here](sql/or.md)

## WHERE (cond1 OR cond2 OR...) AND cond3 AND...

```
{
    "query": {
        "bool": {
            "should": [
                { <cond1> },
                { <cond2> },
                ...
            ]
            "must": [
                { <cond3> },
                { <cond4> },
                ...
            ]
        }
    }
}
```

Example: [click here](sql/and_or.md)

## ... ORDER BY value

```
{
    "query": {...},
    "sort" : [{ "value": ("asc"|"desc")}]
}
```

Example: [click here](sql/sort.md)

## ... GROUP BY value

```
{
    "query": {...},
    "aggs" : { 
        "buckets": {
            "terms": { "field": "value" }       
        } 
    }
}
```

Selected documents are ordered based on the given condition.

Example: [click here](sql/aggs.md)

> **Note**: It is possible to order the contents of the buckets.
> See [this document](https://www.elastic.co/guide/en/elasticsearch/reference/current/search-aggregations-bucket-terms-aggregation.html#search-aggregations-bucket-terms-aggregation-order).

## SELECT count(*) FROM ...

```
wget -O- -q --header='Content-Type: application/json' --post-data='{
        "query": {...}
    }
}' 'localhost:9200/test1/_count?pretty'
```


