# autovacuum

## Category

Maintenance / Bloat Control

## Description

Automatically vacuums tables to remove dead tuples and maintain statistics.

## Default Value

on

## Recommended Value

Always **on**. Tune thresholds, not the feature.

## When to Change

Never disable.

## Risks / Warnings

⚠ Disabling causes:

* Table bloat
* Slower queries
* Stale statistics
* Long-term database performance issues

## Example

```
autovacuum = on
```
