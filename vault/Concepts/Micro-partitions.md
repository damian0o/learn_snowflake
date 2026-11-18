---
tags: [concept, day1, storage]
docs: https://docs.snowflake.com/en/user-guide/tables-clustering-micropartitions
---
# Micro-partitions

**In one sentence:** A micro-partition is Snowflake's unit of storage: a contiguous, immutable, columnar block holding 50 to 500 MB of uncompressed data plus metadata about every column in it.

**Why it matters:** Micro-partitions are the reason Snowflake can skip most of a table without indexes, and the reason you do not design partitions any more. Understanding them explains query speed, storage cost and clustering.

**Coming from Hadoop:** Hive partitions, but automatic, invisible and far more granular. In Hive you chose `PARTITIONED BY (dt)` and got one directory per day; filters on anything but `dt` scanned everything. Snowflake splits every table into micro-partitions by itself, in load order, and keeps min/max for **every** column, so pruning works on any well-ordered column. The analogy breaks because you cannot name, list or target a micro-partition, and you never run `MSCK REPAIR` (see [[Hadoop to Snowflake Rosetta Stone]])

## How it works

Every table, without exception, is stored as micro-partitions:

- **Size:** 50 to 500 MB of uncompressed data each (much smaller on disk after columnar compression).
- **Layout:** columnar inside the partition, so a query reading two columns of twenty touches only those two.
- **Creation:** automatic, as data is loaded, following the order the rows arrive in. Nothing to declare.
- **Immutable:** never modified in place. DML writes new micro-partitions; the old ones are kept for Time Travel and Fail-safe, then purged.
- **Metadata per partition, per column:** the range of values (min and max), the number of distinct values, null counts, and more. This lives in [[Cloud Services Layer]].

That metadata is what makes [[Query Pruning]] possible: a `WHERE order_date = '2026-03-01'` touches only partitions whose `order_date` range includes that day. Because data usually arrives in time order, date columns prune well by default. Columns whose values are scattered across all partitions do not prune; for very large tables you can fix that with [[Clustering Keys]].

`SYSTEM$CLUSTERING_INFORMATION('table', '(col)')` reports how well a column's values are separated across micro-partitions (its clustering depth).

## Gotchas / exam traps

- Micro-partition size is quoted uncompressed: 50 to 500 MB. On disk they are smaller.
- They are not Hive partitions. There is no `PARTITION BY` clause for standard tables; micro-partitioning is automatic.
- Rewriting rows (`UPDATE`, `DELETE`, `MERGE`) creates new micro-partitions and keeps the old ones for a while, which costs storage.

## Related

- [[Database Storage Layer]]
- [[Query Pruning]]
- [[Clustering Keys]]
- [[Metadata Cache]]
- [[Cloud Services Layer]]

## Explain it to a teammate (fill in yourself)

> 
