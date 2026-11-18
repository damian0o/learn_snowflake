---
tags: [concept, day1, compute]
docs: https://docs.snowflake.com/en/user-guide/tables-clustering-micropartitions
---
# Metadata Cache

**In one sentence:** The metadata cache is the statistics Cloud Services keeps about every table and micro-partition, which lets Snowflake answer some queries and prune most others without touching a warehouse.

**Why it matters:** It is why COUNT(*) on a huge table is instant and free, why pruning costs nothing, and why SHOW and DESCRIBE never wait for a warehouse.

**Coming from Hadoop:** The Hive Metastore knew your tables' schemas and partition lists but nothing about their contents; row counts needed `ANALYZE TABLE` and were stale by lunch. The analogy breaks because Snowflake's statistics are written with the data itself, on every load and every DML, so they are never stale (see [[Hadoop to Snowflake Rosetta Stone]])

## How it works

Every [[Micro-partitions|micro-partition]] carries metadata maintained by [[Cloud Services Layer]]: row count, and for each column the minimum and maximum, the number of distinct values, the null count, and more. Because the metadata is updated as part of every write, it is always exact.

What it does for you:

- **Answers whole-table aggregates without compute.** `SELECT COUNT(*) FROM t`, `SELECT MIN(order_date), MAX(order_date) FROM t` can be served from metadata alone for most data types; the warehouse can stay suspended and no credits are spent. Add a `WHERE` or a `GROUP BY` and the query runs normally.
- **Drives [[Query Pruning]].** The optimizer compares predicates with per-partition min/max to decide which partitions to read.
- **Serves `SHOW` and `DESCRIBE`.** Object listings and schemas come from metadata, never from a warehouse.

The docs do not name this a "cache"; the term comes from training material and the exam. The behaviour is what matters: metadata answers come from Cloud Services, instantly, without a warehouse. Try it on Day 1: suspend your warehouse and run `COUNT(*)` on a sample table.

## Gotchas / exam traps

- `COUNT(*)`, `MIN` and `MAX` on a whole table need no warehouse. Add a filter and they do.
- Metadata is never stale; there is no `ANALYZE` to run.
- Lives in Cloud Services next to the result cache, not on the warehouse.

## Related

- [[Caching]]
- [[Cloud Services Layer]]
- [[Micro-partitions]]
- [[Query Pruning]]
- [[Result Cache]]

## Explain it to a teammate (fill in yourself)

> 
