---
tags: [concept, day1, compute]
docs: https://docs.snowflake.com/en/user-guide/warehouses-multicluster
---
# Multi-cluster Warehouse

**In one sentence:** A multi-cluster warehouse is one warehouse that can run several identical clusters at once, starting and stopping them automatically to absorb concurrency, available on Enterprise edition and above.

**Why it matters:** It is how a shared BI warehouse survives Monday morning without a human resizing it, and it is a favourite exam topic: modes, policies and the edition requirement.

**Coming from Hadoop:** Adding capacity to a YARN queue when jobs pile up, done automatically and reversed when the rush ends. The analogy breaks because each extra cluster is an exact copy of the warehouse that serves whole queries; work is not split across clusters, queries are routed to the least loaded one (see [[Hadoop to Snowflake Rosetta Stone]])

## How it works

```sql
CREATE WAREHOUSE WH_BI_M
  WAREHOUSE_SIZE = MEDIUM
  MIN_CLUSTER_COUNT = 1
  MAX_CLUSTER_COUNT = 4
  SCALING_POLICY = STANDARD
  AUTO_SUSPEND = 600;
```

**Modes**

- **Maximized**: `MIN_CLUSTER_COUNT = MAX_CLUSTER_COUNT` (greater than 1). All clusters run whenever the warehouse runs. Predictable, expensive.
- **Auto-scale**: `MIN < MAX`. Snowflake adds a cluster when queries queue and removes one when load drops.

**Scaling policies** (auto-scale only)

| Policy | Starts a cluster | Shuts one down |
|--------|------------------|----------------|
| Standard (default) | immediately when a query queues; minimises waiting | after 2 to 3 consecutive checks show the load could move to other clusters |
| Economy | only if there is enough queued work to keep a cluster busy for at least 6 minutes; saves credits, tolerates queueing | after 5 to 6 consecutive checks |

**Limits.** Snowsight lets you set up to 10 clusters. SQL allows more, depending on size (300 for X-Small to Medium, down to 10 for 4X-Large and above). Cost is size credits times running clusters: a Medium at 4 clusters bills up to 16 credits per hour.

Multi-cluster warehouses are the **scale out** answer in [[Scaling Up vs Scaling Out]].

## Gotchas / exam traps

- Enterprise edition or higher. On Standard edition `MAX_CLUSTER_COUNT` cannot exceed 1.
- Maximized means min equals max; auto-scale means min is less than max. Both are set with the same two parameters.
- Scaling policies are Standard and Economy. Economy trades some queueing for fewer credits.

## Related

- [[Virtual Warehouse]]
- [[Scaling Up vs Scaling Out]]
- [[Snowflake Editions]]
- [[Warehouse Sizes and Credits]]
- [[Auto-suspend and Auto-resume]]

## Explain it to a teammate (fill in yourself)

> 
