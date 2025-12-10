# PostgreSQL Parameters for OLTP Workloads

## Overview

OLTP (Online Transaction Processing) workloads are characterized by:
- High volumes of short transactions
- Frequent reads and writes
- Many concurrent connections
- Emphasis on low latency and response time
- Row-level operations (INSERT, UPDATE, DELETE, SELECT on specific rows)

---

## Memory Settings

### shared_buffers
**Recommended:** `25% of RAM` (e.g., 8GB for 32GB RAM)

Lower than OLAP to leave room for operating system cache, which is beneficial for high-concurrency workloads.

### effective_cache_size
**Recommended:** `50-75% of RAM` (e.g., 20GB for 32GB RAM)

Helps the query planner understand how much memory is available for caching data.

### work_mem
**Recommended:** `32-64MB`

Keep relatively low due to high concurrent connections. Each sort/hash operation can use up to this amount, and with many connections, total memory usage = work_mem × operations × connections.

### maintenance_work_mem
**Recommended:** `512MB-1GB`

Used for maintenance operations like VACUUM, CREATE INDEX, and ALTER TABLE.

---

## Write-Ahead Log (WAL) Settings

### wal_buffers
**Recommended:** `16MB`

Default value is usually sufficient for OLTP workloads.

### checkpoint_timeout
**Recommended:** `15min`

More frequent checkpoints ensure better data safety and faster recovery times.

### checkpoint_completion_target
**Recommended:** `0.9`

Spreads checkpoint I/O over 90% of the checkpoint interval to reduce I/O spikes.

### max_wal_size
**Recommended:** `2-4GB`

Controls checkpoint frequency based on WAL size.

### min_wal_size
**Recommended:** `1GB`

Minimum size to reserve for WAL files.

---

## Query Planner Settings

### random_page_cost
**Recommended:** `1.1-1.5` (SSD) or `4.0` (HDD)

Lower values for SSDs reflect their better random access performance.

### effective_io_concurrency
**Recommended:** `200` (SSD) or `2` (HDD)

Number of concurrent disk I/O operations PostgreSQL expects to be supported.

### default_statistics_target
**Recommended:** `100`

Default value provides good balance for OLTP workloads.

---

## Connection and Concurrency Settings

### max_connections
**Recommended:** `200-500`

Based on application requirements. Consider using connection pooling (PgBouncer) for higher connection counts.

### max_parallel_workers_per_gather
**Recommended:** `0-2`

Limited parallelism for OLTP since queries are typically simple and short.

### max_worker_processes
**Recommended:** `8`

Total number of background worker processes.

---

## Autovacuum Settings (Critical for OLTP)

### autovacuum
**Recommended:** `on`

Must be enabled to prevent transaction ID wraparound and maintain performance.

### autovacuum_naptime
**Recommended:** `10s`

More aggressive naptime to keep up with high transaction rates.

### autovacuum_vacuum_scale_factor
**Recommended:** `0.05`

Triggers vacuum when 5% of table rows have been modified (more aggressive than default 0.2).

### autovacuum_analyze_scale_factor
**Recommended:** `0.025`

Triggers analyze more frequently to keep statistics current.

---

## Additional Recommendations

### Monitoring
- Monitor connection usage and query performance regularly
- Watch for bloat in high-update tables
- Track checkpoint and vacuum activity

### Indexes
- Create appropriate indexes for frequent queries
- Use partial indexes where applicable
- Monitor index usage and remove unused indexes

### Connection Pooling
- Implement PgBouncer or pgpool-II for connection management
- Reduces overhead of connection creation/destruction

### Storage
- Use SSDs for best OLTP performance
- Separate WAL files to different disks if using HDDs

---

## Configuration Example

```ini
# Memory
shared_buffers = 8GB
effective_cache_size = 20GB
work_mem = 64MB
maintenance_work_mem = 1GB

# WAL
wal_buffers = 16MB
checkpoint_timeout = 15min
checkpoint_completion_target = 0.9
max_wal_size = 4GB
min_wal_size = 1GB

# Query Planner (SSD)
random_page_cost = 1.1
effective_io_concurrency = 200
default_statistics_target = 100

# Connections
max_connections = 300
max_parallel_workers_per_gather = 2
max_worker_processes = 8

# Autovacuum
autovacuum = on
autovacuum_naptime = 10s
autovacuum_vacuum_scale_factor = 0.05
autovacuum_analyze_scale_factor = 0.025
```

---

## Important Notes

- **Test thoroughly** - Always test configuration changes in a non-production environment first
- **Monitor performance** - Use pg_stat_statements and system monitoring tools
- **Incremental changes** - Change one parameter at a time and measure impact
- **Hardware matters** - Adjust based on your specific hardware (RAM, CPU, storage type)
- **Application specific** - Fine-tune based on your actual workload patterns