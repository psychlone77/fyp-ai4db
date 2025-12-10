# effective_cache_size

## Category

Planner

## Description

Planner hint for how much memory is available for caching data across PostgreSQL + OS.

## Default Value

4GB (varies by system)

## Recommended Value

50–70% of total system RAM

## When to Change

* Always adjust to real system memory.

## Risks / Warnings

Too low → planner underestimates caching → avoids index scans.

## Example

```
effective_cache_size = 24GB
```
