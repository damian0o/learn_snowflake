---
tags: [concept, day1, platform]
docs: https://docs.snowflake.com/en/user-guide/cost-understanding-overall
---
# Credits and Billing

**In one sentence:** A Snowflake bill is compute (credits for warehouses, serverless features and excess cloud services), storage (a flat rate per compressed terabyte per month) and data transfer (egress between regions or clouds).

**Why it matters:** A data engineer owns most of the compute line. Knowing the three meters and what moves each one is how you keep the warehouse you are about to build affordable.

**Coming from Hadoop:** Node-hours and the capital cost of racks, paid whether the cluster was busy or not. The analogy breaks completely: Snowflake meters seconds of compute, bytes of compressed storage and bytes leaving the region, each separately, so an idle platform costs almost nothing and a careless query costs real money (see [[Hadoop to Snowflake Rosetta Stone]])

## How it works

**1. Compute, in credits.** A credit is the unit of compute; its price in money depends on edition, cloud and region.

- **Virtual warehouses:** credits per second while running, by size (see [[Warehouse Sizes and Credits]]), 60-second minimum per start.
- **Serverless features:** Snowpipe, Automatic Clustering, serverless tasks, search optimization, materialized view maintenance. They use Snowflake-managed compute and bill credits with no warehouse of yours running.
- **Cloud Services:** metered in credits, but charged only for the part above **10 % of the day's warehouse credits** (daily, UTC). Serverless usage does not count toward that base. See [[Cloud Services Layer]].

**2. Storage.** A flat rate per terabyte per month, computed from the average daily on-disk (compressed) bytes, including data retained for Time Travel and Fail-safe and internal stages.

**3. Data transfer.** Ingress is free. Egress is charged when data leaves the region: replication or unloading to another region or another cloud, and cross-region shares. See [[Cloud Providers and Regions]].

Where to look: Snowsight **Admin → Cost Management**, and the `SNOWFLAKE.ACCOUNT_USAGE` views such as `WAREHOUSE_METERING_HISTORY`, `STORAGE_USAGE` and `METERING_DAILY_HISTORY`. A **resource monitor** (Day 2) caps credits per warehouse or per account and can suspend warehouses when the cap is hit.

## Gotchas / exam traps

- Three meters: compute, storage, data transfer. Compute has three parts: warehouses, serverless, cloud services.
- Cloud services are charged only above 10 % of daily warehouse credits, and only the excess.
- Storage is billed on compressed bytes and includes Time Travel and Fail-safe history.

## Related

- [[Warehouse Sizes and Credits]]
- [[Cloud Services Layer]]
- [[Cloud Providers and Regions]]
- [[Virtual Warehouse]]
- [[Snowsight]]

## Explain it to a teammate (fill in yourself)

> 
