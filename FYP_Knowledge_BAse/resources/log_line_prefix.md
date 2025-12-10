# log_line_prefix

## Category

Logging

## Description

Add metadata to each log line for debugging.

## Default Value

Empty

## Recommended Value

```
%t %u@%d %r [%p]
```

## When to Change

* When needing detailed logs.
* Troubleshooting client connections.

## Risks / Warnings

None.

## Example

```
log_line_prefix = '%t %u@%d %r [%p]'
```
