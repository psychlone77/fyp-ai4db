# PostgreSQL Parameters for OLAP Workloads

## Overview

OLAP (Online Analytical Processing) workloads are characterized by:
- Complex queries with aggregations and joins
- Large table scans
- Fewer concurrent users
- Emphasis on throughput over latency
- Heavy read operations on large datasets
- Data warehousing and reporting scenarios

---

## Memory Settings

### shared_buffers
**Recommended:** `25-40% of RAM` (e.g., 12GB for 32GB RAM)

Can be higher for read-heavy workloads since there are fewer concurrent connections competing for memory.

### effective_cache_size
**Recommended:** `75% of RAM` (e.g., 24GB for 32GB RAM)

Higher value helps the planner make better decisions for complex analytical queries.

### work_mem
**Recommended:** `256MB-2GB`

Much higher than OLTP to support complex sorts, hash joins, and aggregations. Monitor carefully to avoid OOM issues.

**Caution:** Total memory usage can be work_mem × max_connections × operations per query. Consider per-query settings for very large operations.

### maintenance_work_mem
**Recommended:** `2-4GB`

Higher values speed up CREATE INDEX, VACUUM, and other maintenance operations on large tables.

---

## Write-Ahead Log (WAL) Settings

### wal_buffers
**Recommended:** `16MB`

Default value is typically sufficient.

### checkpoint_timeout
**Recommended:** `30min-1h`

Less frequent checkpoints are acceptable since recovery time is less critical in analytical environments.

### checkpoint_completion_target
**Recommended:** `0.9`

Spreads checkpoint I/O to reduce performance impact.

### max_wal_size
**Recommended:** `8-16GB`

Allow longer checkpoint intervals to reduce overhead during bulk loads and updates.

### min_wal_size
**Recommended:** `2GB`

Reserve adequate space for WAL files.

---

## Query Planner Settings

### random_page_cost
**Recommended:** `1.1` (SSD) or `2.0` (HDD)

Lower values favor sequential scans which are common in OLAP queries.

### effective_io_concurrency
**Recommended:** `200` (SSD)

Higher concurrency for parallel I/O operations.

### default_statistics_target
**Recommended:** `500-1000`

Higher statistics provide better query plans for complex analytical queries.

### from_collapse_limit
**Recommended:** `20`

Allow more complex query optimization (default is 8).

### join_collapse_limit
**Recommended:** `20`

Allow optimizer to reorder more joins for better execution plans (default is 8).

---

## Connection and Concurrency Settings

### max_connections
**Recommended:** `50-100`

Fewer connections since analytical queries are typically executed by fewer concurrent users.

### max_parallel_workers_per_gather
**Recommended:** `4-8`

Heavy parallelism for large table scans and aggregations.

### max_parallel_workers
**Recommended:** `16`

Overall limit on parallel workers across all queries.

### max_worker_processes
**Recommended:** `16-32`

Should be at least equal to max_parallel_workers plus autovacuum workers.

### parallel_leader_participation
**Recommended:** `on`

Allow the query leader to participate in parallel operations.

---

## Parallelism Thresholds

### min_parallel_table_scan_size
**Recommended:** `8MB`

Minimum table size to consider parallel scan (default is 8MB).

### min_parallel_index_scan_size
**Recommended:** `512kB`

Minimum index size to consider parallel scan.

### parallel_tuple_cost
**Recommended:** `0.01`

Lower values encourage parallelism (default is 0.1).

### parallel_setup_cost
**Recommended:** `100`

Lower to encourage parallel query execution (default is 1000).

---

## Autovacuum Settings

### autovacuum
**Recommended:** `on`

Always keep enabled.

### autovacuum_naptime
**Recommended:** `60s`

Less aggressive schedule is acceptable for analytical workloads.

### autovacuum_vacuum_scale_factor
**Recommended:** `0.1`

Default value works well for OLAP.

### autovacuum_analyze_scale_factor
**Recommended:** `0.05`

Keep statistics relatively current for query optimization.

### autovacuum_max_workers
**Recommended:** `4-6`

More workers for large tables.

---

## Additional Recommendations

### Partitioning
- Partition large tables by date or other logical divisions
- Enables partition pruning for faster queries
- Easier maintenance and archival

### Indexes
- Create appropriate indexes but avoid over-indexing
- Consider BRIN indexes for large, naturally ordered tables
- Use partial indexes for filtered queries

### Materialized Views
- Pre-compute complex aggregations
- Refresh during off-peak hours
- Can dramatically improve query performance

### Compression
- Use TOAST compression for large text/binary columns
- Consider table compression extensions for data warehouses

### Columnar Storage
- Consider columnar storage extensions (like citus columnar) for analytical workloads
- Can provide 10-20x compression and faster scans

---

## Configuration Example

```ini
# Memory
shared_buffers = 12GB
effective_cache_size = 24GB
work_mem = 512MB
maintenance_work_mem = 4GB

# WAL
wal_buffers = 16MB
checkpoint_timeout = 30min
checkpoint_completion_target = 0.9
max_wal_size = 16GB
min_wal_size = 2GB

# Query Planner (SSD)
random_page_cost = 1.1
effective_io_concurrency = 200
default_statistics_target = 500
from_collapse_limit = 20
join_collapse_limit = 20

# Connections and Parallelism
max_connections = 100
max_parallel_workers_per_gather = 8
max_parallel_workers = 16
max_worker_processes = 32
parallel_leader_participation = on

# Parallelism Thresholds
min_parallel_table_scan_size = 8MB
min_parallel_index_scan_size = 512kB
parallel_tuple_cost = 0.01
parallel_setup_cost = 100

# Autovacuum
autovacuum = on
autovacuum_naptime = 60s
autovacuum_vacuum_scale_factor = 0.1
autovacuum_analyze_scale_factor = 0.05
autovacuum_max_workers = 6
```

---

## Performance Optimization Tips

### Query-Specific Settings
For very large operations, consider setting work_mem per query:
```sql
SET work_mem = '2GB';
SELECT ...;
RESET work_mem;
```

### Monitoring
- Use EXPLAIN ANALYZE to understand query execution
- Monitor parallel worker usage
- Track I/O patterns and buffer hit ratios
- Watch for queries that could benefit from more parallelism

### Bulk Loading
For large data loads:
- Disable indexes temporarily
- Increase maintenance_work_mem
- Adjust max_wal_size higher
- Consider unlogged tables for staging

### JIT Compilation
**Recommended:** `jit = on`

Can significantly speed up complex queries (requires PostgreSQL 11+).

```ini
jit = on
jit_above_cost = 100000
jit_inline_above_cost = 500000
jit_optimize_above_cost = 500000
```

---

## Important Notes

- **Work_mem warning** - With work_mem = 2GB and max_connections = 100, potential memory usage could be 200GB+ if all connections use maximum work_mem
- **Test thoroughly** - OLAP workloads vary significantly; test with representative queries
- **Hardware scaling** - OLAP benefits greatly from more CPU cores, RAM, and fast storage
- **Consider columnar stores** - For pure analytical workloads, consider specialized columnar databases
- **Monitor resource usage** - Watch CPU, memory, and I/O closely during optimization