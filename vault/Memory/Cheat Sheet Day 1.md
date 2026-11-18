---
tags: [memory, day1]
---
# Cheat Sheet Day 1

One page. Print it, stick it up, rewrite it from memory in a week.

## Architecture

```
 CLOUD SERVICES   login · metadata · optimizer · result cache     (billed above 10 % of WH credits)
 COMPUTE          virtual warehouses, MPP, per-second credits      (the only layer you size)
 DATABASE STORAGE micro-partitions in object storage, columnar     (billed per compressed TB)
```
Hybrid of shared-disk and shared-nothing. [[Three-Layer Architecture]] · [[Cloud Services Layer]] · [[Compute Layer]] · [[Database Storage Layer]]

## Storage

- [[Micro-partitions]]: 50 to 500 MB uncompressed, columnar, immutable, automatic, min/max per column.
- [[Query Pruning]]: skip partitions by metadata; Query Profile shows *Partitions scanned / total*.
- [[Clustering Keys]]: `CLUSTER BY`, multi-TB tables only, Automatic Clustering is serverless and costs credits.

## Warehouses

| Size | XS | S | M | L | XL | 2XL | 3XL | 4XL | 5XL | 6XL |
|------|----|---|---|---|----|-----|-----|-----|-----|-----|
| Credits/h | 1 | 2 | 4 | 8 | 16 | 32 | 64 | 128 | 256 | 512 |

Per second, 60 s minimum per start. Default auto-suspend 600 s; suspend drops the warehouse cache. Up = heavier query, out = more concurrency (multi-cluster, Enterprise). Maximized: min = max. Policies: Standard, Economy. [[Virtual Warehouse]] · [[Warehouse Sizes and Credits]] · [[Auto-suspend and Auto-resume]] · [[Scaling Up vs Scaling Out]] · [[Multi-cluster Warehouse]]

## Caches

| Cache | Where | Lifetime |
|-------|-------|----------|
| [[Result Cache]] | Cloud Services | 24 h, reset on reuse, 31 d max |
| [[Warehouse Cache]] | warehouse local disk | until suspend |
| [[Metadata Cache]] | Cloud Services | always current |

Result reuse needs identical text, unchanged data, allowed role, deterministic SQL. [[Caching]]

## Platform

| Edition | Key additions |
|---------|---------------|
| Standard | everything basic, Time Travel 1 day |
| Enterprise | multi-cluster, Time Travel 90 d, materialized views, masking |
| Business Critical | Tri-Secret Secure, private connectivity, account failover, HIPAA/PCI |
| VPS | fully isolated environment |

One account = one cloud + one region. Identifier `<orgname>-<account_name>`. ORGADMIN above accounts, ACCOUNTADMIN inside. Bill = compute + storage + transfer; ingress free. [[Snowflake Editions]] · [[Cloud Providers and Regions]] · [[Organizations and Accounts]] · [[Credits and Billing]] · [[Snowsight]]

## Five Hadoop mappings

HDFS → storage layer · YARN queue + executors → warehouse · Hive Metastore → Cloud Services · Hive partitions → micro-partitions (automatic) · Hue → Snowsight. [[Hadoop to Snowflake Rosetta Stone]]

## Five exam traps

1. "Query Processing" and "Compute" are the same layer.
2. Cloud Services is free only up to 10 % of daily warehouse credits.
3. Suspend drops the warehouse cache, not the result cache.
4. Multi-cluster needs Enterprise; max = min means Maximized.
5. Snowsight defaults new warehouses to X-Large; SQL defaults to X-Small.
