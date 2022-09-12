# Blog REST API Service

[![Test](https://github.com/tobias2910/blog-restapi-service/actions/workflows/conduct_tests.yml/badge.svg)](https://github.com/tobias2910/blog-restapi-service/actions/workflows/conduct_tests.yml)
![Documentation](https://img.shields.io/badge/license-MIT-brightgreen)
---

This is a REST API build using the FAST API framework. It has the purpose to to provide the capabilities to manage
the articles, posts and skills in the database.

---

## Development

Please follow the following steps to start developing on this project:

* Clone this repository
* You need to to have the following requirements installed:
  * [Poetry](https://python-poetry.org/)
  * Python 3.9+
* Create a new virtual environment and install the dependencies using the following command:

```sh
poetry install
```

## Testing

To run the test, run the following command

```sh
pytest
```

---

## Documentation

The documentation is automatically generated using MKDocs in combination with several plugins.
Therefor, you are not required to add new pages in the mkdocs.yml file. You can find the documentation [here](http://tobias2910.github.io/blog-restapi-service/).

If you want to access the documentation locally use the following command:

```sh
poetry mkdocs serve
```
