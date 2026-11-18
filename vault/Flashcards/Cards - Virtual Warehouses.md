---
tags: [flashcards/day1, cards]
---
# Cards - Virtual Warehouses

Cards for: [[Virtual Warehouse]], [[Warehouse Sizes and Credits]], [[Auto-suspend and Auto-resume]], [[Scaling Up vs Scaling Out]], [[Multi-cluster Warehouse]]

What is a virtual warehouse?::A named cluster of compute that executes queries and loads. You create, size, suspend and pay for it by the second. It holds no tables, only a cache. [[Virtual Warehouse]]

What happens to your data when you drop a warehouse?::Nothing. Warehouses are compute only; data lives in the storage layer. [[Virtual Warehouse]]

Credits per hour by size, X-Small to X-Large?::XS 1, S 2, M 4, L 8, XL 16. Each size doubles. [[Warehouse Sizes and Credits]]

Credits per hour for 2XL, 3XL, 4XL, 5XL, 6XL?::32, 64, 128, 256, 512. (5XL and 6XL are AWS and Azure only.) [[Warehouse Sizes and Credits]]

Warehouses bill per ==second== with a ==60==-second minimum every time they start or resume. [[Warehouse Sizes and Credits]]

A warehouse runs 61 s, suspends, then runs 30 s. How many seconds are billed?::121 seconds: 60 + 1 for the first run, 60 minimum for the second. [[Warehouse Sizes and Credits]]

What is the default AUTO_SUSPEND and what does 0 mean?::600 seconds (10 minutes). 0 or NULL disables auto-suspend; the warehouse never sleeps. [[Auto-suspend and Auto-resume]]

What is lost when a warehouse suspends?::Its local warehouse cache. Data and the result cache are untouched. [[Auto-suspend and Auto-resume]]

Why not set every warehouse to suspend after 60 seconds?
?
Each resume costs a 60-second minimum and starts with a cold cache. Bursty or BI workloads can end up slower and more expensive than with a 5 to 10 minute timeout. [[Auto-suspend and Auto-resume]]

Default size when you create a warehouse in SQL versus in Snowsight?::SQL `CREATE WAREHOUSE` defaults to X-Small; the Snowsight form defaults to X-Large. [[Virtual Warehouse]]

One query is slow because of a huge join. Scale up or out?::Up: resize to a larger warehouse. Scaling out only helps concurrency. [[Scaling Up vs Scaling Out]]

Dashboards queue at 9 a.m., each query is fast on its own. Scale up or out?::Out: a multi-cluster warehouse adds clusters while the queue exists. [[Scaling Up vs Scaling Out]]

How do you tell "scale up" from "scale out" symptoms in Query History?::Long *execution* time means scale up; long *queued* time means scale out. [[Scaling Up vs Scaling Out]]

Does resizing a running warehouse interrupt running queries?::No. Running queries finish on their current resources; queued and new queries use the new size. [[Scaling Up vs Scaling Out]]

Which edition is required for multi-cluster warehouses?::Enterprise or higher. [[Multi-cluster Warehouse]]

Maximized mode versus Auto-scale mode?::Maximized: MIN_CLUSTER_COUNT = MAX_CLUSTER_COUNT (greater than 1), all clusters always run. Auto-scale: MIN < MAX, clusters start and stop with load. [[Multi-cluster Warehouse]]

Name the two scaling policies and the difference.
?
Standard starts a cluster as soon as a query queues (minimise waiting). Economy starts one only if there is at least 6 minutes of queued work (save credits). [[Multi-cluster Warehouse]]

A Medium warehouse with 4 clusters running bills how many credits per hour?::16: 4 credits per Medium cluster times 4 clusters. [[Multi-cluster Warehouse]]

Coming from Hadoop: what is the closest thing to a warehouse, and where does the analogy break?::A YARN queue with its Spark executors. It breaks because a warehouse holds no data, so you can create, resize or drop it in seconds with nothing to rebalance. [[Virtual Warehouse]]
