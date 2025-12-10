# random_page_cost

## Category

Planner

## Description

Planner estimate for cost of random disk I/O.

## Default Value

4.0 (designed for HDD)

## Recommended Value

1.1 – 2.0 for SSD systems.

## When to Change

* When using SSDs
* When planner prefers sequential scans unnecessarily

## Risks / Warnings

Setting too low may overuse indexes.

## Example

```
random_page_cost = 1.3
```
