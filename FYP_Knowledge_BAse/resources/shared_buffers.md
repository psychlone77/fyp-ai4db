# shared_buffers

## Category

Memory

## Description

Memory allocated for PostgreSQL to cache table and index data.

## Default Value

128MB

## Recommended Value

25–40% of total system RAM

## When to Change

* High read workloads
* Systems with plenty of RAM

## Risks / Warnings

* Too high reduces OS page cache.
* Allocated fully on startup.

## Example

```
shared_buffers = 8GB
```
