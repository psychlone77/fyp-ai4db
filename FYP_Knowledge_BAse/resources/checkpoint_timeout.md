# checkpoint_timeout

## Category

WAL / Checkpoint

## Description

How often PostgreSQL performs checkpoints.

## Default Value

5 minutes

## Recommended Value

10–30 minutes

## When to Change

* Systems with frequent checkpoints
* High write volume

## Risks / Warnings

Too frequent → heavy I/O spikes.

## Example

```
checkpoint_timeout = 20min
```
