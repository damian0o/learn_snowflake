---
tags: [concept, day1, compute]
docs: https://docs.snowflake.com/en/user-guide/warehouses-overview
---
# Virtual Warehouse

**In one sentence:** A virtual warehouse is a named cluster of compute that executes your queries and loads, which you create, size, start, suspend and pay for by the second.

**Why it matters:** Warehouses are where the money goes and where performance is decided. A data engineer's daily Snowflake decisions are mostly warehouse decisions: how many, what size, when they sleep.

**Coming from Hadoop:** A YARN queue with a fixed pool of Spark executors, except you can create one per team or job in a second, resize it in a sentence, and switch it off when the job ends. The analogy breaks because a warehouse keeps no data of its own, so there is nothing to rebalance when you add, remove or resize them (see [[Hadoop to Snowflake Rosetta Stone]])

## How it works

```sql
CREATE WAREHOUSE WH_ANALYTICS_LOAD_S
  WAREHOUSE_SIZE = SMALL
  AUTO_SUSPEND = 300
  AUTO_RESUME = TRUE
  INITIALLY_SUSPENDED = TRUE
  COMMENT = 'Batch loads for the analytics domain';
```

A warehouse provides the CPU, memory and temporary storage for SQL execution: `SELECT`, DML, and `COPY INTO` loads and unloads all need a running warehouse. It is a cluster of nodes whose count doubles with each size step (see [[Warehouse Sizes and Credits]]).

Lifecycle:

- **Created suspended or running.** `INITIALLY_SUSPENDED = TRUE` avoids paying the 60-second minimum for a warehouse you only wanted to define.
- **Resumes on demand** when a query arrives, if `AUTO_RESUME` is on (default). See [[Auto-suspend and Auto-resume]].
- **Suspends after idling** for `AUTO_SUSPEND` seconds (default 600). Suspended warehouses cost nothing.
- **Resizes live.** `ALTER WAREHOUSE ... SET WAREHOUSE_SIZE = LARGE` adds nodes; queries already running are unaffected, queued and new queries use the new size. See [[Scaling Up vs Scaling Out]].
- **Grows sideways** with extra clusters for concurrency on Enterprise edition. See [[Multi-cluster Warehouse]].

A session uses one current warehouse (`USE WAREHOUSE`), and a user can have a default. Good practice is one warehouse per workload: loading, transformation, BI, ad-hoc, each named by the team standard (`WH_<TEAM>_<PURPOSE>_<SIZE>`, Day 3).

Snowflake now offers **Generation 2 (Gen2)** standard warehouses with faster hardware; the credit table most material quotes is for Gen1. Check `GENERATION` in `SHOW WAREHOUSES` when comparing costs.

## Gotchas / exam traps

- A warehouse is compute only. It holds a cache (see [[Warehouse Cache]]), never the tables. Dropping it loses nothing.
- Some statements do not need a warehouse at all: `SHOW`, `DESCRIBE`, and queries served from the [[Result Cache]] or [[Metadata Cache]].
- Snowsight defaults new warehouses to X-Large; `CREATE WAREHOUSE` defaults to X-Small. Check the size before you click Create.

## Related

- [[Compute Layer]]
- [[Warehouse Sizes and Credits]]
- [[Auto-suspend and Auto-resume]]
- [[Scaling Up vs Scaling Out]]
- [[Multi-cluster Warehouse]]
- [[Warehouse Cache]]

## Explain it to a teammate (fill in yourself)

> 
