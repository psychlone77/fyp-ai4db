# max_connections

## Category

Connection

## Description

Specifies how many concurrent client connections are allowed.

## Default Value

100

## Recommended Value

Use the lowest number that fits your workload. Use PgBouncer for scaling.

## When to Change

* When running applications with moderate concurrency.
* When your workload cannot be pooled.

## Risks / Warnings

* PostgreSQL uses one OS process per connection → high values can crash the server.
* Use connection pooling instead of increasing too much.

## Example

```
max_connections = 200
```
