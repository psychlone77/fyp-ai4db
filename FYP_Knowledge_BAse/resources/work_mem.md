# work_mem

## Category

Memory

## Description

Memory used for per-operation sorts, hashes, and joins.

## Default Value

4MB

## Recommended Value

10–50MB depending on workload.

## When to Change

* Large sort/aggregation workloads.
* Reporting/analytics systems.

## Risks / Warnings

⚠ Total usage:

```
sessions × sort_ops × work_mem
```

Too high causes OOM.

## Example

```
work_mem = 32MB
```
