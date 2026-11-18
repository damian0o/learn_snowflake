---
tags: [concept, day1, compute]
docs: https://docs.snowflake.com/en/user-guide/warehouses-overview
---
# Warehouse Sizes and Credits

**In one sentence:** Warehouse sizes run from X-Small to 6X-Large, each step doubles the compute and the credits per hour, starting at 1 credit per hour for X-Small, billed per second with a 60-second minimum.

**Why it matters:** Sizing is the main cost lever. Doubling the size usually halves the time of a big query, so the cost is the same; it only wastes money when the query was already fast or when the warehouse sits idle.

**Coming from Hadoop:** Cluster sizing and `spark.executor.instances`. The analogy breaks because you resize in one statement, with no restart, and because the price is linear and public: a Medium costs exactly four times an X-Small, so right-sizing is arithmetic, not guesswork (see [[Hadoop to Snowflake Rosetta Stone]])

## How it works

| Size | Credits per hour (Gen1) | Rough mental model |
|------|------------------------|--------------------|
| X-Small (XS) | 1 | 1 node |
| Small (S) | 2 | 2 nodes |
| Medium (M) | 4 | 4 nodes |
| Large (L) | 8 | 8 nodes |
| X-Large (XL) | 16 | 16 nodes |
| 2X-Large | 32 | |
| 3X-Large | 64 | |
| 4X-Large | 128 | |
| 5X-Large | 256 | AWS and Azure only |
| 6X-Large | 512 | AWS and Azure only |

Billing rules:

- **Per second**, with a **60-second minimum** every time the warehouse starts or resumes. A warehouse that runs 61 seconds, suspends, and runs 30 seconds more is billed 60 + 1 + 60 = 121 seconds.
- A suspended warehouse costs nothing.
- Resizing bills the new size from the moment the new nodes are provisioned.
- A multi-cluster warehouse bills size credits times running clusters (a Medium with 3 clusters running is 12 credits per hour).

Rule of thumb for sizing: a bigger warehouse helps **one heavy query** (large scans, big joins, spilling to disk). It does not help many small queries; for those use a [[Multi-cluster Warehouse]] or just a smaller warehouse. Start small, watch Query Profile for spilling and long scans, step up one size at a time.

## Gotchas / exam traps

- Credits double per size: XS 1, S 2, M 4, L 8, XL 16, 2XL 32, 3XL 64, 4XL 128, 5XL 256, 6XL 512.
- The 60-second minimum applies at every start or resume, not once a day. Aggressive auto-suspend on a bursty workload can cost more than a longer timeout.
- A credit is the unit; the price per credit depends on edition, cloud and region, and is set by your contract.

## Related

- [[Virtual Warehouse]]
- [[Scaling Up vs Scaling Out]]
- [[Credits and Billing]]
- [[Auto-suspend and Auto-resume]]
- [[Multi-cluster Warehouse]]

## Explain it to a teammate (fill in yourself)

> 
