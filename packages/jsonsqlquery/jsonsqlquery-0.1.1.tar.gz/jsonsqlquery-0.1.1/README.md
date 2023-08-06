# jsonsqlquery

Query JSON using SQL.

[![CI](https://github.com/Peter554/jsonsqlquery/actions/workflows/ci.yml/badge.svg)](https://github.com/Peter554/jsonsqlquery/actions/workflows/ci.yml)

## Examples

Inline SQL query:

```
cat foo.jsonl | jsonsqlquery --query 'select name, age from data'
```

SQL query from a file:

```
cat foo.jsonl | jsonsqlquery --query-file query.sql
```

Create a SQLite database:

```
cat foo.jsonl | jsonsqlquery --create-db foo.db
```

See the `examples/` directory.

## Caveats

* Booleans are cast to integers.
* Data is assumed to fit in memory.
