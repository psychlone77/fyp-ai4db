# max_wal_size

## Category

WAL

## Description

Maximum WAL volume allowed before a checkpoint is forced.

## Default Value

1GB

## Recommended Value

4–16GB depending on write workload.

## When to Change

* When WAL-driven checkpoints appear in logs.

## Risks / Warnings

Larger WAL means longer crash recovery time.

## Example

```
max_wal_size = 8GB
```
