# idle_in_transaction_session_timeout

## Category

Session / Safety

## Description

Terminates sessions that remain idle inside a transaction for too long.

## Default Value

0 (disabled)

## Recommended Value

30 minutes (1800000 ms)

## When to Change

* When preventing long-held locks.
* When avoiding vacuum blockages.
* When protecting from badly coded applications.

## Risks / Warnings

* Can terminate legitimate long-running transactions if set too low.

## Example

```
idle_in_transaction_session_timeout = 1800000
```
