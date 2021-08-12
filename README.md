This document is a quick introduction to ElasticSearch.

It covers the basic usage from the command line, and the Python package [elasticsearch](https://elasticsearch-py.readthedocs.io/en/v7.14.0/).

> Installation for Debian: [Install Elasticsearch with Debian Package](https://www.elastic.co/guide/en/elasticsearch/reference/current/deb.html)

* [Management](doc/management.md)
* [Insert a document into ElasticSearch](doc/insert.md)
* [Delete a document](doc/delete.md)
* [Delete an index](doc/delete-index.md)
* [Select all documents from an index](doc/select-all-from-index.md)
* [Example script in Python](main.py)

How to run the script:

```shell
pipenv shell
pipenv install
python main.py
```
