# listen_addresses

## Category

Connection

## Description

Controls which IP addresses the PostgreSQL server listens on for incoming connections.

## Default Value

`localhost`

## Recommended Value

`'*'` when remote clients must connect (ensure pg_hba.conf is properly configured).

## When to Change

* When enabling remote connections.
* When hosting multi-application environments.

## Risks / Warnings

* Exposing PostgreSQL publicly without firewall rules is dangerous.
* Must update `pg_hba.conf` for actual client authentication.

## Example

```
listen_addresses = '*'
```
