---
tags: [concept, day1, compute]
docs: https://docs.snowflake.com/en/sql-reference/sql/create-warehouse
---
# Auto-suspend and Auto-resume

**In one sentence:** Auto-suspend stops a warehouse after a set number of idle seconds so it stops billing; auto-resume starts it again, transparently, when the next query arrives.

**Why it matters:** Together they are why Snowflake compute can be cheap: the meter runs only while work is happening. Set them wrong and you either pay for idle nodes or lose your warehouse cache every few minutes.

**Coming from Hadoop:** Nothing in Cloudera did this. A cluster you kept warm cost the same at 3 a.m. as at 3 p.m.; a Spark job that finished released its executors but the nodes stayed on. The analogy breaks completely, which is why teams migrating from Hadoop over-provision at first: they are used to paying for capacity, not for seconds (see [[Hadoop to Snowflake Rosetta Stone]])

## How it works

```sql
ALTER WAREHOUSE WH_BI_M SET AUTO_SUSPEND = 600, AUTO_RESUME = TRUE;
ALTER WAREHOUSE WH_BI_M SUSPEND;   -- manual
ALTER WAREHOUSE WH_BI_M RESUME;
```

- `AUTO_SUSPEND = <seconds>`: the warehouse suspends after that long with no activity. Default **600** (10 minutes). `0` or `NULL` disables auto-suspend (it never sleeps; avoid). Snowflake checks roughly every 30 seconds, so the real delay is a little longer than the setting.
- `AUTO_RESUME = TRUE` (default): any statement that needs the warehouse starts it. With `FALSE` you must resume by hand and queries wait with an error.
- Multi-cluster: auto-suspend applies to the whole warehouse once only the minimum clusters remain and they are idle; auto-resume starts it when no cluster is running.

Choosing the timeout is a trade between credits and the [[Warehouse Cache]], which is dropped on suspend:

| Workload | Suggested auto-suspend |
|----------|------------------------|
| Loads and transformations (ELT) | short, 60 to 300 s; nothing to cache between runs |
| DevOps, data science, ad-hoc | about 5 minutes |
| BI dashboards, repeated SELECTs | 10 minutes or more, so the cache keeps serving |

Remember the 60-second minimum on every resume (see [[Warehouse Sizes and Credits]]): a warehouse that resumes every 90 seconds for a 5-second query is mostly paying minimums.

## Gotchas / exam traps

- Default auto-suspend is 600 seconds (10 minutes). Setting it to 0 disables suspension.
- Suspending drops the warehouse cache, so short timeouts make repeated queries slower, not just cheaper.
- Auto-resume is on by default. If a query seems to hang for a few seconds before running, that is the warehouse resuming.

## Related

- [[Virtual Warehouse]]
- [[Warehouse Cache]]
- [[Warehouse Sizes and Credits]]
- [[Multi-cluster Warehouse]]
- [[Credits and Billing]]

## Explain it to a teammate (fill in yourself)

> 
