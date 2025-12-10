# CRUNCHYDATA

**Source:** https://www.crunchydata.com/blog/postgres-tuning-and-performance-for-analytics-data
**Generated:** 2025-12-07T10:56:57.499213

---

[](https://www.crunchydata.com/)
Products
Cloud
Solutions
Developer?
[Customers](https://www.crunchydata.com/customers)[Pricing](https://www.crunchydata.com/pricing)
[Blog](https://www.crunchydata.com/blog)[Contact](https://www.crunchydata.com/contact)
Login
[Access Portal](https://access.crunchydata.com)
[Crunchy Bridge](https://www.crunchybridge.com/login)
[Create Account](https://www.crunchybridge.com/register)
Open menu
![Avatar for Karen Jex](https://www.crunchydata.com/build/_assets/karen-jex.png-FZT5KN5U.webp)
Karen Jex
Jan 9, 2025·19 min read
[More by this author](https://www.crunchydata.com/blog/author/karen-jex)
## Latest Articles
  * [Postgres Scan Types in EXPLAIN Plans](https://www.crunchydata.com/blog/postgres-scan-types-in-explain-plans)
  * [PostGIS Performance: Data Sampling](https://www.crunchydata.com/blog/postgis-performance-data-sampling)
  * [PostGIS Performance: Intersection Predicates and Overlays](https://www.crunchydata.com/blog/postgis-performance-intersection-predicates-and-overlays)
  * [Postgres Internals Hiding in Plain Sight](https://www.crunchydata.com/blog/postgres-internals-hiding-in-plain-sight)
  * [PostGIS Performance: Improve Bounding Boxes with Decompose and Subdivide](https://www.crunchydata.com/blog/postgis-performance-improve-bounding-boxes-with-decompose-and-subdivide)


[Analytics](https://www.crunchydata.com/blog/topic/analytics)
# Postgres Tuning & Performance for Analytics Data
![Avatar for Karen Jex](https://www.crunchydata.com/build/_assets/karen-jex.png-FZT5KN5U.webp)
Karen Jex
Jan 9, 2025·19 min read·[More by this author](https://www.crunchydata.com/blog/author/karen-jex)
Your database is configured for the needs of your day-to-day OLTP (online transaction processing) application workload, but what if you need to run analytics queries against your application data? How can you do that without compromising the performance of your application?
## [OLTP & OLAP activity in the same database](https://www.crunchydata.com/blog/postgres-tuning-and-performance-for-analytics-data#oltp--olap-activity-in-the-same-database)
Application data gradually builds up in your database over time, and at some point the business wants to glean insights from it by running analytics queries.
Analytics activity, sometimes called OLAP (online analytical processing), Reporting, Decision Support (DS) or Business Intelligence (BI) is activity that’s designed to answer real-world business questions. It might be something like "How successful was our last marketing campaign?" or “What's the impact on our CO2 emissions of performing this action compared to this one?"
The business often wants to get answers to these questions in real-time, querying the data where it is rather than setting up a dedicated analytics environment.
This means running analytics queries directly against your application database.
Analytics or OLAP activity typically involves much longer, more complex queries than OLTP activity, joining data from multiple tables, and working on large data sets. This means it's very resource intensive.
Where you've got this OLTP plus OLAP activity in the same database, you'll hear it called a mixed or a hybrid workload. Without careful planning and tuning, you can find yourself with analytics queries that not only take far too long to run, but also slow down your existing application. Even if you have a dedicated PostgreSQL instance for OLAP, you’ll want to tune it for analytics as the data gets bigger and the server gets busier.
Let’s look at some of the ways that you can tweak and tune your database and your code to work with this hybrid workload. The goal is to make sure you've got performant analytics queries that have minimal impact on your operational database activity.
## [Coffee shop sales data](https://www.crunchydata.com/blog/postgres-tuning-and-performance-for-analytics-data#coffee-shop-sales-data)
Since coffee and cake are some of my favourite things, I used this [Coffee Shop Sales](https://www.kaggle.com/datasets/ahmedabbas757/coffee-sales) data to populate a coffee_shop_sales table. I expanded the data until I had 26.5 million rows in the table.
```
CREATE TABLE coffee_shop_sales (
  transaction_id NUMERIC,
  transaction_date DATE,
  transaction_time TIME,
  transaction_qty NUMERIC,
  store_id NUMERIC,
  store_location TEXT,
  product_id NUMERIC,
  unit_price NUMERIC,
  product_category TEXT,
  product_type TEXT,
  product_detail TEXT,
  sales_tax_pct NUMERIC);

```

I then created an analytics query to answer the question:
_“Which store had the highest total sales for each month of the previous calendar year, taking into account only transactions with a value greater than 20?”_
```
WITH ranked_sales AS (
  SELECT
	store_id::text||': '||store_location AS store,
	DATE_TRUNC('month', transaction_date) AS month,
	SUM(unit_price*(1+sales_tax_pct/100)*transaction_qty) AS total_monthly_sales,
	RANK() OVER (PARTITION BY DATE_TRUNC('month', transaction_date)
             	ORDER BY SUM(unit_price*(1+sales_tax_pct/100)*transaction_qty) DESC) AS sales_rank
  FROM coffee_shop_sales
  WHERE date_trunc('year', transaction_date) = date_trunc('year', now()) - interval '1 year'
  AND unit_price*(1+sales_tax_pct/100)*transaction_qty>20
  GROUP BY 1, 2)
SELECT
  to_char(month, 'YYYY-MM') AS month,
  store,
  round(total_monthly_sales,2) AS total_monthly_sales
FROM ranked_sales
WHERE sales_rank = 1
ORDER BY month;

```

Here are the results of the query, which were returned in just under 3 seconds:
```
┌─────────┬────────────────────┬─────────────────────┐
│  month  │       store        │ total_monthly_sales │
├─────────┼────────────────────┼─────────────────────┤
| 2023-01 | 5: Lower Manhattan |            92228.86 |
| 2023-02 | 5: Lower Manhattan |            74252.86 |
| 2023-03 | 5: Lower Manhattan |            49454.54 |
| 2023-04 | 8: Hell's Kitchen  |            84161.92 |
| 2023-05 | 8: Hell's Kitchen  |           102180.72 |
| 2023-06 | 3: Astoria         |          1908647.57 |
| 2023-07 | 8: Hell's Kitchen  |            71506.82 |
| 2023-08 | 8: Hell's Kitchen  |            40446.00 |
| 2023-09 | 5: Lower Manhattan |            49454.54 |
| 2023-10 | 3: Astoria         |          1383157.99 |
| 2023-11 | 8: Hell's Kitchen  |           102180.72 |
| 2023-12 | 8: Hell's Kitchen  |           128999.20 |
└─────────┴────────────────────┴─────────────────────┘
(12 rows)

```
We can use EXPLAIN ANALYZE to have a look at the execution plan for the query so we can see what Postgres is doing behind the scenes. ```
EXPLAIN ANALYZE
WITH ranked_sales AS (
  SELECT
	store_id::text||': '||store_location AS store,
	DATE_TRUNC('month', transaction_date) AS month,
	SUM(unit_price*(1+sales_tax_pct/100)*transaction_qty) AS total_monthly_sales,
	RANK() OVER (PARTITION BY DATE_TRUNC('month', transaction_date)
             	ORDER BY SUM(unit_price*(1+sales_tax_pct/100)*transaction_qty) DESC) AS sales_rank
  FROM coffee_shop_sales
  WHERE date_trunc('year', transaction_date) = date_trunc('year', now()) - interval '1 year'
  AND unit_price*(1+sales_tax_pct/100)*transaction_qty>20
  GROUP BY 1, 2)
SELECT
  to_char(month, 'YYYY-MM') AS month,
  store,
  round(total_monthly_sales,2) AS total_monthly_sales
FROM ranked_sales
WHERE sales_rank = 1
ORDER BY month;

	QUERY PLAN
------------------------------------------------------------------------------
 Sort  (cost=893953.86..893953.96 rows=40 width=96) (actual time=2948.391..2948.417 rows=12 loops=1)
   Sort Key: (to_char(ranked_sales.month, 'YYYY-MM'::text))
   Sort Method: quicksort  Memory: 25kB
   ->  Subquery Scan on ranked_sales  (cost=893569.08..893952.80 rows=40 width=96) (actual time=2948.344..2948.383 rows=12 loops=1)
     	Filter: (ranked_sales.sales_rank = 1)
     	->  WindowAgg  (cost=893569.08..893851.67 rows=8074 width=80) (actual time=2948.338..2948.373 rows=12 loops=1)
           	Run Condition: (rank() OVER (?) <= 1)
           	->  Sort  (cost=893569.08..893589.27 rows=8074 width=72) (actual time=2948.324..2948.351 rows=36 loops=1)
                 	Sort Key: (date_trunc('month'::text, (coffee_shop_sales.transaction_date)::timestamp with time zone)), (sum(((coffee_shop_sales.unit_price * ('1'::numeric + (coffee_shop_sales.sales_tax_pct / '100'::numeric))) * coffee_shop_sales.transaction_qty))) DESC
                 	Sort Method: quicksort  Memory: 27kB
                 	->  Finalize GroupAggregate  (cost=890207.19..893045.12 rows=8074 width=72) (actual time=2927.807..2948.320 rows=36 loops=1)
                       	Group Key: ((((coffee_shop_sales.store_id)::text || ': '::text) || coffee_shop_sales.store_location)), (date_trunc('month'::text, (coffee_shop_sales.transaction_date)::timestamp with time zone))
                       	->  Gather Merge  (cost=890207.19..892661.61 rows=16148 width=72) (actual time=2927.677..2948.280 rows=108 loops=1)
                             	Workers Planned: 2
                             	Workers Launched: 2
                             	->  Partial GroupAggregate  (cost=889207.17..889797.70 rows=8074 width=72) (actual time=2891.938..2912.869 rows=36 loops=3)
                                   	Group Key: ((((coffee_shop_sales.store_id)::text || ': '::text) || coffee_shop_sales.store_location)), (date_trunc('month'::text, (coffee_shop_sales.transaction_date)::timestamp with time zone))
                                   	->  Sort  (cost=889207.17..889253.23 rows=18425 width=56) (actual time=2891.713..2895.854 rows=62219 loops=3)
                                         	Sort Key: ((((coffee_shop_sales.store_id)::text || ': '::text) || coffee_shop_sales.store_location)), (date_trunc('month'::text, (coffee_shop_sales.transaction_date)::timestamp with time zone))
                                         	Sort Method: external merge  Disk: 3232kB
                                         	Worker 0:  Sort Method: external merge  Disk: 3056kB
                                         	Worker 1:  Sort Method: external merge  Disk: 3336kB
                                         	->  Parallel Seq Scan on coffee_shop_sales  (cost=0.00..887901.81 rows=18425 width=56) (actual time=2.044..2874.587 rows=62219 loops=3)
                                               	Filter: ((((unit_price * ('1'::numeric + (sales_tax_pct / '100'::numeric))) * transaction_qty) > '20'::numeric) AND (date_trunc('year'::text, (transaction_date)::timestamp with time zone) = (date_trunc('year'::text, now()) - '1 year'::interval)))
                                               	Rows Removed by Filter: 8781589
 Planning Time: 0.674 ms
 Execution Time: 2949.244 ms

```

Amongst other things, we see a full table scan on the coffee_shop_sales table: `Seq Scan on coffee_shop_sales` and some sorts on disk: `Sort Method: external merge Disk: 3056kB`.
## [Analytics tuning solutions](https://www.crunchydata.com/blog/postgres-tuning-and-performance-for-analytics-data#analytics-tuning-solutions)
Let’s look at some of the things you can do to tune your analytics queries and make sure they don’t have too much impact on your operational database activity.
### [Configuration parameters](https://www.crunchydata.com/blog/postgres-tuning-and-performance-for-analytics-data#configuration-parameters)
Your database configuration parameters have probably (hopefully) been carefully considered and set to optimize your day-to-day application activity. If not, I highly recommend having a look at them. I discussed some of them in [Tuning PostgreSQL to work even better](https://youtu.be/7CnqVoMxoeo).
  * Some parameters need to be set across the whole of your database instance.
  * Some parameters can be set for individual users or individual sessions.
  * Some can be set for individual statements.


For parameters that can be set per user, you could create a dedicated analytics role with appropriate values. For the parameters that have to be set across your whole Postgres instance, you're going to have to find some kind of compromise that works for your OLTP activity as well as your analytics activity. That part can be a bit of a challenge.
We’ll just look at a few of the most relevant parameters here.
### [max_connections](https://www.crunchydata.com/blog/postgres-tuning-and-performance-for-analytics-data#max_connections)
The chances are, you won't have all that many concurrent analytics connections, but those connections are likely to be using a lot of resources, so you probably want to keep an eye on them and make sure there aren't too many of them.
The [max_connections](https://www.postgresql.org/docs/current/runtime-config-connection.html#GUC-MAX-CONNECTIONS) parameter specifies the maximum number of concurrent client connections allowed for the entire instance. It's 100 by default, and on most systems you don’t want to increase it too much higher than that (definitely no more than a few hundred if you can help it).
### [Connection pooling](https://www.crunchydata.com/blog/postgres-tuning-and-performance-for-analytics-data#connection-pooling)
You probably want to limit the number of analytics connections to a much smaller number. To do that you might want to look at [connection pooling](https://www.crunchydata.com/blog/your-guide-to-connection-management-in-postgres) (for example using PgBouncer) so you can create a separate, smaller, pool for analytics connections.
### [work_mem](https://www.crunchydata.com/blog/postgres-tuning-and-performance-for-analytics-data#work_mem)
[work_mem](https://www.postgresql.org/docs/current/runtime-config-resource.html#GUC-WORK-MEM%22) says how much memory a query operation can use before it has to create a temporary file on disk. The default value of work_mem is 4MB, and larger values can be useful for complex queries that perform large sort or hash operations.
If your queries are having to perform sorts on disk, it might mean you need to increase work_mem. To check if and when this is happening, you can set log_temp_files to 0 to record in your Postgres logs whenever a temporary file is created.
With the default value of work_mem, we saw `Sort Method: external merge` in the execution plan, indicating that our query created some temporary files on disk.
I tested the query with different values of work_mem and found that we were able to get rid of the disk sorts and perform the sort in memory when work_mem was set to 8MB and above. This was shown as `Sort Method: quicksort` in the execution plan.
It’s tempting to just set work_mem to a really high value, but be aware that a complex query might run multiple sort or hash operations in parallel, and that several running sessions could be doing that type of operation at the same time, so you could end up using many GB of memory.
Instead, you can set work_mem to a high value just for specific analytics sessions, and make sure there aren’t too many of them at the same time.
### [statement_timeout](https://www.crunchydata.com/blog/postgres-tuning-and-performance-for-analytics-data#statement_timeout)
If you think your analytics queries may run for too long and therefore cause performance issues on your database, you could set [statement_timeout](https://www.crunchydata.com/blog/control-runaway-postgres-queries-with-statement-timeout), which will abort any statement that runs for longer than a set amount of time.
It's disabled by default, so statements can run for as long as they need to.
You can set it for the entire instance, but it's probably better to do it for individual sessions or groups of sessions. Certain analytics queries might be OK running for many minutes, but you might expect statements executed via your application to take milliseconds.
Here, I set statement_timeout to 2 seconds and then tried rerunning the query (I saved the query in a file called coffee_shop_query.sql so I can run it whenever I want to with the \i command):
```
coffee=# SET statement_timeout='2s';
SET

coffee=# SHOW statement_timeout;
 statement_timeout
-------------------
 2s

coffee=# \i coffee_shop_query.sql
psql:coffee_shop_query.sql:20: **ERROR:  canceling statement due to statement timeout**
Time: 2080.006 ms (00:02.080)

```

You can see the query was cancelled after just over 2 seconds.
If you want to know whenever a query is cancelled due to statement_timeout, make sure that [log_min_error_statement](https://www.postgresql.org/docs/current/runtime-config-logging.html#GUC-LOG-MIN-ERROR-STATEMENT) is set to ERROR (the default) or above. The information will be recorded in your Postgres logs.
### [max_parallel_workers_per_gather](https://www.crunchydata.com/blog/postgres-tuning-and-performance-for-analytics-data#max_parallel_workers_per_gather)
PostgreSQL can [parallelize queries](https://www.crunchydata.com/blog/parallel-queries-in-postgre) using multiple processes, but you may have to tune how many workers a query can be used. There can be up to max_parallel_workers (8 by default) parallel worker processes total in the system, and an individual query can use up to max_parallel_workers_per_gather (2 by default) of those. Fortunately, the original PostgreSQL process that is handling your query can also do work, so you get 3 processes total by default.
Of course, machines often have many CPUs, so it often makes sense to raise max_parallel_workers and max_parallel_workers_per_gather to be closer to the number of cores. The downside is that your query will use more resources, and if all the parallel workers are busy with concurrent queries, new queries will not be parallelized at all.
Nonetheless, if you have an analytical workload, raising max_parallel_workers_per_gather can often make your queries several times faster.
## [Indexes](https://www.crunchydata.com/blog/postgres-tuning-and-performance-for-analytics-data#indexes)
You'll probably need specific [indexes](https://www.crunchydata.com/blog/postgres-indexes-for-newbies) for your analytics queries. Just remember that indexes need to be maintained. Although they can improve performance of selects, they can impact the performance of your inserts and updates, so you should only create the ones that will be really useful to you.
As well as creating indexes on one or more table columns, you can also create [indexes on functions or scalar expressions](https://www.postgresql.org/docs/current/indexes-expressional.html) based on your table columns.
I created an index on the expression `unit_price*(1+sales_tax_pct/100)*transaction_qty` that’s used to calculate the total sale amount in the query:
```
CREATE INDEX css_total_sale_amt
ON coffee_shop_sales((unit_price*(1+sales_tax_pct/100)*transaction_qty));

```

Re-running the query, we see `Bitmap Index Scan on css_total_sale_amt` in the execution plan, showing that the index is used and the execution time goes down to just over a second.
```
	QUERY PLAN
-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
 Sort  (cost=863063.33..863063.36 rows=10 width=96) (actual time=1143.634..1143.993 rows=12 loops=1)
   Sort Key: (to_char(ranked_sales.month, 'YYYY-MM'::text))
   Sort Method: quicksort  Memory: 25kB
   ->  Subquery Scan on ranked_sales  (cost=862971.68..863063.17 rows=10 width=96) (actual time=1143.572..1143.945 rows=12 loops=1)
     	Filter: (ranked_sales.sales_rank = 1)
     	->  WindowAgg  (cost=862971.68..863039.06 rows=1925 width=80) (actual time=1143.562..1143.931 rows=12 loops=1)
           	Run Condition: (rank() OVER (?) <= 1)
           	->  Sort  (cost=862971.68..862976.49 rows=1925 width=72) (actual time=1143.556..1143.916 rows=36 loops=1)
                 	Sort Key: (date_trunc('month'::text, (coffee_shop_sales.transaction_date)::timestamp with time zone)), (sum(((coffee_shop_sales.unit_price * ('1'::numeric + (coffee_shop_sales.sales_tax_pct / '100'::numeric))) * coffee_shop_sales.transaction_qty))) DESC
                 	Sort Method: quicksort  Memory: 27kB
                 	->  Finalize GroupAggregate  (cost=862540.74..862866.67 rows=1925 width=72) (actual time=1123.470..1143.903 rows=36 loops=1)
                       	Group Key: ((((coffee_shop_sales.store_id)::text || ': '::text) || coffee_shop_sales.store_location)), (date_trunc('month'::text, (coffee_shop_sales.transaction_date)::timestamp with time zone))
                       	->  Gather Merge  (cost=862540.74..862795.43 rows=1830 width=72) (actual time=1123.333..1143.864 rows=108 loops=1)
                             	Workers Planned: 2
                             	Workers Launched: 2
                             	->  Partial GroupAggregate  (cost=861540.72..861584.18 rows=915 width=72) (actual time=1089.824..1110.195 rows=36 loops=3)
                                   	Group Key: ((((coffee_shop_sales.store_id)::text || ': '::text) || coffee_shop_sales.store_location)), (date_trunc('month'::text, (coffee_shop_sales.transaction_date)::timestamp with time zone))
                                   	->  Sort  (cost=861540.72..861543.00 rows=915 width=56) (actual time=1089.600..1093.336 rows=62219 loops=3)
                                         	Sort Key: ((((coffee_shop_sales.store_id)::text || ': '::text) || coffee_shop_sales.store_location)), (date_trunc('month'::text, (coffee_shop_sales.transaction_date)::timestamp with time zone))
                                         	Sort Method: external merge  Disk: 3192kB
                                         	Worker 0:  Sort Method: external merge  Disk: 3208kB
                                         	Worker 1:  Sort Method: external merge  Disk: 3216kB
                                         	->  Parallel Bitmap Heap Scan on coffee_shop_sales  (cost=8125.30..861495.71 rows=915 width=56) (actual time=68.788..1071.567 rows=62219 loops=3)
                                               	Recheck Cond: (((unit_price * ('1'::numeric + (sales_tax_pct / '100'::numeric))) * transaction_qty) > '20'::numeric)
                                               	Rows Removed by Index Recheck: 2369902
                                               	Filter: (date_trunc('year'::text, (transaction_date)::timestamp with time zone) = (date_trunc('year'::text, now()) - '1 year'::interval))
                                               	Rows Removed by Filter: 87104
                                               	Heap Blocks: exact=12330 lossy=44445
                                               	->  Bitmap Index Scan on css_total_sale_amt  (cost=0.00..8124.75 rows=439492 width=0) (actual time=75.955..75.955 rows=447968 loops=1)
                                                     	Index Cond: (((unit_price * ('1'::numeric + (sales_tax_pct / '100'::numeric))) * transaction_qty) > '20'::numeric)
 Planning Time: 1.723 ms
 Execution Time: 1145.800 ms

```

## [Pre-Calculating data](https://www.crunchydata.com/blog/postgres-tuning-and-performance-for-analytics-data#pre-calculating-data)
Most analytics queries aggregate, sort and calculate large quantities of data: totals, averages, comparisons, groupings etc.
If you pre-calculate, pre-sort and pre-aggregate some of the data that's needed in your analytics queries, you can do it just once so it doesn't have to be done every time you run your analytics queries.
### [Generated columns](https://www.crunchydata.com/blog/postgres-tuning-and-performance-for-analytics-data#generated-columns)
You can create a [generated column](https://www.postgresql.org/docs/current/ddl-generated-columns.html) whose value is calculated automatically to match an expression used in your queries. For example, we might want a total_sale_amt column in the coffee_shop_sales table with the default value `unit_price*(1+sales_tax_pct/100)*transaction_qty`.
You can do this using the GENERATED ALWAYS AS keywords:
```
ALTER TABLE coffee_shop_sales
  ADD COLUMN total_sale_amt numeric
  GENERATED ALWAYS AS
    ((unit_price*(1+sales_tax_pct/100)*transaction_qty)) STORED;

```

The STORED keyword says that the column value should be physically stored in the table rather than calculated at query-time. This can improve query performance but it will, of course, affect inserts into the table.
Now, we can use the calculated column total_sale_amt in our query instead of the expression `unit_price*(1+sales_tax_pct/100)*transaction_qty`:
```
WITH ranked_sales AS (
  SELECT
	store_id::text||': '||store_location AS store,
	DATE_TRUNC('month', transaction_date) AS month,
	SUM(total_sale_amt) AS total_monthly_sales,
	RANK() OVER (PARTITION BY DATE_TRUNC('month', transaction_date)
             	ORDER BY SUM(total_sale_amt) DESC) AS sales_rank
  FROM coffee_shop_sales
  WHERE date_trunc('year', transaction_date) = date_trunc('year', now()) - interval '1 year'
  AND total_sale_amt>20
  GROUP BY 1, 2)
SELECT
  to_char(month, 'YYYY-MM') AS month,
  store,
  round(total_monthly_sales,2) AS total_monthly_sales
FROM ranked_sales
WHERE sales_rank = 1
ORDER BY month;

```

This took the execution time down to around 2.2 seconds.
You can also create an index on the generated column:
```
CREATE INDEX css_total_sale_amt
ON coffee_shop_sales(total_sale_amt);

```

With the index on the generated column, the query takes just 0.6 seconds to execute.
### [Materialized views](https://www.crunchydata.com/blog/postgres-tuning-and-performance-for-analytics-data#materialized-views)
[Materialized views](https://www.crunchydata.com/developers/playground/materialized-views) are another useful way to pre-aggregate and pre-sort your data. A materialized view is a physical copy of the results of a query. They can be particularly useful when you don’t need the data to be completely up to date - data from an hour ago, a day ago or even a week ago might be good enough for analytics.
We can create a materialized view based on the ranked_sales section of our query.
```
CREATE MATERIALIZED VIEW ranked_sales_mv AS (
  SELECT
	store_id::text||': '||store_location AS store,
	DATE_TRUNC('month', transaction_date) AS month,
	SUM(unit_price*(1+sales_tax_pct/100)*transaction_qty) AS total_monthly_sales,
	RANK() OVER (PARTITION BY DATE_TRUNC('month', transaction_date)
             	ORDER BY SUM(unit_price*(1+sales_tax_pct/100)*transaction_qty) DESC) AS sales_rank
  FROM coffee_shop_sales
  WHERE date_trunc('year', transaction_date) = date_trunc('year', now()) - interval '1 year'
  AND unit_price*(1+sales_tax_pct/100)*transaction_qty>20
  GROUP BY 1, 2);

```

The 26.5 million rows of data in the coffee_shop_sales table have been aggregated into just 36 rows in the ranked_sales_mv materialized view:
```
SELECT * FROM ranked_sales_mv;

```
```
┌────────────────────┬────────────────────────┬─────────────────────┬────────────┐
|      store         |         month          | total_monthly_sales | sales_rank |
├────────────────────┼────────────────────────┼─────────────────────┼────────────┤
| 5: Lower Manhattan | 2023-01-01 00:00:00+01 |          92228.864  |          1 |
| 8: Hell's Kitchen  | 2023-01-01 00:00:00+01 |          71506.816  |          2 |
| 3: Astoria         | 2023-01-01 00:00:00+01 |          51875.312  |          3 |...
...
| 5: Lower Manhattan | 2023-12-01 00:00:00+01 |          85971.504  |          2 |
| 3: Astoria         | 2023-12-01 00:00:00+01 |          84232.112  |          3 |
└────────────────────┴────────────────────────┴─────────────────────┴────────────┘
(36 rows)


```

Whenever you want to use that block in a bigger query, you can select from the materialized view where the data has already been calculated, aggregated and sorted:
```
SELECT
  to_char(month, 'YYYY-MM') AS month,
  store,
  round(total_monthly_sales,2) AS total_monthly_sales
FROM ranked_sales_mv
WHERE sales_rank = 1
ORDER BY month;

```
```
┌─────────┬────────────────────┬─────────────────────┐
|  month  |       store        | total_monthly_sales |
├─────────┼────────────────────┼─────────────────────┤
| 2023-01 | 5: Lower Manhattan |            92228.86 |
| 2023-02 | 5: Lower Manhattan |            74252.86 |
| 2023-03 | 5: Lower Manhattan |            49454.54 |
| 2023-04 | 8: Hell's Kitchen  |            84161.92 |
| 2023-05 | 8: Hell's Kitchen  |           102180.72 |
| 2023-06 | 3: Astoria         |          1908647.57 |
| 2023-07 | 8: Hell's Kitchen  |            71506.82 |
| 2023-08 | 8: Hell's Kitchen  |            40446.00 |
| 2023-09 | 5: Lower Manhattan |            49454.54 |
| 2023-10 | 3: Astoria         |          1383157.99 |
| 2023-11 | 8: Hell's Kitchen  |           102180.72 |
| 2023-12 | 8: Hell's Kitchen  |           128999.20 |
└─────────┴────────────────────┴─────────────────────┘

(12 rows)

Time: 1.816 ms

```

This returns the results in a couple of milliseconds instead of several seconds!
Note that you’ll need to schedule a periodic [refresh](https://www.postgresql.org/docs/current/sql-refreshmaterializedview.html) of the materialized view to re-execute the query and re-populate the materialized view with up to date information. The frequency will depend on how up to date you need the data to be.
If you use [pg_cron](https://github.com/citusdata/pg_cron), you can set up a periodic refresh in PostgreSQL itself. This example schedules an hourly refresh of the ranked_sales_mv materialized view:
```
SELECT cron.schedule('@hourly', 'REFRESH MATERIALIZED VIEW CONCURRENTLY ranked_sales_mv');

```

You can also create indexes on a materialized view.
Here's a quick table to show the improvements we've made on the sample data.
![](https://imagedelivery.net/lPM0ntuwQfh8VQgJRu0mFg/70560449-867a-47c3-77fd-7e6eb0a4d200/public)
## [Separate analytics database](https://www.crunchydata.com/blog/postgres-tuning-and-performance-for-analytics-data#separate-analytics-database)
Often the best way to avoid impacting your application database is probably by not running analytics queries against it at all. Even if you don’t have a completely separate analytics environment, there are still some options that might be available to you.
### [Read replica](https://www.crunchydata.com/blog/postgres-tuning-and-performance-for-analytics-data#read-replica)
You've probably already got a high availability architecture in place, which usually means you have one or more standby databases that are kept in sync with the primary via physical replication.
The replica databases are available for read-only transactions, so you could send your analytics workload to one of them to take load off your primary application database.
Just be aware that physical replication gives you an exact copy of the primary database cluster, and you can't make any changes on the standby. You can’t create separate users, create indexes, change the layout of the schema etc. Any changes have to be made on the primary and propagated across.
### [Logical replication](https://www.crunchydata.com/blog/postgres-tuning-and-performance-for-analytics-data#logical-replication)
Another option is [logical replication](https://www.postgresql.org/docs/current/logical-replication.html). You can use this to replicate just certain schemas or tables from a publisher database (your primary application DB) to a subscriber database (your analytics DB).
From Postgres version 16 onwards, you can also set up logical replication from a standby, which can take even more pressure off your primary database.
Logical replication is more complicated to put in place and maintain than physical replication, but it's more flexible. You can:
  * Replicate just a selection of objects.
  * Replicate to/from multiple targets/sources.
  * Make the subscriber database available for read-write activity.


Create indexes, users, materialized views etc. on the subscriber database.
### [Columnar analytics databases](https://www.crunchydata.com/blog/postgres-tuning-and-performance-for-analytics-data#columnar-analytics-databases)
Part of what makes analytical queries on PostgreSQL quite expensive is that the storage format and query engine are not optimized for analytical queries. For instance, a query that sums a single column will read all the data in the table from disk.
Analytical database systems like Snowflake, Databricks, Clickhouse and others use columnar storage to be able to efficiently skip columns and make operations that aggregate across many rows a lot faster. Nowadays, analytics data is often stored in files in object storage due to its low cost and seemingly infinite scale. The most commonly used columnar file format is [Parquet](https://parquet.apache.org/). Parquet files can be organized into a modifiable table using the [Iceberg table format](https://iceberg.apache.org/).
[Crunchy Data Warehouse](https://www.crunchydata.com/products/crunchy-bridge-for-analytics) is a new PostgreSQL service with additional extensions for creating Iceberg tables and running very fast analytical queries on them. You can also query/import/export files in object storage in a variety of formats, using native PostgreSQL syntax.
Let’s repeat our example using Iceberg in Crunchy Data Warehouse:
```
CREATE TABLE coffee_shop_sales_iceberg USING iceberg
AS SELECT * FROM coffee_shop_sales;

```
```
WITH ranked_sales AS (
  SELECT
	store_id::text||': '||store_location AS store,
	DATE_TRUNC('month', transaction_date) AS month,
	SUM(unit_price*(1+sales_tax_pct/100)*transaction_qty) AS total_monthly_sales,
	RANK() OVER (PARTITION BY DATE_TRUNC('month', transaction_date)
             	ORDER BY SUM(unit_price*(1+sales_tax_pct/100)*transaction_qty) DESC) AS sales_rank
  FROM coffee_shop_sales_iceberg
  WHERE date_trunc('year', transaction_date) = date_trunc('year', now()) - interval '1 year'
  AND unit_price*(1+sales_tax_pct/100)*transaction_qty>20
  GROUP BY 1, 2)
SELECT
  to_char(month, 'YYYY-MM') AS month,
  store,
  round(total_monthly_sales,2) AS total_monthly_sales
FROM ranked_sales
WHERE sales_rank = 1
ORDER BY month;

```
```
┌─────────┬────────────────────┬─────────────────────┐
│  month  │       store        │ total_monthly_sales │
├─────────┼────────────────────┼─────────────────────┤
│ 2023-01 │ 5: Lower Manhattan │            92228.86 │
│ 2023-02 │ 5: Lower Manhattan │            74252.86 │
│ 2023-03 │ 5: Lower Manhattan │            49454.54 │
│ 2023-04 │ 8: Hell's Kitchen  │            84161.92 │
│ 2023-05 │ 8: Hell's Kitchen  │           102180.72 │
│ 2023-06 │ 3: Astoria         │          1908647.57 │
│ 2023-07 │ 8: Hell's Kitchen  │            71506.82 │
│ 2023-08 │ 8: Hell's Kitchen  │            40446.00 │
│ 2023-09 │ 5: Lower Manhattan │            49454.54 │
│ 2023-10 │ 3: Astoria         │          1383157.99 │
│ 2023-11 │ 8: Hell's Kitchen  │           102180.72 │
│ 2023-12 │ 8: Hell's Kitchen  │           128999.20 │
└─────────┴────────────────────┴─────────────────────┘
(12 rows)

Time: 205.417 ms

```

Without doing additional tuning, we got >10x better performance than our initial attempt on PostgreSQL. In addition, the Iceberg table is only 523MB, compared to 3.7GB for the PostgreSQL table. The underlying files are stored in object storage (with local caching), so it will only cost ~$0.02/month to store the Iceberg table.
## [Summary](https://www.crunchydata.com/blog/postgres-tuning-and-performance-for-analytics-data#summary)
In summary: we looked at various techniques to make sure your database is optimized for analytics without slowing down your application:
  * If you can, use physical or logical replication to create a separate database for your analytics workloadx.
  * Tune configuration parameters for your hybrid workload.
  * Consider your indexing strategies, including indexes on expressions.
  * Create generated columns or materialized views to pre-aggregate, pre-sort and pre-calculate data.
  * Combine the various techniques to get the results you need: create indexes on generated columns, create materialized views on a logical replica etc.
  * Or, use a specialized analytics database. If you want to keep using Postgres, then [Crunchy Data Warehouse](https://docs.crunchybridge.com/warehouse) is a good option.


  
  
Co-authored with [Marco Slot](http://localhost:3060/blog/author/marco-slot).
## Enjoy this article?
You will love our newsletter!
Do not fill this out please: Do not fill this out please, it will be pre-filled:
Email address
Join The List
## Related Articles
  * Dec 4, 2025·9 min read
[Postgres Scan Types in EXPLAIN Plans](https://www.crunchydata.com/blog/postgres-scan-types-in-explain-plans)
  * Nov 21, 2025·3 min read
[PostGIS Performance: Data Sampling](https://www.crunchydata.com/blog/postgis-performance-data-sampling)
  * Nov 14, 2025·3 min read
[PostGIS Performance: Intersection Predicates and Overlays](https://www.crunchydata.com/blog/postgis-performance-intersection-predicates-and-overlays)
  * Nov 7, 2025·9 min read
[Postgres Internals Hiding in Plain Sight](https://www.crunchydata.com/blog/postgres-internals-hiding-in-plain-sight)
  * Nov 6, 2025·4 min read
[PostGIS Performance: Improve Bounding Boxes with Decompose and Subdivide](https://www.crunchydata.com/blog/postgis-performance-improve-bounding-boxes-with-decompose-and-subdivide)



Products
     [Crunchy Postgres](https://www.crunchydata.com/products/crunchy-high-availability-postgresql)[Crunchy Postgres for Kubernetes](https://www.crunchydata.com/products/crunchy-postgresql-for-kubernetes)[Crunchy Bridge](https://www.crunchydata.com/products/crunchy-bridge)[Crunchy Certified PostgreSQL](https://www.crunchydata.com/products/crunchy-certified-postgresql)[Crunchy PostgreSQL for Cloud Foundry](https://www.crunchydata.com/products/crunchy-postgresql-for-cloud-foundry)[Crunchy MLS PostgreSQL](https://www.crunchydata.com/products/crunchy-mls-postgresql)[Crunchy Spatial](https://www.crunchydata.com/products/crunchy-spatial) 

Services & Support
     [Enterprise PostgreSQL Support](https://www.crunchydata.com/solutions/enterprise-postgresql-support)[Ansible](https://www.crunchydata.com/solutions/ansible)[Red Hat Partner](https://www.crunchydata.com/red-hat-certified-technologies)[Trusted PostgreSQL](https://www.crunchydata.com/about/postgresql-enterprise-database)[Crunchy Data Subscription](https://www.crunchydata.com/about/value-of-subscription) 

Migrate to Crunchy Data
     [Migrate from RDS](https://www.crunchydata.com/migrate-from-rds)[Migrate from Heroku](https://www.crunchydata.com/migrate-from-heroku) 

Resources
     [Customer Portal](https://access.crunchydata.com)[Documentation](https://access.crunchydata.com/documentation/)[Postgres Tutorials](https://www.crunchydata.com/developers/tutorials)[Crunchy Bridge Walkthrough](https://www.crunchydata.com/developers/get-started/fully-managed-postgres)[Postgres Operator Walkthrough](https://www.crunchydata.com/developers/get-started/postgres-operator)[Blog](https://www.crunchydata.com/blog)[Events](https://www.crunchydata.com/events) 

Company
     [About](https://www.crunchydata.com/about)[Team](https://www.crunchydata.com/team)[News](https://www.crunchydata.com/news)[Contact Us](https://www.crunchydata.com/contact)[Newsletter](https://www.crunchydata.com/newsletter)[Branding](https://www.crunchydata.com/branding)[Privacy Notice – Recently Updated](https://www.snowflake.com/en/legal/privacy/privacy-policy/)[Security](https://www.crunchydata.com/security)Cookies Settings
Subscribe to the Crunchy Data Newsletter and receive Postgres content every month.
Do not fill this out please: Do not fill this out please, it will be pre-filled:
Email address
Subscribe
© 2018-2025 Crunchy Data Solutions, Inc.
[YouTube](https://www.youtube.com/c/CrunchyDataPostgres)[LinkedIn](https://www.linkedin.com/company/crunchy-data-solutions-inc-)[X](https://twitter.com/crunchydata)[GitHub](https://github.com/CrunchyData)
