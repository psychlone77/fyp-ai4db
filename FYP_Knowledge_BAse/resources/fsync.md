# fsync

## Category

Safety / Durability

## Description

Ensures data is physically flushed to disk for durability.

## Default Value

on

## Recommended Value

Always **on**.

## When to Change

Never — only in benchmarking environments.

## Risks / Warnings

⚠ Turning off can cause **total data corruption** after a crash.

## Example

```
fsync = on
```
