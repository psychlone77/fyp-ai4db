# PERCONA-TUNING-POSTGRESQL-DATABASE-PARAMETERS-TO-OPTIMIZE-PERFORMANCE

**Source:** https://www.percona.com/blog/tuning-postgresql-database-parameters-to-optimize-performance
**Generated:** 2026-01-08T14:11:27.087750

---

Opens in a new window Opens an external website Opens an external website in a new window
<!---->Close this dialog<!----> 
This website utilizes technologies such as cookies to enable essential site functionality, as well as for analytics personalization, and marketing. By continuing to use our website, you acknowledge having read and understood our To learn more, view the following link:  [Privacy Policy](https://www.percona.com/privacy-policy)
Manage Preferences 
<!---->Close Cookie Preferences<!----> 
[ ![Percona Database Performance Blog](https://www.percona.com/blog/wp-content/uploads/2023/02/logo.svg) ](https://www.percona.com)
  * [Solutions](https://www.percona.com/blog/tuning-postgresql-database-parameters-to-optimize-performance/)
    * [Solutions Dropdown](https://www.percona.com/blog/tuning-postgresql-database-parameters-to-optimize-performance/)
Featured
#### MySQL 5.7   
Support
![Percona Server for MySQL](https://www.percona.com/wp-content/uploads/2023/04/mysqlicon-1.png)
[Learn More](https://www.percona.com/post-mysql-5-7-eol-support)
#### Compare Percona to Leading Database Solutions
[Start](https://www.percona.com/compare-mysql-mongodb-postgresql-mariadb)
Percona Products
    * [MySQL](https://www.percona.com/mysql)
[Software](https://www.percona.com/mysql/software) [Support and Services](https://www.percona.com/mysql/support-and-services) [Kubernetes](https://www.percona.com/mysql/kubernetes)
    * [MongoDB](https://www.percona.com/mongodb)
[Software](https://www.percona.com/mongodb/software) [Support and Services](https://www.percona.com/mongodb/support-and-services) [Kubernetes](https://www.percona.com/mongodb/kubernetes)
    * [PostgreSQL](https://www.percona.com/postgresql)
[Software](https://www.percona.com/postgresql/software) [Support and Services](https://www.percona.com/postgresql/support-and-services) [Kubernetes](https://www.percona.com/postgresql/kubernetes)
    * [Cloud Native](https://www.percona.com/cloud-native)
[Software](https://www.percona.com/cloud-native/software) [Percona Operators](https://www.percona.com/software/percona-operators) [Percona Everest](https://www.percona.com/software/percona-everest) [Support and Services](https://www.percona.com/cloud-native/support-and-services)
    * [Valkey/Redis](https://www.percona.com/valkey-redis)
[Software](https://docs.percona.com/valkey/index.html) [Services](https://www.percona.com/valkey-redis/support-and-services) [Performance Calculator](https://www.percona.com/calculator/valkey-redis-savings-and-performance)
    * [Monitoring](https://www.percona.com/software/database-tools/percona-monitoring-and-management)
    * [Percona Toolkit](https://www.percona.com/percona-toolkit)
Percona Services
    * [Support](https://www.percona.com/services/support)
    * [Managed Services](https://www.percona.com/services/managed-services)
    * [Consulting](https://www.percona.com/services/consulting)
    * [Policies](https://www.percona.com/services/policies)
    * [Training](https://www.percona.com/training)
Use Cases
    * [Emergency Support](https://www.percona.com/services/emergency-support)
    * [High-Traffic Events](https://www.percona.com/services/high-traffic)
    * [Performance Tuning](https://www.percona.com/services/database-performance)
    * [Migrations](https://www.percona.com/services/open-source-migration)
    * [Upgrades](https://www.percona.com/services/open-source-upgrade)
    * [Security](https://www.percona.com/services/database-security)
  * [Resources](https://www.percona.com/blog/tuning-postgresql-database-parameters-to-optimize-performance/)
    * [Learn Dropdown](https://www.percona.com/blog/tuning-postgresql-database-parameters-to-optimize-performance/)
Percona Resources
#### Software   
Downloads
All of Percona’s open source software products, in one place, to download as much or as little as you need. 
[View Downloads](https://www.percona.com/downloads)
#### Valkey Contribution
[Learn More](https://www.percona.com/valkey-project-contribution)
#### Product Documentation
[View Documentation](https://docs.percona.com/)
#### Resource Hub
A single source for all resources
[Webinars](https://www.percona.com/resources/webinars)
[Presentations](https://www.percona.com/resources/technical-presentations)
[Datasheets](https://www.percona.com/resources/datasheets)
[Ebooks](https://www.percona.com/resources/ebooks)
[Downloads](https://www.percona.com/downloads)
[Solution Briefs](https://www.percona.com/resources/solution-brief)
[Case Studies](https://www.percona.com/resources/case-studies)
[Percona Videos](https://www.percona.com/resources/videos)
[White Papers](https://www.percona.com/resources/white-papers)
[Documentation](https://docs.percona.com)
[View All Resources](https://www.percona.com/resources)
#### Why Percona for MongoDB?
[Learn More](https://experience.percona.com/mongodb/percona-mongodb-alternative/)
#### Why Percona for PostgreSQL?
[Learn More](https://experience.percona.com/postgresql/hub/)
  * [Community](https://www.percona.com/blog/tuning-postgresql-database-parameters-to-optimize-performance/)
    * [Discover Dropdown](https://www.percona.com/blog/tuning-postgresql-database-parameters-to-optimize-performance/)
Percona Blog
#### Percona Blog
Our popular knowledge center for all Percona products and all related topics.
[View The Blog](https://www.percona.com/blog/)
Community
#### Percona Community Hub
A place to stay in touch with the open-source community
[Forums](https://forums.percona.com)
[Community Blog](https://percona.community/blog/)
[PMM Contributions](https://percona.community/projects/pmm/)
[Explore The Community](https://percona.community/)
Events
#### Percona Events Hub
See all of Percona’s upcoming events and view materials like webinars and forums from past events
[Percona.connect events](https://www.percona.com/connect)
[Upcoming Events](https://www.percona.com/events)
[View Our Events](https://www.percona.com/events)
  * [About](https://www.percona.com/blog/tuning-postgresql-database-parameters-to-optimize-performance/)
    * [About Dropdown](https://www.percona.com/blog/tuning-postgresql-database-parameters-to-optimize-performance/)
About
#### About Percona
Percona is an open source database software, support, and services company that helps make databases and applications run better.
[Learn More](https://www.percona.com/about)
#### Percona in the News
See Percona’s recent news coverage, press releases and industry recognition for our open source software and support.
[News coverage](https://www.percona.com/about/in-the-news)
[Press Releases](https://www.percona.com/about/newsroom/press-releases)
#### Our Customers
[Learn More](https://www.percona.com/about/customers)
#### Our Partners
[Learn More](https://www.percona.com/about/partners)
#### Careers
[Learn More](https://www.percona.com/about/careers)
#### Contact Us
[Let's Talk](https://www.percona.com/about/contact)


  * [Contact us](https://www.percona.com/about/contact)


Select Page
  * [Solutions](https://www.percona.com/blog/tuning-postgresql-database-parameters-to-optimize-performance/)
    * [Solutions Dropdown](https://www.percona.com/blog/tuning-postgresql-database-parameters-to-optimize-performance/)
Featured
#### MySQL 5.7   
Support
![Percona Server for MySQL](data:image/svg+xml,%3Csvg%20xmlns='http://www.w3.org/2000/svg'%20viewBox='0%200%20100%2092'%3E%3C/svg%3E)
[Learn More](https://www.percona.com/post-mysql-5-7-eol-support)
#### Compare Percona to Leading Database Solutions
[Start](https://www.percona.com/compare-mysql-mongodb-postgresql-mariadb)
Percona Products
    * [MySQL](https://www.percona.com/mysql)
[Software](https://www.percona.com/mysql/software) [Support and Services](https://www.percona.com/mysql/support-and-services) [Kubernetes](https://www.percona.com/mysql/kubernetes)
    * [MongoDB](https://www.percona.com/mongodb)
[Software](https://www.percona.com/mongodb/software) [Support and Services](https://www.percona.com/mongodb/support-and-services) [Kubernetes](https://www.percona.com/mongodb/kubernetes)
    * [PostgreSQL](https://www.percona.com/postgresql)
[Software](https://www.percona.com/postgresql/software) [Support and Services](https://www.percona.com/postgresql/support-and-services) [Kubernetes](https://www.percona.com/postgresql/kubernetes)
    * [Cloud Native](https://www.percona.com/cloud-native)
[Software](https://www.percona.com/cloud-native/software) [Percona Operators](https://www.percona.com/software/percona-operators) [Percona Everest](https://www.percona.com/software/percona-everest) [Support and Services](https://www.percona.com/cloud-native/support-and-services)
    * [Valkey/Redis](https://www.percona.com/valkey-redis)
[Software](https://docs.percona.com/valkey/index.html) [Services](https://www.percona.com/valkey-redis/support-and-services) [Performance Calculator](https://www.percona.com/calculator/valkey-redis-savings-and-performance)
    * [Monitoring](https://www.percona.com/software/database-tools/percona-monitoring-and-management)
    * [Percona Toolkit](https://www.percona.com/percona-toolkit)
Percona Services
    * [Support](https://www.percona.com/services/support)
    * [Managed Services](https://www.percona.com/services/managed-services)
    * [Consulting](https://www.percona.com/services/consulting)
    * [Policies](https://www.percona.com/services/policies)
    * [Training](https://www.percona.com/training)
Use Cases
    * [Emergency Support](https://www.percona.com/services/emergency-support)
    * [High-Traffic Events](https://www.percona.com/services/high-traffic)
    * [Performance Tuning](https://www.percona.com/services/database-performance)
    * [Migrations](https://www.percona.com/services/open-source-migration)
    * [Upgrades](https://www.percona.com/services/open-source-upgrade)
    * [Security](https://www.percona.com/services/database-security)
  * [Resources](https://www.percona.com/blog/tuning-postgresql-database-parameters-to-optimize-performance/)
    * [Learn Dropdown](https://www.percona.com/blog/tuning-postgresql-database-parameters-to-optimize-performance/)
Percona Resources
#### Software   
Downloads
All of Percona’s open source software products, in one place, to download as much or as little as you need. 
[View Downloads](https://www.percona.com/downloads)
#### Valkey Contribution
[Learn More](https://www.percona.com/valkey-project-contribution)
#### Product Documentation
[View Documentation](https://docs.percona.com/)
#### Resource Hub
A single source for all resources
[Webinars](https://www.percona.com/resources/webinars)
[Presentations](https://www.percona.com/resources/technical-presentations)
[Datasheets](https://www.percona.com/resources/datasheets)
[Ebooks](https://www.percona.com/resources/ebooks)
[Downloads](https://www.percona.com/downloads)
[Solution Briefs](https://www.percona.com/resources/solution-brief)
[Case Studies](https://www.percona.com/resources/case-studies)
[Percona Videos](https://www.percona.com/resources/videos)
[White Papers](https://www.percona.com/resources/white-papers)
[Documentation](https://docs.percona.com)
[View All Resources](https://www.percona.com/resources)
#### Why Percona for MongoDB?
[Learn More](https://experience.percona.com/mongodb/percona-mongodb-alternative/)
#### Why Percona for PostgreSQL?
[Learn More](https://experience.percona.com/postgresql/hub/)
  * [Community](https://www.percona.com/blog/tuning-postgresql-database-parameters-to-optimize-performance/)
    * [Discover Dropdown](https://www.percona.com/blog/tuning-postgresql-database-parameters-to-optimize-performance/)
Percona Blog
#### Percona Blog
Our popular knowledge center for all Percona products and all related topics.
[View The Blog](https://www.percona.com/blog/)
Community
#### Percona Community Hub
A place to stay in touch with the open-source community
[Forums](https://forums.percona.com)
[Community Blog](https://percona.community/blog/)
[PMM Contributions](https://percona.community/projects/pmm/)
[Explore The Community](https://percona.community/)
Events
#### Percona Events Hub
See all of Percona’s upcoming events and view materials like webinars and forums from past events
[Percona.connect events](https://www.percona.com/connect)
[Upcoming Events](https://www.percona.com/events)
[View Our Events](https://www.percona.com/events)
  * [About](https://www.percona.com/blog/tuning-postgresql-database-parameters-to-optimize-performance/)
    * [About Dropdown](https://www.percona.com/blog/tuning-postgresql-database-parameters-to-optimize-performance/)
About
#### About Percona
Percona is an open source database software, support, and services company that helps make databases and applications run better.
[Learn More](https://www.percona.com/about)
#### Percona in the News
See Percona’s recent news coverage, press releases and industry recognition for our open source software and support.
[News coverage](https://www.percona.com/about/in-the-news)
[Press Releases](https://www.percona.com/about/newsroom/press-releases)
#### Our Customers
[Learn More](https://www.percona.com/about/customers)
#### Our Partners
[Learn More](https://www.percona.com/about/partners)
#### Careers
[Learn More](https://www.percona.com/about/careers)
#### Contact Us
[Let's Talk](https://www.percona.com/about/contact)


[ ![PostgreSQL Performance Tuning Guide: Settings That Make a Difference](https://www.percona.com/blog/wp-content/uploads/2023/03/lucas.speyer_a_robot_elephant_made_out_of_computer_hardware_mou_9d69e266-d848-45e2-96e7-c6cc36f8586f.jpg) ](https://www.percona.com/blog/tuning-postgresql-database-parameters-to-optimize-performance/)
[Insight for DBAs](https://www.percona.com/blog/category/dba-insight/) [Open Source](https://www.percona.com/blog/category/open-source/) [PostgreSQL](https://www.percona.com/blog/category/postgresql/)
[ ](https://www.percona.com/blog/feed)
# PostgreSQL Performance Tuning Guide: Settings That Make a Difference
April 1, 2025
[Ibrar Ahmed](https://www.percona.com/blog/author/ibrar-ahmed)
_This blog was first authored by Ibrar Ahmed in 2018. We’ve updated it in 2025 for clarity and relevance, reflecting current practices while honoring their original perspective._
**If your PostgreSQL performance seems to be lagging, you’re not imagining things.**
It probably started out fine**.** You installed it, spun up a few apps, and everything just worked. But over time, queries got slower, load times crept up, and suddenly you’re fielding complaints or watching CPU usage spike for no obvious reason.
The truth is, PostgreSQL’s default settings aren’t built for performance. They’re built to be safe and generic, so the database works in as many environments as possible. That’s great for getting started, but not for running real workloads.
**Performance tuning helps you take control.** By adjusting key configuration settings, you can make PostgreSQL faster, more efficient, and better suited to the hardware and data it’s actually using.
This post covers the most important tuning areas to focus on. And if you’re starting to feel like constantly tweaking PostgreSQL parameters is more than you bargained for, we’ll talk about that too.
## What is PostgreSQL performance tuning?
Performance tuning is how you get PostgreSQL to respond the way you need it to. A fresh install is designed to work in a wide range of environments, which means it won’t be optimized for yours.
The goal is to improve efficiency and responsiveness by resolving bottlenecks and making better use of available resources. That usually includes a mix of configuration changes, query improvements, and smart database design choices.
Here are some of the most common areas teams focus on:
### Configuration tuning 
Settings in postgresql.conf can be adjusted to better match your hardware and workload. This includes memory parameters like shared_buffers and work_mem, I/O behavior, write-ahead logging, and concurrency controls. This post focuses on this area specifically.
### Query optimization
Slow queries are often the biggest cause of performance issues. Tools like EXPLAIN help you identify where they’re getting stuck so you can rewrite or reindex as needed.
### Index tuning
Choosing the right index types and keeping them maintained helps PostgreSQL find data faster. That might include B-tree, GIN, GiST, or Hash indexes, depending on the query patterns.
### Hardware optimization
PostgreSQL depends on the system it runs on. Fast storage, enough RAM, and strong CPU performance all matter, especially under heavy load.
### Monitoring and statistics
Tuning without visibility is guesswork. PostgreSQL provides internal stats, and tools like [Percona Monitoring and Management](https://www.percona.com/software/database-tools/percona-monitoring-and-management) (PMM) make it easier to track trends and confirm that changes are working.
### Schema design
The way your data is structured has a direct impact on performance. Good schema design includes choosing appropriate data types, partitioning large tables, and knowing when to normalize or denormalize.
### Connection pooling
PostgreSQL isn’t built to handle a large number of open connections directly. Tools like [PgBouncer](https://www.percona.com/blog/pgbouncer-for-postgresql-how-connection-pooling-solves-enterprise-slowdowns/) help manage those connections more efficiently.
### Replication and load balancing
When traffic grows, spreading read operations across replicas or balancing load across servers can help maintain performance.
![PostgreSQL Tuning](data:image/svg+xml,%3Csvg%20xmlns='http://www.w3.org/2000/svg'%20viewBox='0%200%201000%20161'%3E%3C/svg%3E)
## Why tuning your PostgreSQL database actually matters
You might not notice the impact of slow performance right away. **But your users do.**
When queries drag, pages hang, or background jobs take too long to finish, frustration builds fast. Small issues become bigger ones, and pretty soon, your team is spending way too much time chasing problems.
Performance tuning helps prevent that spiral. It’s how you keep PostgreSQL responsive under pressure, ready to grow with your data, and efficient enough to avoid wasting resources.
![](data:image/svg+xml,%3Csvg%20xmlns='http://www.w3.org/2000/svg'%20viewBox='0%200%2031%2031'%3E%3C/svg%3E)**It keeps your users happy:** Fast queries mean faster pages, quicker reports, and fewer complaints. A tuned database helps your application feel seamless and responsive.
**![](data:image/svg+xml,%3Csvg%20xmlns='http://www.w3.org/2000/svg'%20viewBox='0%200%2031%2031'%3E%3C/svg%3E)It supports more traffic without slowing down:** Better throughput means you can serve more users at once. Tuning helps your system handle higher loads without breaking a sweat.
**![](data:image/svg+xml,%3Csvg%20xmlns='http://www.w3.org/2000/svg'%20viewBox='0%200%2031%2031'%3E%3C/svg%3E)It scales with your business:** As data grows, performance often drops. A tuned database is better prepared to keep up without forcing a full redesign.
**![](data:image/svg+xml,%3Csvg%20xmlns='http://www.w3.org/2000/svg'%20viewBox='0%200%2031%2031'%3E%3C/svg%3E)It uses your hardware more efficiently:** You get more value from the CPUs, memory, and storage you’re already paying for. That adds up, especially in cloud environments where overprovisioning gets expensive.
**![](data:image/svg+xml,%3Csvg%20xmlns='http://www.w3.org/2000/svg'%20viewBox='0%200%2031%2031'%3E%3C/svg%3E)It keeps things stable:** A well-performing database is usually a healthy one. You’ll see fewer errors, fewer surprises, and a lot less downtime.  
  
**![](data:image/svg+xml,%3Csvg%20xmlns='http://www.w3.org/2000/svg'%20viewBox='0%200%2031%2031'%3E%3C/svg%3E)It gives you an edge:** Faster systems don’t just run better. They help your product stand out. Performance is a real competitive advantage, especially when users have options.
## The critical impact of queries on PostgreSQL performance
You’ve tweaked your config. You’ve bumped memory. Maybe you’ve even tuned WAL settings and checkpoints. 
But something still feels off.
If PostgreSQL is still slow after all that, there’s a good chance the problem isn’t in your settings. 
#### **_It’s in the queries._**
You expect performance tuning to give you a faster database, and it does… to a point. But a poorly written query can blow right through your tuning efforts and drag the system down anyway.
We’ve seen this happen more times than we can count. Everything looks fine at the system level, but a single query is chewing through CPU or locking up rows and causing a backlog.
Here’s what usually helps:
![PostgreSQL Query Tuning](data:image/svg+xml,%3Csvg%20xmlns='http://www.w3.org/2000/svg'%20viewBox='0%200%20500%20563'%3E%3C/svg%3E)
Query performance is where everything comes together. If your config is dialed in but queries are still inefficient, the database will always struggle to keep up.
**The good news?** Once you fix the queries, all your other tuning work starts to pay off.
## Key PostgreSQL parameters for performance tuning
Now that we’ve covered why performance can lag, let’s look at the settings that often have the biggest impact. These are the PostgreSQL parameters worth adjusting when you want to see real improvement.
### shared_buffer
If your PostgreSQL instance feels slow, this is often the first setting to look at.
By default, PostgreSQL barely uses memory. It leans on the operating system for caching, which means your database ends up working harder than it needs to. shared_buffers lets PostgreSQL use its own memory more efficiently by storing frequently accessed data in a dedicated cache.
In most default installs, this value is tiny (something like 128MB), which is fine for testing, but not nearly enough for production.
If you’re running a real workload, try setting shared_buffers to about 25 percent of total system RAM. From there, test and adjust. You’ll want to leave enough memory for the OS and other processes, but giving PostgreSQL more room to breathe here can make a noticeable difference.
Just keep in mind that on some systems, especially older versions of Windows, there are limits on how much shared memory you can allocate. So check before you scale it up too far.
testdb=# SHOW shared_buffers; shared_buffers ---------------- 128MB (1 row)
1 2 3 4 5 |  testdb=# SHOW shared_buffers; shared_buffers ---------------- 128MB (1row)  
---|---  
**Note:** Be careful, as some kernels do not allow a bigger value. In particular, in Windows, a higher value is not useful.
### wal_buffers
Every time data is written in PostgreSQL, it first goes into the Write-Ahead Log (WAL). Before those changes hit disk, they pass through wal_buffers. If this buffer is too small, writes get flushed more frequently, which can slow things down, especially under heavy write load.
By default, wal_buffers is set pretty low, often around 16MB. That might be fine for light traffic, but not for systems with lots of inserts, updates, or concurrent writers.
If you’re seeing write pressure or slow commit times, try increasing it to 64MB or 128MB. In some cases, going even higher helps, up to the size of one full WAL segment. Just like other tuning settings, it’s worth testing to see how your workload responds.
### effective_cache_size
This setting doesn’t change how much memory PostgreSQL uses, but it does influence how it thinks.
effective_cache_size is a rough estimate of the memory available for caching data, both inside PostgreSQL and from the operating system. The query planner uses this number to decide whether an index makes sense.
If you set it too low, PostgreSQL might assume the cache is too small and skip indexes that would actually help. If you set it too high, there’s not much risk, since this setting doesn’t reserve memory—it’s just a hint.
A good starting point is somewhere between 50 and 75 percent of your total system RAM. Just make sure it reflects reality, and you’ll help the planner make smarter choices.
### work_mem
If you’re noticing slow ORDER BY, DISTINCT, or hash joins, this setting is worth a look.
work_mem controls how much memory PostgreSQL can use for operations like sorting and hashing before it spills to disk. In-memory is always faster, so tuning this can have a big impact, especially for reporting queries or anything that processes a lot of rows.
The default is usually around 4MB, which is pretty conservative. Bumping it to 16MB, 32MB, or 64MB can make a difference, but there’s a catch. PostgreSQL can use this amount **per operation** , **per query** , **per user**. That adds up fast on a busy system.
For that reason, it’s often better to increase it cautiously or set it temporarily for a single session when you know a heavy query is coming. You’ll see the biggest impact in EXPLAIN ANALYZE plans when sorts or joins stop hitting disk and stay in memory.
testdb=# SET work_mem TO "2MB"; testdb=# EXPLAIN SELECT * FROM bar ORDER BY bar.b; QUERY PLAN ----------------------------------------------------------------------------------- Gather Merge (cost=509181.84..1706542.14 rows=10000116 width=24) Workers Planned: 4 -> Sort (cost=508181.79..514431.86 rows=2500029 width=24) Sort Key: b -> Parallel Seq Scan on bar (cost=0.00..88695.29 rows=2500029 width=24) (5 rows)
1 2 3 4 5 6 7 8 9 10 |  testdb=# SET work_mem TO "2MB"; testdb=# EXPLAIN SELECT * FROM bar ORDER BY bar.b; QUERY PLAN ----------------------------------------------------------------------------------- Gather Merge(cost=509181.84..1706542.14rows=10000116width=24) Workers Planned:4 ->Sort(cost=508181.79..514431.86rows=2500029width=24) Sort Key:b ->Parallel Seq Scan on bar(cost=0.00..88695.29rows=2500029width=24) (5rows)  
---|---  
The initial query’s sort node has an estimated cost of 514431.86. A cost is an arbitrary unit of computation. For the above query, we have a work_mem of only 2 MB. For testing purposes, let’s increase this to 256MB and see if there is any impact on cost.
testdb=# SET work_mem TO "256MB"; testdb=# EXPLAIN SELECT * FROM bar ORDER BY bar.b; QUERY PLAN ----------------------------------------------------------------------------------- Gather Merge (cost=355367.34..1552727.64 rows=10000116 width=24) Workers Planned: 4 -> Sort (cost=354367.29..360617.36 rows=2500029 width=24) Sort Key: b -> Parallel Seq Scan on bar (cost=0.00..88695.29 rows=2500029 width=24)
1 2 3 4 5 6 7 8 9 |  testdb=# SET work_mem TO "256MB"; testdb=# EXPLAIN SELECT * FROM bar ORDER BY bar.b; QUERY PLAN ----------------------------------------------------------------------------------- Gather Merge(cost=355367.34..1552727.64rows=10000116width=24) Workers Planned:4 ->Sort(cost=354367.29..360617.36rows=2500029width=24) Sort Key:b ->Parallel Seq Scan on bar(cost=0.00..88695.29rows=2500029width=24)  
---|---  
The query cost is reduced to 360617.36 from 514431.86 — a 30% reduction.
### maintenance_work_mem
This setting doesn’t affect day-to-day query performance, but it plays a big role in how fast PostgreSQL can handle maintenance tasks.
When you run a VACUUM, build an index, or restore from a backup, PostgreSQL uses maintenance_work_mem to decide how much memory it can use for the job. If the value is too low, these operations take longer than they need to, especially on large tables.
The default is usually around 64MB, which isn’t much. If you’ve got the RAM to spare, increasing it to 256MB, 512MB, or even more can speed things up significantly. Since these tasks often run during off-peak hours, it’s usually safe to give them more room to work.
postgres=# CHECKPOINT; postgres=# SET maintenance_work_mem to '10MB'; postgres=# CREATE INDEX foo_idx ON foo (c); CREATE INDEX Time: 170091.371 ms (02:50.091) – postgres=# CHECKPOINT; postgres=# set maintenance_work_mem to '256MB'; postgres=# CREATE INDEX foo_idx ON foo (c); CREATE INDEX Time: 111274.903 ms (01:51.275)
1 2 3 4 5 6 7 8 9 10 11 12 13 |  postgres=# CHECKPOINT; postgres=# SET maintenance_work_mem to '10MB'; postgres=# CREATE INDEX foo_idx ON foo (c); CREATE INDEX Time:170091.371ms(02:50.091) – postgres=# CHECKPOINT; postgres=# set maintenance_work_mem to '256MB'; postgres=# CREATE INDEX foo_idx ON foo (c); CREATE INDEX Time:111274.903ms(01:51.275)  
---|---  
The index creation time is 170091.371ms when maintenance_work_mem is set to only 10MB, but that is reduced to 111274.903 ms when we increase maintenance_work_mem setting to 256MB.
### synchronous_commit
This setting decides how careful PostgreSQL is when writing data. More specifically, it controls whether a transaction is fully written to disk before PostgreSQL tells the client, “You’re good.”
By default, it’s set to on, which means PostgreSQL waits for confirmation that everything has been flushed. This is the safest option and ensures durability.
You can make it faster by setting it to off, which skips the disk flush and returns success sooner. But there’s a trade-off. If the system crashes before the data is actually written, you can lose those transactions.
Unless your application can afford to lose a small amount of recent data in a worst-case scenario, it’s best to leave this on. That said, if you’re doing bulk inserts or non-critical writes, you might choose to relax it temporarily to get a performance boost.
Just be sure you understand what you’re giving up before you flip the switch.
### checkpoint_timeout, checkpoint_completion_target
PostgreSQL uses checkpoints to flush dirty data from memory to disk. This is necessary to keep data safe, but if checkpoints happen too often or all at once, they can create massive I/O spikes that slow everything down.
Here’s how to manage that.
  * **checkpoint_timeout** sets how often checkpoints happen. The default is every five minutes, which is a bit aggressive for most systems. Bumping it to 15 or even 30 minutes gives the system more breathing room and reduces write pressure, but it also means longer crash recovery times if something goes wrong. You’ll want to find the right balance based on how long you’re comfortable waiting during recovery.
  * **checkpoint_completion_target** controls how evenly the checkpoint writes are spread out over that time window. The default used to be 0.5, meaning PostgreSQL would try to finish checkpoints halfway through the interval. A more common setting now is 0.9, which helps avoid sudden write storms by stretching the work across more time.


Tuning these together helps reduce performance dips from I/O spikes. If your disk usage suddenly jumps or the system feels sluggish at regular intervals, it’s worth reviewing both settings.
### When PostgreSQL performance tuning isn’t enough
You’ve seen how much impact the right tuning can have, but configuration is only part of the story. If your team is spending more and more time just keeping PostgreSQL stable, the problem probably runs deeper than a few settings.
So here’s the real question: 
**_Is PostgreSQL becoming more work than you expected?_**
If the answer is yes, don’t fret. Many teams hit this wall. What started as a flexible, open source choice turns into a patchwork of tuning, tooling, and ongoing maintenance that eats away at your time and focus.
That’s why we put together a guide that looks at the bigger picture: what it really takes to run PostgreSQL at scale, and whether your team has the time, expertise, and resources to manage it properly over the long term.
[![](data:image/svg+xml,%3Csvg%20xmlns='http://www.w3.org/2000/svg'%20viewBox='0%200%20800%20150'%3E%3C/svg%3E)](https://hubs.ly/Q03j7phM0)
It’s practical, direct, and written for teams like yours. If you’re starting to feel the strain, this will help you figure out what to do next.
### PostgreSQL performance tuning FAQs
**Q1: What is the most important parameter for PostgreSQL performance tuning?**  
**A:** While it depends on the workload, shared_buffers is often considered the most impactful single parameter, as it controls the size of PostgreSQL’s main memory cache for data pages. Correctly sizing it (often 25% of system RAM as a starting point) is crucial.
**Q2: How can I improve slow query performance in PostgreSQL?**  
**A:** Improving slow queries involves **query optimization**. Use EXPLAIN ANALYZE to understand the query plan, then focus on **index tuning** (adding missing indexes, removing unused ones, choosing the right index type), rewriting the query logic for efficiency, ensuring statistics are up-to-date (ANALYZE), and potentially adjusting work_mem for large sorts or joins.
**Q3: What does work_mem control in PostgreSQL?**  
**A:** work_mem sets the amount of memory PostgreSQL can use for internal operations like sorting (ORDER BY, window functions), hash joins, and hash aggregation before resorting to slower temporary disk files. Tuning it can significantly speed up complex queries but must be done cautiously due to its per-operation allocation.
**Q4: Why should I tune checkpoint parameters ( checkpoint_timeout, checkpoint_completion_target)?**  
**A:** Checkpoints flush dirty data buffers to disk. Tuning these parameters helps manage the I/O impact. Increasing checkpoint_timeout reduces checkpoint frequency (less I/O disruption, longer recovery time). Increasing checkpoint_completion_target spreads the I/O over a longer duration within the timeout period, reducing I/O spikes.
**Q5: What tools can help with PostgreSQL performance tuning and monitoring?**  
**A:** Built-in tools like EXPLAIN, pg_stat_statements, and various statistics views are essential. External monitoring tools like **Percona Monitoring and Management (PMM)** provide comprehensive dashboards and query analytics. Benchmarking tools like pgbench or sysbench help test the impact of tuning changes.
### About the Author
![](data:image/svg+xml,%3Csvg%20xmlns='http://www.w3.org/2000/svg'%20viewBox='0%200%201%201'%3E%3C/svg%3E) [Ibrar Ahmed](https://www.percona.com/blog/author/ibrar-ahmed/)  
Joined Percona in the month of July 2018. Before joining Percona, Ibrar worked as a Senior Database Architect at EnterpriseDB for 10 Years. Ibrar has 18 years of software development experience. Ibrar authored multiple books on PostgreSQL. 
### Share This Post!
[](https://twitter.com/intent/tweet?text=PostgreSQL%20Performance%20Tuning%20Guide:%20Settings%20That%20Make%20a%20Difference&url=https%3A%2F%2Fwww.percona.com%2Fblog%2Ftuning-postgresql-database-parameters-to-optimize-performance%2F)[](https://www.facebook.com/sharer/sharer.php?u=https%3A%2F%2Fwww.percona.com%2Fblog%2Ftuning-postgresql-database-parameters-to-optimize-performance%2F)[](https://www.linkedin.com/shareArticle?mini=true&url=https%3A%2F%2Fwww.percona.com%2Fblog%2Ftuning-postgresql-database-parameters-to-optimize-performance%2F&title=PostgreSQL%20Performance%20Tuning%20Guide:%20Settings%20That%20Make%20a%20Difference)
Subscribe
Notify of 
new follow-up comments new replies to my comments
![guest](data:image/svg+xml,%3Csvg%20xmlns='http://www.w3.org/2000/svg'%20viewBox='0%200%2056%2056'%3E%3C/svg%3E)
Label
  

[](about:blank)
{} [+]
Name*
Email*
Website
Δ
![guest](data:image/svg+xml,%3Csvg%20xmlns='http://www.w3.org/2000/svg'%20viewBox='0%200%2056%2056'%3E%3C/svg%3E)
Label
{} [+]
Name*
Email*
Website
Δ
4 Comments 
Oldest
Newest Most Voted
View all comments
![fpuga](data:image/svg+xml,%3Csvg%20xmlns='http://www.w3.org/2000/svg'%20viewBox='0%200%2064%2064'%3E%3C/svg%3E)
[fpuga](http://conocimientoabierto.es)
I understad that most of this suggestions like using 25% of RAM for `shared_buffer` is for servers that are only running PostgreSQL and not for servers that also run a web server or other services. Is this true?
0
Reply
[![Ibrar Ahmed](data:image/svg+xml,%3Csvg%20xmlns='http://www.w3.org/2000/svg'%20viewBox='0%200%2064%2064'%3E%3C/svg%3E)](https://www.percona.com/blog/author/ibrar-ahmed/)
[Ibrar Ahmed](https://www.percona.com/blog/author/ibrar-ahmed/)
Author
[ fpuga ](https://www.percona.com/blog/tuning-postgresql-database-parameters-to-optimize-performance/#comment-10969640)
Most of the tuning advices are for the dedicated “database” server. In case of shared system where you are running database and some other server on a single machine need to be tuned accordingly.
0
Reply
![Glyn](data:image/svg+xml,%3Csvg%20xmlns='http://www.w3.org/2000/svg'%20viewBox='0%200%2064%2064'%3E%3C/svg%3E)
[Glyn](https://blog.8kb.co.uk)
That shared_buffer advice isn’t great, especially if applied to modern systems with large volumes of ram.
Generally there’s a tipping point, and it’s much lower than you’d think. A better approach is to use pg_buffercache extension to inspect the system under typical load and tune down.
0
Reply
![joshuamills235](data:image/svg+xml,%3Csvg%20xmlns='http://www.w3.org/2000/svg'%20viewBox='0%200%2064%2064'%3E%3C/svg%3E)
[joshuamills235](https://www.autoupgrades.co.nz/)
In this post you are very thoughtful . I am very happy to read this post. It’s so motivational post for me. I would like to very thankful for this best and most important information. For more info :-https://www.autoupgrades.co.nz/
0
Reply
## Stay up to date with the Percona Blog
Email*
![right-img](data:image/svg+xml,%3Csvg%20xmlns='http://www.w3.org/2000/svg'%20viewBox='0%200%201%201'%3E%3C/svg%3E)
## Related Blog Articles
### RECOMMENDED ARTICLES
[ ![JavaScript Stored Routines in Percona Server for MySQL: A New Era for Database Programmability](data:image/svg+xml,%3Csvg%20xmlns='http://www.w3.org/2000/svg'%20viewBox='0%200%201216%20681'%3E%3C/svg%3E) ](https://www.percona.com/blog/javascript-stored-routines-in-percona-server-for-mysql-a-new-era-for-database-programmability/)
January 5, 2026
[Dennis Kittrell](https://www.percona.com/blog/author/dennis-kittrell)
## [JavaScript Stored Routines in Percona Server for MySQL: A New Era for Database Programmability ](https://www.percona.com/blog/javascript-stored-routines-in-percona-server-for-mysql-a-new-era-for-database-programmability/)
[Insight for DBAs](https://www.percona.com/blog/category/dba-insight/) [MySQL](https://www.percona.com/blog/category/mysql/) [Percona Software](https://www.percona.com/blog/category/percona-software/)
[ ![Running Databases on Kubernetes: A Practical Guide to Risks, Benefits, and Best Practices](data:image/svg+xml,%3Csvg%20xmlns='http://www.w3.org/2000/svg'%20viewBox='0%200%201216%20681'%3E%3C/svg%3E) ](https://www.percona.com/blog/running-databases-on-kubernetes-a-practical-guide-to-risks-benefits-and-best-practices/)
January 2, 2026
[David Quilty](https://www.percona.com/blog/author/david-quilty)
## [Running Databases on Kubernetes: A Practical Guide to Risks, Benefits, and Best Practices ](https://www.percona.com/blog/running-databases-on-kubernetes-a-practical-guide-to-risks-benefits-and-best-practices/)
[Cloud](https://www.percona.com/blog/category/cloud/) [Insight for DBAs](https://www.percona.com/blog/category/dba-insight/) [Open Source](https://www.percona.com/blog/category/open-source/)
[ ![Building a Multi-Cloud Strategy: Cut Costs, Improve Resilience, and Avoid Lock-In](data:image/svg+xml,%3Csvg%20xmlns='http://www.w3.org/2000/svg'%20viewBox='0%200%201216%20681'%3E%3C/svg%3E) ](https://www.percona.com/blog/building-a-multi-cloud-strategy-cut-costs-improve-resilience-and-avoid-lock-in/)
December 31, 2025
[David Quilty](https://www.percona.com/blog/author/david-quilty)
## [Building a Multi-Cloud Strategy: Cut Costs, Improve Resilience, and Avoid Lock-In ](https://www.percona.com/blog/building-a-multi-cloud-strategy-cut-costs-improve-resilience-and-avoid-lock-in/)
[Cloud](https://www.percona.com/blog/category/cloud/) [Insight for DBAs](https://www.percona.com/blog/category/dba-insight/) [Open Source](https://www.percona.com/blog/category/open-source/)
### MOST POPULAR ARTICLES
[ ![Deploy Django on Kubernetes With Percona Operator for PostgreSQL](data:image/svg+xml,%3Csvg%20xmlns='http://www.w3.org/2000/svg'%20viewBox='0%200%201024%201024'%3E%3C/svg%3E) ](https://www.percona.com/blog/deploy-django-on-kubernetes-with-percona-operator-for-postgresql/)
June 20, 2023
[Sergey Pronin](https://www.percona.com/blog/author/sergey-pronin)
## [Deploy Django on Kubernetes With Percona Operator for PostgreSQL ](https://www.percona.com/blog/deploy-django-on-kubernetes-with-percona-operator-for-postgresql/)
[Cloud](https://www.percona.com/blog/category/cloud/) [Insight for Developers](https://www.percona.com/blog/category/developer-insight/) [Percona Software](https://www.percona.com/blog/category/percona-software/) [PostgreSQL](https://www.percona.com/blog/category/postgresql/)
[ ![MySQL Performance Tuning: Maximizing Database Efficiency and Speed](data:image/svg+xml,%3Csvg%20xmlns='http://www.w3.org/2000/svg'%20viewBox='0%200%201500%201125'%3E%3C/svg%3E) ](https://www.percona.com/blog/mysql-101-parameters-to-tune-for-mysql-performance/)
February 1, 2025
[Brian Sumpter](https://www.percona.com/blog/author/brian-sumpter)
## [MySQL Performance Tuning: Maximizing Database Efficiency and Speed ](https://www.percona.com/blog/mysql-101-parameters-to-tune-for-mysql-performance/)
[Insight for DBAs](https://www.percona.com/blog/category/dba-insight/) [Monitoring](https://www.percona.com/blog/category/monitoring/) [MySQL](https://www.percona.com/blog/category/mysql/)
[ ![The Ultimate Guide to Open Source Databases](data:image/svg+xml,%3Csvg%20xmlns='http://www.w3.org/2000/svg'%20viewBox='0%200%201280%20721'%3E%3C/svg%3E) ](https://www.percona.com/blog/ultimate-guide-open-source-databases)
March 30, 2023
[Pete Scott](https://www.percona.com/blog/author/pete-scott)
## [The Ultimate Guide to Open Source Databases ](https://www.percona.com/blog/ultimate-guide-open-source-databases)
[Insight for DBAs](https://www.percona.com/blog/category/dba-insight/)
## Ready to get started?
Subscribe to our newsletter for updates on enterprise-grade open source software and tools to keep your business running better.
  

GA Source
Email*
First name
Last name
Company name
By submitting my information I agree that Percona may use my personal data in sending communication to me about Percona services. I understand that I can unsubscribe from the communication at any time in accordance with the [Percona Privacy Policy](https://www.percona.com/20180524-privacy-policy). This site is protected by reCAPTCHA and the Google [Privacy Policy](https://policies.google.com/privacy) and [Terms of Service](https://policies.google.com/terms) apply.
## **Follow us for updates**
  * [Twitter](https://twitter.com/percona)
  * [Facebook](https://www.facebook.com/Percona?fref=ts)
  * [LinkedIn](https://www.linkedin.com/company/percona)
  * [Instagram](https://www.instagram.com/percona/)
  * [GitHub](https://github.com/percona)


#### Featured
  * [MySQL 5.7 End of Life](https://www.percona.com/navigating-mysql-5-7-end-of-life)
  * Learn
  * [Downloads](https://www.percona.com/downloads)
  * [Resources](https://www.percona.com/resources)
  * [Docs](https://docs.percona.com/)


#### Products
  * [MySQL](https://www.percona.com/mysql)
    * [Distribution for MySQL](https://www.percona.com/software/mysql-database)
    * [Server for MySQL](https://www.percona.com/software/mysql-database/percona-server)
    * [XtraDB Cluster](https://www.percona.com/software/mysql-database/percona-xtradb-cluster)
    * [XtraBackup for MySQL Databases](https://www.percona.com/software/mysql-database/percona-xtrabackup)
  * [MongoDB](https://www.percona.com/mongodb)
    * [Distribution for MongoDB](https://www.percona.com/software/mongodb)
    * [Server for MongoDB](https://www.percona.com/software/mongodb/percona-server-for-mongodb)
    * [Backup for MongoDB](https://www.percona.com/software/mongodb/percona-backup-for-mongodb)
  * [PostgreSQL](https://www.percona.com/postgresql)
    * [Software](https://www.percona.com/postgresql/software)
    * [Support and Services](https://www.percona.com/postgresql/support-and-services)
  * [Cloud Native](https://www.percona.com/cloud-native)
  * [Monitoring](https://www.percona.com/software/database-tools/percona-monitoring-and-management)
  * [Percona Toolkit](https://www.percona.com/software/database-tools/percona-toolkit)


#### Services
  * [Support](https://www.percona.com/services/support)
  * [Managed Services](https://www.percona.com/services/managed-services)
  * [Consulting](https://www.percona.com/services/consulting)
  * [Policies](https://www.percona.com/services/policies)
  * [Training](https://www.percona.com/training)


#### Use Cases
  * [Emergency Support](https://www.percona.com/services/emergency-support)
  * [High-Traffic Events](https://www.percona.com/services/high-traffic)
  * [Performance Tuning](https://www.percona.com/services/database-performance)
  * [Migrations](https://www.percona.com/services/open-source-migration)
  * [Upgrades](https://www.percona.com/services/open-source-upgrade)
  * [Security](https://www.percona.com/services/database-security)


#### Discover
  * [Blog](https://www.percona.com/blog/)
  * [Community](https://percona.community/)
  * [Percona Community Forum](https://forums.percona.com/)
  * [Events](https://www.percona.com/events)


#### About
  * [About Percona](https://www.percona.com/about)
  * [Partners](https://www.percona.com/about/partners)
  * [In The News](https://www.percona.com/about/in-the-news)
  * [Careers](https://www.percona.com/about/careers)


  * [Terms of Use](https://www.percona.com/legal/platform-terms-of-service)
  * [Privacy](https://www.percona.com/privacy-policy)
  * [Copyright](https://www.percona.com/copyright-policy)
  * [Legal](https://www.percona.com/legal)
  * [Security Center](https://www.percona.com/legal/percona-security-and-data-privacy-practices)


MySQL, PostgreSQL, InnoDB, MariaDB, MongoDB and Kubernetes are trademarks for their respective owners.
Copyright © 2006-2026 Percona LLC.
wpDiscuz
Insert
[](javascript:; "Close")[](javascript:; "Next")[](javascript:; "Previous")
