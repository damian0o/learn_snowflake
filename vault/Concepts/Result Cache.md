---
tags: [concept, day1, compute]
docs: https://docs.snowflake.com/en/user-guide/querying-persisted-results
---
# Result Cache

**In one sentence:** The result cache stores every query's result set in Cloud Services for 24 hours and returns it instantly to anyone who runs the exact same query against unchanged data.

**Why it matters:** Dashboards that refresh the same queries cost nothing after the first run, and your benchmarks lie unless you switch it off.

**Coming from Hadoop:** No Hadoop equivalent; Hive and Impala re-executed every query (Impala could reuse metadata, not results). The analogy breaks because this cache is shared across users and needs no running compute at all (see [[Hadoop to Snowflake Rosetta Stone]])

## How it works

Every successful query's result is persisted. A new query reuses it when **all** of these hold:

- the SQL text is **identical**, byte for byte (case, whitespace and aliases matter);
- the underlying table data has **not changed** (no DML since) and the micro-partitions are unchanged (reclustering counts as a change);
- the role has the required privileges on the tables;
- the query uses no non-deterministic or external functions (`CURRENT_TIMESTAMP`, `RANDOM`, `UUID_STRING`, external functions all block reuse) and does not touch hybrid tables;
- `USE_CACHED_RESULT` is `TRUE` (the default) for the session.

Lifetime: **24 hours** after the last use. Each reuse resets the 24-hour window, up to **31 days** from the first execution, after which the result is purged and recomputed on the next run.

Reused results are served from [[Cloud Services Layer]], so no warehouse needs to be running and no warehouse credits are spent. In Query Profile the single node reads *QUERY RESULT REUSE*. Watch for it on Day 1 hands-on: run the same query twice and compare.

Meeting every condition does not guarantee reuse, but in practice it is reliable for dashboards and repeated reports.

## Gotchas / exam traps

- 24 hours, reset on every reuse, maximum 31 days total.
- Exact text. `SELECT *` and `select *` are different queries to the result cache.
- A different user with the same role gets the cached result too; the cache is per account, not per user.

## Related

- [[Caching]]
- [[Cloud Services Layer]]
- [[Warehouse Cache]]
- [[Metadata Cache]]
- [[Snowsight]]

## Explain it to a teammate (fill in yourself)

> 
