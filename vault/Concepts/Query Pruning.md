---
tags: [concept, day1, storage]
docs: https://docs.snowflake.com/en/user-guide/tables-clustering-micropartitions
---
# Query Pruning

**In one sentence:** Pruning is the optimizer skipping every micro-partition whose column metadata proves it cannot contain rows matching the query, before any data is read.

**Why it matters:** Pruning is Snowflake's substitute for indexes. A query that prunes well on a 10 TB table reads megabytes; one that cannot prune reads the whole table and you pay for every second of it.

**Coming from Hadoop:** Hive partition pruning on `dt`, generalised to every column, plus Parquet row-group min/max statistics, done centrally by the optimizer rather than by each mapper opening footers. The analogy breaks because pruning quality depends on how data was ordered when loaded, not on a directory layout you designed (see [[Hadoop to Snowflake Rosetta Stone]])

## How it works

Two kinds of pruning happen on every query:

1. **Partition pruning.** [[Cloud Services Layer]] compares the predicate with each micro-partition's min/max metadata. Partitions that cannot match are never read. `WHERE ship_date BETWEEN '2026-01-01' AND '2026-01-07'` on a table loaded in date order touches a handful of partitions.
2. **Column pruning.** Inside the partitions that are read, only the referenced columns are fetched, because the storage is columnar.

You can see pruning in **Query Profile** (Snowsight → Monitoring → Query History → a query → Query Profile): the TableScan node reports *Partitions scanned* against *Partitions total*. A small ratio means good pruning.

Pruning works well when:

- the filter column's values are grouped, not scattered, across partitions (natural for load-date columns);
- the predicate is a simple comparison the optimizer can evaluate against min/max (`=`, `<`, `BETWEEN`, `IN`). Wrapping the column in a function (`WHERE TO_CHAR(ship_date,'YYYY') = '2026'`) usually disables it.

When a huge table is filtered on a column that does not prune, [[Clustering Keys]] reorganise micro-partitions so that it does.

## Gotchas / exam traps

- Pruning happens before execution, in Cloud Services, using metadata only. No warehouse time is spent on skipped partitions.
- Functions on the filtered column, `LIKE '%x'`, and comparing columns of different types tend to defeat pruning.
- "Partitions scanned" much lower than "Partitions total" in Query Profile is the evidence that pruning worked.

## Related

- [[Micro-partitions]]
- [[Clustering Keys]]
- [[Cloud Services Layer]]
- [[Snowsight]]
- [[Warehouse Sizes and Credits]]

## Explain it to a teammate (fill in yourself)

> 
