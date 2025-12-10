# maintenance_work_mem

## Category

Memory

## Description

Memory used for maintenance operations like VACUUM, CREATE INDEX, ALTER TABLE.

## Default Value

64MB

## Recommended Value

5% of system RAM

## When to Change

* During bulk indexing
* Heavy vacuum workloads

## Risks / Warnings

* Autovacuum can use up to 3× this value.

## Example

```
maintenance_work_mem = 2GB
```
