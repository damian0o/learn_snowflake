---
tags: [migration, day1]
---
# Hadoop to Snowflake Rosetta Stone

One row per concept: the Cloudera-world thing you know, the Snowflake thing that replaces it, and the place where the analogy stops being true. Use the bridge to get oriented, then let it go; every row's third column is a habit to unlearn.

## Day 1

| Cloudera (Hadoop, HDFS, Hive, Spark) | Snowflake | Where it breaks | Note |
|---|---|---|---|
| HDFS (the distributed file system) | [[Database Storage Layer]] | You cannot list, copy or read the files; only SQL reaches the data | One copy, every warehouse reads it |
| Parquet / ORC files you laid out | [[Micro-partitions]] | Snowflake picks size, compression and ordering; you cannot target a partition | 50 to 500 MB uncompressed, columnar, immutable |
| Hive partitions and bucketing (`PARTITIONED BY dt`) | [[Clustering Keys]] and [[Query Pruning]] | Pruning is automatic on every column; clustering is a tuning step for multi-TB tables, not a design step | No `MSCK REPAIR`, no directory layout |
| YARN queue plus Spark executors | [[Virtual Warehouse]] | A warehouse holds no data, so you can create, resize or drop one in seconds | One per workload is the norm |
| Cluster sizing, `spark.executor.instances` | [[Warehouse Sizes and Credits]] | Linear public pricing: each size doubles nodes and credits | XS = 1 credit per hour |
| Keeping the cluster warm overnight | [[Auto-suspend and Auto-resume]] | Nothing in Hadoop did this; idle Snowflake compute costs zero | Default suspend 600 s; suspend drops the warehouse cache |
| Adding nodes to the cluster | [[Scaling Up vs Scaling Out]] | Both are one `ALTER`; scale out can be automatic | Up = bigger size for one heavy query; out = more clusters for concurrency |
| Raising a YARN queue's capacity at peak | [[Multi-cluster Warehouse]] | Extra clusters are identical copies; queries are routed, not split | Enterprise edition; Standard vs Economy policy |
| Hive Metastore, Ranger, the YARN ResourceManager | [[Cloud Services Layer]] | Also holds per-partition statistics and query results; can answer some queries alone | Charged only above 10 % of warehouse credits |
| `ANALYZE TABLE` statistics in the Metastore | [[Metadata Cache]] | Statistics are written with every load, never stale, and answer `COUNT(*)` with no compute | Lives in Cloud Services |
| Re-running the same Hive query (always recomputed) | [[Result Cache]] | No equivalent existed; identical SQL on unchanged data is free for 24 h | Exact text match, up to 31 days with reuse |
| Spark `.cache()` and the DataNode page cache | [[Warehouse Cache]] | Belongs to the warehouse, not the job; dropped on suspend | Why the first query after resume is slow |
| Hue, Cloudera Manager UI | [[Snowsight]] | Query Profile shows pruning, cache hits and spilling for every query | Admin → Warehouses, Monitoring → Query History |
| CDH / CDP licence tiers | [[Snowflake Editions]] | The edition changes what SQL is allowed (multi-cluster, 90-day Time Travel) | Standard, Enterprise, Business Critical, VPS |
| Your on-premises data centre | [[Cloud Providers and Regions]] | One account lives in one region of one cloud; crossing regions costs egress | AWS, Azure, Google Cloud |
| One Cloudera Manager, several clusters | [[Organizations and Accounts]] | Accounts can share data without copying and replicate with one command | ORGADMIN above, ACCOUNTADMIN inside |
| Node-hours and rack capital | [[Credits and Billing]] | Seconds of compute, compressed bytes stored, bytes leaving the region, each metered separately | Idle costs almost nothing |
| The whole Cloudera platform | [[What Snowflake Is]] | Nothing to install or patch; storage and compute billed separately | SaaS, one copy of data, elastic compute |
| Hadoop's three concerns on one set of nodes | [[Three-Layer Architecture]] | Layers run on separate infrastructure and scale independently | Storage, Compute, Cloud Services |
| Data-local processing (code to data) | [[Compute Layer]] | Compute reads shared cloud storage; pruning and caches make that fast | Many warehouses, one copy of data |

## Rows added on Day 2 and Day 3

(filled in with increments 2 and 3: Hive databases and tables, external tables and stages, Sqoop and Flume, Oozie, Ranger and Sentry, HDFS snapshots, Hive UDFs, and the naming habits that need translating)

## Related

- [[00 Home]]
- [[Day 1]]
- [[Memory Techniques]]
