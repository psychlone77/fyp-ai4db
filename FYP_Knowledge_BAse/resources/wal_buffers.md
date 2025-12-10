# wal_buffers

## Category

WAL

## Description

Memory for buffering WAL (Write-Ahead Log) writes.

## Default Value

-1 (auto: ~3% of shared_buffers, max 16MB)

## Recommended Value

16MB–32MB for high write loads.

## When to Change

* High concurrency systems
* Heavy write applications

## Risks / Warnings

None.

## Example

```
wal_buffers = 32MB
```
