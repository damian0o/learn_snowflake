---
tags: [concept, day1, architecture]
docs: https://docs.snowflake.com/en/user-guide/intro-key-concepts
---
# Three-Layer Architecture

**In one sentence:** Snowflake is built from three independent layers: Database Storage at the bottom, Compute (virtual warehouses) in the middle, and Cloud Services on top.

**Why it matters:** Every performance, cost and security question maps to one layer. Knowing which layer does what tells you where to look and what you are paying for.

**Coming from Hadoop:** In Cloudera the three jobs were also split, HDFS stored, YARN plus Spark or Hive computed, the Hive Metastore and Ranger coordinated, but they all ran on the same nodes you owned. In Snowflake the layers run on separate infrastructure that scales on its own. The analogy breaks because Hadoop compute was data-local (move the code to the data) while Snowflake compute reads from shared cloud storage over the network, relying on columnar pruning and caches to make that fast (see [[Hadoop to Snowflake Rosetta Stone]])

## How it works

```
 ┌──────────────────────────────────────────────┐
 │  CLOUD SERVICES  (the brain)                 │  login, metadata, optimizer,
 │  authentication · metadata · optimizer ·     │  access control, transactions,
 │  access control · transactions · result cache│  infrastructure management
 ├──────────────────────────────────────────────┤
 │  COMPUTE  (the muscles)                      │  virtual warehouses: MPP
 │  [WH_LOAD]  [WH_BI]  [WH_DS]  [WH_ADHOC]     │  clusters you size, start,
 │                                              │  suspend and pay for
 ├──────────────────────────────────────────────┤
 │  DATABASE STORAGE  (the memory)              │  one copy of all data in cloud
 │  micro-partitions in S3 / Blob / GCS         │  object storage, columnar,
 │                                              │  compressed, encrypted
 └──────────────────────────────────────────────┘
```

Snowflake calls this a **hybrid of shared-disk and shared-nothing**. Shared-disk: there is one central data repository that every compute node can reach. Shared-nothing: a query runs on an MPP cluster (a warehouse) whose nodes each process a portion of the data locally, in parallel. You get the simplicity of one copy of the data and the speed of parallel processing.

Each layer scales independently. Adding data does not need more compute. Adding users or workloads means adding or enlarging warehouses, not re-sharding storage.

Read the three layers in detail: [[Database Storage Layer]], [[Compute Layer]], [[Cloud Services Layer]].

## Gotchas / exam traps

- The docs name the middle layer **Compute**. Older material and many exam questions call it **Query Processing**. Same layer.
- Only the Compute layer is something you create and size. Storage and Cloud Services are managed entirely by Snowflake.
- Hybrid means both, not a choice. If a question asks whether Snowflake is shared-disk or shared-nothing, the answer is a hybrid of the two.

## Related

- [[What Snowflake Is]]
- [[Database Storage Layer]]
- [[Compute Layer]]
- [[Cloud Services Layer]]
- [[Virtual Warehouse]]

## Explain it to a teammate (fill in yourself)

> 
