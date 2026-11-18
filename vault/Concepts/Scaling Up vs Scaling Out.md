---
tags: [concept, day1, compute]
docs: https://docs.snowflake.com/en/user-guide/warehouses-considerations
---
# Scaling Up vs Scaling Out

**In one sentence:** Scaling up means resizing a warehouse to a larger size for heavier individual queries; scaling out means adding clusters to a multi-cluster warehouse for more concurrent users.

**Why it matters:** Picking the wrong direction is the classic Snowflake mistake: a bigger warehouse does nothing for a queue of small dashboard queries, and more clusters do nothing for one giant join.

**Coming from Hadoop:** Scaling up is giving a Spark job more and bigger executors; scaling out is adding more YARN queue capacity so more jobs run at once. The analogy breaks because in Snowflake both are a one-line `ALTER`, take effect in seconds, and the second one can be automatic (see [[Hadoop to Snowflake Rosetta Stone]])

## How it works

```
 Scale UP (size)                      Scale OUT (clusters)
 one query is slow                    many queries are queued
 ┌────┐   ┌────────┐                  ┌────┐ ┌────┐ ┌────┐
 │ S  │ → │   L    │                  │ M  │ │ M  │ │ M  │
 └────┘   └────────┘                  └────┘ └────┘ └────┘
 more nodes per query                 same size, more copies
 ALTER WAREHOUSE ... SET              ALTER WAREHOUSE ... SET
   WAREHOUSE_SIZE = LARGE               MAX_CLUSTER_COUNT = 3
```

**Scale up** when a single query is slow because of data volume or complexity: long table scans, big joins, sorts that spill to local or remote storage (visible in Query Profile as *bytes spilled*). Resizing is immediate for new and queued queries; running ones finish on the resources they have.

**Scale out** when queries are individually fast but users wait in a queue, typically BI at 9 a.m. A [[Multi-cluster Warehouse]] starts extra clusters of the same size while the queue exists and shuts them down when it drains. Enterprise edition is required.

A useful test: look at Query History. If the slow queries show long *execution* time, scale up. If they show long *queued* time, scale out.

## Gotchas / exam traps

- Scaling up helps one heavy query. Scaling out helps many concurrent queries. Exam questions describe a symptom and expect you to pick the matching direction.
- Resizing a running warehouse does not interrupt running queries. Downsizing drops the cache attached to the removed nodes.
- Scaling out needs Enterprise edition or higher; scaling up is available on every edition.

## Related

- [[Virtual Warehouse]]
- [[Multi-cluster Warehouse]]
- [[Warehouse Sizes and Credits]]
- [[Snowsight]]
- [[Warehouse Cache]]

## Explain it to a teammate (fill in yourself)

> 
