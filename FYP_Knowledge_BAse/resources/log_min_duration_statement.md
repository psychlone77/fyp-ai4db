# log_min_duration_statement

## Category

Logging

## Description

Logs SQL statements whose execution time exceeds the given duration in milliseconds.

## Default Value

-1 (disabled)

## Recommended Value

1000 ms (1s) or lower for performance tuning.

## When to Change

* Tracking slow queries
* Performance debugging

## Risks / Warnings

* Very low values (0) generate massive logs.

## Example

```
log_min_duration_statement = 1000
```
