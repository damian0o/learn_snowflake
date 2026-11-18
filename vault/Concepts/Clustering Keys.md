---
tags: [concept, day1, storage]
docs: https://docs.snowflake.com/en/user-guide/tables-clustering-keys
---
# Clustering Keys

**In one sentence:** A clustering key is one to a few columns you declare with CLUSTER BY so that Snowflake continuously reorganises a very large table's micro-partitions to keep those columns' values grouped together.

**Why it matters:** It is the one storage tuning knob you have, it costs credits continuously, and it is only worth it for multi-terabyte tables with slow, selective filters. Knowing when not to use it saves money.

**Coming from Hadoop:** Hive bucketing and the careful sort-before-write you did in Spark to make Parquet statistics useful. The analogy breaks because clustering is maintained for you after every load by a serverless service (Automatic Clustering), and because you rarely need it: natural load order plus micro-partition metadata already prunes most tables well (see [[Hadoop to Snowflake Rosetta Stone]])

## How it works

By default micro-partitions follow insertion order, which prunes well on load-time columns and poorly on others. For a table that is **multiple terabytes** and is usually filtered or joined on a column that does not prune, define a clustering key:

```sql
ALTER TABLE fct_orders CLUSTER BY (customer_region, order_date);
```

Snowflake's **Automatic Clustering** then reclusters in the background whenever enough new data has arrived, rewriting micro-partitions so that each one covers a narrow range of the key. This runs on Snowflake-managed (serverless) compute and consumes credits; it also keeps the replaced partitions for Time Travel and Fail-safe, so it costs storage too.

Choosing a key:

- Columns used most in **selective filters**, then columns used in **joins**.
- **Moderate cardinality**: enough distinct values to prune, few enough to group. A boolean is useless; a UUID is too fine. Prefer `order_date` to `order_timestamp`, or cluster on an expression such as `TO_DATE(order_timestamp)`.
- At most 3 or 4 columns, ordered from lowest to highest cardinality.

Check the effect with `SYSTEM$CLUSTERING_INFORMATION` and `SYSTEM$CLUSTERING_DEPTH`; lower depth is better clustered.

## Gotchas / exam traps

- Clustering is for very large tables (multi-TB). For everything else, the default load order is enough and clustering just burns credits.
- Automatic Clustering is serverless: it bills credits with no warehouse of yours running.
- A cloned table has Automatic Clustering suspended; you must resume it. Clustering keys cannot be defined on hybrid tables.

## Related

- [[Micro-partitions]]
- [[Query Pruning]]
- [[Database Storage Layer]]
- [[Credits and Billing]]
- [[Virtual Warehouse]]

## Explain it to a teammate (fill in yourself)

> 
