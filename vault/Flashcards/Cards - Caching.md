---
tags: [flashcards/day1, cards]
---
# Cards - Caching

Cards for: [[Caching]], [[Result Cache]], [[Warehouse Cache]], [[Metadata Cache]]

Name Snowflake's three caches and where each lives.::Result cache in Cloud Services; warehouse cache on the warehouse's local disk; metadata cache in Cloud Services. [[Caching]]

Which of the three caches survives a warehouse suspend?::The result cache and the metadata cache. Only the warehouse cache is dropped. [[Caching]]

The result cache keeps a result for ==24== hours after its last use, extended on each reuse, up to ==31== days from first execution. [[Result Cache]]

List the conditions for result cache reuse.
?
Identical SQL text; underlying data unchanged; the role has the needed privileges; no non-deterministic or external functions; USE_CACHED_RESULT is TRUE. [[Result Cache]]

Does `SELECT *` reuse the cached result of `select *`?::No. The text must match exactly, including case, whitespace and aliases. [[Result Cache]]

How do you switch the result cache off for a benchmark?::`ALTER SESSION SET USE_CACHED_RESULT = FALSE;` [[Result Cache]]

Does serving a result from the result cache need a running warehouse?::No. It is served by Cloud Services; Query Profile shows a single node, QUERY RESULT REUSE. [[Result Cache]]

What does the warehouse cache hold?::Raw table data (micro-partition columns) read by recent queries, on the warehouse's local SSD, shared by every query on that warehouse. [[Warehouse Cache]]

When is the warehouse cache dropped?::On suspend, and the part held by removed nodes on downsizing. Upsizing keeps it. [[Warehouse Cache]]

Which queries can the metadata cache answer with no warehouse?::Whole-table `COUNT(*)`, `MIN`, `MAX`, plus `SHOW` and `DESCRIBE`. Add a WHERE or GROUP BY and the query needs a warehouse. [[Metadata Cache]]

Why are Snowflake's table statistics never stale?::They are written with the data on every load and DML, as micro-partition metadata. There is no ANALYZE to run. [[Metadata Cache]]

Coming from Hadoop: which Snowflake cache has no Hadoop equivalent at all?::The result cache. Hive and Impala recomputed every query. [[Result Cache]]
