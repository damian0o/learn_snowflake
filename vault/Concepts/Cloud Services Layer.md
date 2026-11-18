---
tags: [concept, day1, architecture]
docs: https://docs.snowflake.com/en/user-guide/intro-key-concepts
---
# Cloud Services Layer

**In one sentence:** Cloud Services is the always-on coordination layer that authenticates you, keeps all metadata, parses and optimises every query, enforces access control and manages the infrastructure.

**Why it matters:** It is why a Snowflake query can be planned, pruned and sometimes fully answered before a single warehouse starts, and it is the layer behind the 10 % billing rule that occasionally shows up on invoices.

**Coming from Hadoop:** Think Hive Metastore plus Ranger plus the YARN ResourceManager plus the Hive query compiler, rolled into one service you never run. The analogy breaks because Cloud Services also holds statistics for every micro-partition and the result cache, so it can answer some queries alone, which the Metastore never could (see [[Hadoop to Snowflake Rosetta Stone]])

## How it works

Cloud Services is a collection of services running on compute instances that Snowflake provisions. Its jobs:

| Job | What it means for you |
|-----|-----------------------|
| Authentication and access control | logins, MFA, SSO, roles and grants are checked here |
| Metadata management | every table, column, micro-partition statistic, grant and query history record |
| Query parsing and optimisation | the plan, including which micro-partitions to skip (see [[Query Pruning]]) |
| Infrastructure management | starting and stopping warehouse nodes, upgrades |
| Transactions and the [[Result Cache]] | ACID coordination; identical queries served without compute |

Because the metadata lives here, some statements never touch a warehouse: `SHOW TABLES`, `DESCRIBE`, and whole-table `COUNT(*)`, `MIN`, `MAX` (see [[Metadata Cache]]).

**Billing.** Cloud Services usage is measured in credits but charged only for the part that exceeds **10 % of the day's warehouse credits** (calculated daily, UTC). A day with 100 warehouse credits and 8 cloud-services credits costs 100; with 20 cloud-services credits it costs 110. Serverless compute does not count toward the 10 % base. Workloads with thousands of tiny metadata-heavy queries are the usual way to cross the line.

## Gotchas / exam traps

- Cloud Services is not free. It is free up to 10 % of daily warehouse usage; the excess is billed.
- The optimizer lives here, not in the warehouse. The warehouse executes the plan it is handed.
- You cannot size, suspend or see the Cloud Services instances. If a question offers a way to configure them, it is a distractor.

## Related

- [[Three-Layer Architecture]]
- [[Compute Layer]]
- [[Metadata Cache]]
- [[Result Cache]]
- [[Credits and Billing]]

## Explain it to a teammate (fill in yourself)

> 
