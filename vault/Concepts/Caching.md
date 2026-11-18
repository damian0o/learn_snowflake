---
tags: [concept, day1, compute]
docs: https://docs.snowflake.com/en/user-guide/querying-persisted-results
---
# Caching

**In one sentence:** Snowflake has three caches at three layers: the result cache in Cloud Services, the warehouse cache on each warehouse's local storage, and the metadata cache in Cloud Services.

**Why it matters:** The caches explain why identical queries become free, why a warehouse that just woke up feels slow, and why COUNT(*) on a billion rows returns instantly. Each one has a different lifetime and a different owner.

**Coming from Hadoop:** Spark's `.cache()` and the OS page cache on DataNodes were the only caches you had, both per job and per node. The analogy breaks because two of Snowflake's three caches live outside any compute you pay for, and all three are automatic (see [[Hadoop to Snowflake Rosetta Stone]])

## How it works

| Cache | Lives in | Holds | Lifetime | Note |
|-------|----------|-------|----------|------|
| [[Result Cache]] | [[Cloud Services Layer]] | the full result of a query | 24 h, extended on each reuse, up to 31 days | identical SQL text, unchanged data, needs no warehouse |
| [[Warehouse Cache]] | each [[Virtual Warehouse]], local disk | raw table data (micro-partition columns) read by recent queries | while the warehouse runs; dropped on suspend | why the second query on a warm warehouse is faster |
| [[Metadata Cache]] | [[Cloud Services Layer]] | micro-partition statistics: row counts, min, max, distinct counts | always current, maintained on every write | answers `COUNT(*)`, `MIN`, `MAX` on whole tables and drives pruning |

A query is checked against the caches in this order: can the result cache answer it (same text, same data, allowed)? If not, can metadata alone answer it? If not, run it on the warehouse, where the warehouse cache may spare a trip to cloud storage for some partitions.

You can turn result reuse off for a session with `ALTER SESSION SET USE_CACHED_RESULT = FALSE`, which is how you benchmark honestly.

## Gotchas / exam traps

- Three caches, three places: result cache and metadata cache in Cloud Services, warehouse cache on the warehouse.
- Only the warehouse cache depends on the warehouse being up. Suspending drops it; the other two survive.
- Benchmarks that ignore caching are wrong twice: the second run hits the result cache, and the warm warehouse hides scan time.

## Related

- [[Result Cache]]
- [[Warehouse Cache]]
- [[Metadata Cache]]
- [[Cloud Services Layer]]
- [[Virtual Warehouse]]

## Explain it to a teammate (fill in yourself)

> 
