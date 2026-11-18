---
tags: [concept, day1, architecture]
docs: https://docs.snowflake.com/en/user-guide/intro-key-concepts
---
# What Snowflake Is

**In one sentence:** Snowflake is a fully managed cloud data platform, sold as a service, where storage and compute are separate and you pay for each only while you use it.

**Why it matters:** Almost every design decision you will make, from how many warehouses to create to how to name schemas, follows from these three facts: nothing to install, storage and compute scale independently, and the meter runs per second.

**Coming from Hadoop:** Cloudera gave you a cluster you owned and kept running: HDFS for files, YARN for scheduling, Hive and Spark for processing. Snowflake gives you a database you log in to. There is no cluster to patch, no NameNode, no HDFS quota. The analogy breaks at cost: a Hadoop cluster costs the same idle or busy, while Snowflake storage is cheap and compute costs money only while a warehouse runs (see [[Hadoop to Snowflake Rosetta Stone]])

## How it works

Snowflake is **software as a service**. You get an account in one cloud region (AWS, Azure or Google Cloud) and talk to it with SQL. Snowflake owns and operates everything underneath: the virtual machines, the object storage, the upgrades.

Three ideas carry the whole platform:

1. **Storage and compute are separate.** Data lives once, in cloud object storage, compressed and columnar. Any number of compute clusters (virtual warehouses) can read it at the same time without copying it.
2. **Compute is elastic and billed per second.** You create a warehouse, pick a size, and pay credits only while it runs. Suspend it and the meter stops.
3. **A services layer coordinates everything.** Login, metadata, query planning, security and transactions happen in Cloud Services, which you never provision.

The result is one copy of the data, many independent workloads (loading, transformation, BI, data science) each on its own compute, none fighting the others for resources.

## Gotchas / exam traps

- Snowflake is not a database you install. There is no on-premises version and no Snowflake inside your Kubernetes cluster.
- Snowflake is not built on Hadoop, Spark or any other existing engine. The storage format and the query engine are Snowflake's own.
- "Serverless" in Snowflake marketing has a precise meaning: features (Snowpipe, Automatic Clustering, serverless tasks) that use Snowflake-managed compute and bill credits without a warehouse of yours.

## Related

- [[Three-Layer Architecture]]
- [[Virtual Warehouse]]
- [[Credits and Billing]]
- [[Cloud Providers and Regions]]
- [[Snowflake Editions]]

## Explain it to a teammate (fill in yourself)

> 
