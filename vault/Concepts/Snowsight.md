---
tags: [concept, day1, platform]
docs: https://docs.snowflake.com/en/user-guide/ui-snowsight
---
# Snowsight

**In one sentence:** Snowsight is Snowflake's web interface: worksheets for SQL, query history and Query Profile for diagnosis, and admin pages for warehouses, cost and users.

**Why it matters:** Everything in these notes can be observed in Snowsight: pruning, cache hits, warehouse credits. It is where you check whether what you learned is true.

**Coming from Hadoop:** Hue plus Cloudera Manager in one browser tab. The analogy breaks because Snowsight's Query Profile shows you the execution plan of every query you ever ran, with bytes scanned, partitions pruned and cache hits, something Hue never came close to (see [[Hadoop to Snowflake Rosetta Stone]])

## How it works

Menu names shift a little between releases; the pieces you will use on Day 1:

| Where | What for |
|-------|----------|
| **Projects → Worksheets** | write and run SQL; each worksheet has a current role, warehouse, database and schema shown at the top |
| **Monitoring → Query History** | every query in the account with duration, bytes scanned, warehouse, user; click one to open **Query Profile** |
| **Query Profile** | the execution plan: each operator, *Partitions scanned / total*, *bytes scanned from cache*, *bytes spilled*, and the single node *QUERY RESULT REUSE* when the [[Result Cache]] answered |
| **Admin → Warehouses** | create, resize, suspend, see what is running and queued |
| **Admin → Cost Management** | credits per warehouse and per day, storage, serverless usage |
| **Admin → Accounts** | organization view (needs ORGADMIN) |
| **Data → Databases** | browse objects, grants, previews |

The SQL you type in a worksheet is exactly the SQL a driver sends. Snowsight adds convenience (autocomplete, result charts, filters) but no special powers; anything you do there you can script with Snowflake CLI or a connector in phase 2.

## Gotchas / exam traps

- Snowsight defaults a new warehouse to X-Large. Change the size before clicking Create.
- Query Profile is where you prove pruning and caching claims; learn to find *Partitions scanned* and *QUERY RESULT REUSE*.
- The classic console is gone; Snowsight is the only web UI.

## Related

- [[Query Pruning]]
- [[Result Cache]]
- [[Virtual Warehouse]]
- [[Snowflake Account]]
- [[Organizations and Accounts]]

## Explain it to a teammate (fill in yourself)

> 
