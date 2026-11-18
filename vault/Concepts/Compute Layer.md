---
tags: [concept, day1, architecture]
docs: https://docs.snowflake.com/en/user-guide/intro-key-concepts
---
# Compute Layer

**In one sentence:** The Compute layer (also called Query Processing) is where SQL runs: on virtual warehouses, independent MPP clusters that you create, size and pay for.

**Why it matters:** This is the only layer you control, and the only one with a meaningful bill attached to your decisions. Warehouse sizing, suspension and separation per workload are the daily work of a Snowflake engineer.

**Coming from Hadoop:** YARN queues and the Spark executors they hand out. A warehouse is a cluster of nodes that processes one query in parallel, like a Spark job across executors. The analogy breaks because a warehouse holds no data permanently (only a cache), so you can have ten of them reading the same table at once, and you can switch one off at lunch without losing anything (see [[Hadoop to Snowflake Rosetta Stone]])

## How it works

A query is planned in [[Cloud Services Layer]] and then executed on a **virtual warehouse**: a named cluster of compute nodes provisioned by Snowflake from the cloud provider. Nodes process micro-partitions in parallel (MPP), each handling a share of the data, and exchange intermediate results over the network.

Properties of this layer:

- **Independent clusters.** Each warehouse is isolated. A heavy transformation on `WH_LOAD` does not slow dashboards on `WH_BI`.
- **Shared storage.** Every warehouse reads the same [[Database Storage Layer]]. No copies, no sync.
- **Elastic.** Resize up for heavier queries, add clusters for more concurrent users (see [[Scaling Up vs Scaling Out]]), suspend when idle (see [[Auto-suspend and Auto-resume]]).
- **Local cache.** Nodes keep recently read table data on local disk for as long as the warehouse runs (see [[Warehouse Cache]]).
- **Billed per second** in credits, with a 60-second minimum each start (see [[Warehouse Sizes and Credits]]).

The common pattern is one warehouse per workload type: loading, transformation, BI, ad-hoc analysis, each sized and scheduled to fit.

## Gotchas / exam traps

- "Query Processing layer" and "Compute layer" are the same thing; the docs moved to the second name.
- A warehouse processes queries; it does not store your tables. Dropping a warehouse loses no data.
- Two warehouses never share compute. If one is saturated, the other is unaffected.

## Related

- [[Three-Layer Architecture]]
- [[Virtual Warehouse]]
- [[Cloud Services Layer]]
- [[Database Storage Layer]]
- [[Warehouse Cache]]

## Explain it to a teammate (fill in yourself)

> 
