---
tags: [concept, day1, compute]
docs: https://docs.snowflake.com/en/user-guide/performance-query-warehouse-cache
---
# Warehouse Cache

**In one sentence:** The warehouse cache keeps the table data a running warehouse has already read on its local storage, so later queries that need the same micro-partitions skip the trip to cloud storage.

**Why it matters:** It is the reason a longer auto-suspend can make BI faster and cheaper at once, and the reason the first query after a resume is the slow one.

**Coming from Hadoop:** The OS page cache on a DataNode or Spark's cached RDD, but managed by Snowflake and shared by every query on that warehouse. The analogy breaks because the cache belongs to the warehouse, not the data: suspend the warehouse and the cache is gone, while the data is untouched (see [[Hadoop to Snowflake Rosetta Stone]])

## How it works

A [[Virtual Warehouse]] reads micro-partition columns from the [[Database Storage Layer]] and keeps them on its nodes' local disk (SSD). While the warehouse keeps running, a query that needs some of those columns reads them locally. Query Profile shows this as the share of *bytes scanned from cache* against *bytes scanned from remote storage*.

Lifetime and limits:

- Kept **as long as the warehouse runs**. Dropped when the warehouse **suspends**.
- **Downsizing** drops the part of the cache held by the removed nodes. Upsizing keeps the existing cache and adds empty nodes.
- Bounded by the local disk of the warehouse; a bigger warehouse has a bigger cache.
- Shared by every user and query on that warehouse; private to that warehouse.

This is why [[Auto-suspend and Auto-resume]] settings are a performance choice, not just a cost choice: a BI warehouse suspended after 60 seconds re-reads everything from cloud storage on each wake-up, while one left running for 10 minutes serves the dashboard refresh from local disk.

## Gotchas / exam traps

- Dropped on suspend. A warehouse that resumes is a cold warehouse.
- Holds table data, not results. Same query twice on a warm warehouse: the second run is served by the result cache before the warehouse cache even matters.
- Per warehouse. Two warehouses reading the same table each build their own cache.

## Related

- [[Caching]]
- [[Virtual Warehouse]]
- [[Auto-suspend and Auto-resume]]
- [[Result Cache]]
- [[Database Storage Layer]]

## Explain it to a teammate (fill in yourself)

> 
