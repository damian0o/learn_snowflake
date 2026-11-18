---
tags: [flashcards/day1, cards]
---
# Cards - Architecture

Cards for: [[What Snowflake Is]], [[Three-Layer Architecture]], [[Cloud Services Layer]], [[Compute Layer]], [[Database Storage Layer]], [[Micro-partitions]], [[Query Pruning]], [[Clustering Keys]]

What kind of product is Snowflake, in three words?::A fully managed cloud data platform delivered as a service (SaaS). Nothing to install or patch. [[What Snowflake Is]]

Name the three layers of Snowflake's architecture, bottom to top.::Database Storage, Compute (also called Query Processing), Cloud Services. [[Three-Layer Architecture]]

Snowflake describes its architecture as a hybrid of ==shared-disk== (one central data repository all compute can reach) and ==shared-nothing== (MPP clusters where each node processes a portion of the data). [[Three-Layer Architecture]]

Which layer is the only one you create, size and pay for directly?::The Compute layer, through virtual warehouses. Storage and Cloud Services are managed by Snowflake. [[Compute Layer]]

List four jobs of the Cloud Services layer.
?
Authentication and access control, metadata management, query parsing and optimisation, infrastructure management (also transactions and the result cache). [[Cloud Services Layer]]

When is Cloud Services usage actually charged?::Only for the part that exceeds 10 % of the day's virtual warehouse credits, calculated daily in UTC. Serverless compute does not count toward the base. [[Cloud Services Layer]]

How is data physically stored in the Database Storage layer?::As micro-partitions in the cloud provider's object storage: columnar, compressed, encrypted. You see tables, never files. [[Database Storage Layer]]

Can you read Snowflake-stored data directly from the cloud bucket?::No. Data is reachable only through SQL, by unloading to a stage, or by sharing. [[Database Storage Layer]]

A micro-partition holds between ==50== MB and ==500== MB of ==uncompressed== data. [[Micro-partitions]]

Which metadata does Snowflake keep for every column of every micro-partition?::The range of values (min and max), the number of distinct values, null counts, and other optimisation properties. [[Micro-partitions]]

Why are micro-partitions called immutable, and what follows from it?
?
They are never edited in place; DML writes new micro-partitions and retires old ones. That is what makes Time Travel, Fail-safe and zero-copy cloning cheap. [[Micro-partitions]]

What is query pruning and where does it happen?::Skipping micro-partitions whose min/max metadata proves they cannot match the predicate. It happens in Cloud Services before execution, using metadata only. [[Query Pruning]]

Where in Snowsight do you prove that pruning worked?::Query Profile, TableScan node: *Partitions scanned* versus *Partitions total*. A small ratio means good pruning. [[Query Pruning]]

Name two things in a WHERE clause that usually defeat pruning.::Wrapping the filtered column in a function (`TO_CHAR(dt,'YYYY') = '2026'`) and leading-wildcard `LIKE '%x'`. [[Query Pruning]]

When is a clustering key worth defining?::Only on very large tables (multiple terabytes) that are frequently filtered or joined on a column that does not prune naturally. [[Clustering Keys]]

What maintains a clustering key after you define it, and what does it cost?::Automatic Clustering, a serverless service that reclusters in the background and bills credits with no warehouse of yours running, plus extra storage for replaced partitions. [[Clustering Keys]]

A good clustering key column has ==moderate== cardinality: enough distinct values to prune, few enough to group. Use at most ==3 or 4== columns, ordered from lowest to highest cardinality. [[Clustering Keys]]

Coming from Hadoop: what replaces Hive partitions (`PARTITIONED BY dt`)?::Nothing you design. Micro-partitioning is automatic on every column; clustering keys are a later tuning step for multi-TB tables. [[Micro-partitions]]
