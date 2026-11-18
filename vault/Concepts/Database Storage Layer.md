---
tags: [concept, day1, storage]
docs: https://docs.snowflake.com/en/user-guide/intro-key-concepts
---
# Database Storage Layer

**In one sentence:** Database Storage is Snowflake-managed cloud object storage holding one compressed, columnar, encrypted copy of every table as micro-partitions.

**Why it matters:** You never tune files, formats or directories again, and you pay for compressed bytes. But you also cannot reach the files directly, which changes how data gets in and out.

**Coming from Hadoop:** HDFS plus the Parquet or ORC files you laid out in it. The analogy breaks in two places: you chose Parquet row-group sizes, compression and directory partitioning, Snowflake chooses all of that for you; and you could `hdfs dfs -get` a file, while Snowflake storage is reachable only through SQL (or by unloading to a stage) (see [[Hadoop to Snowflake Rosetta Stone]])

## How it works

When you load data, Snowflake rewrites it into its own internal format: **columnar, compressed, encrypted**, split into [[Micro-partitions]] of 50 to 500 MB uncompressed. These land in the cloud provider's object storage (S3, Azure Blob, Google Cloud Storage) in the region of your account.

Snowflake manages everything about the stored data: organisation, file size, structure, compression, metadata and statistics. You see tables and columns; you never see files.

What the storage layer gives you:

- **One copy, many readers.** Every [[Virtual Warehouse]] reads the same bytes.
- **Immutability.** Micro-partitions are never edited in place. `UPDATE` and `DELETE` write new partitions and retire old ones, which is what makes Time Travel, Fail-safe and zero-copy cloning possible (Day 2).
- **Statistics for free.** Each micro-partition carries min/max per column and more, which the optimizer uses for [[Query Pruning]].
- **Billing by compressed size.** Storage costs a flat rate per TB per month, measured as the average daily on-disk (compressed) bytes, including Time Travel and Fail-safe retention.

## Gotchas / exam traps

- You cannot access Snowflake-stored data as files. Data leaves through SQL, `COPY INTO <stage>` or sharing, never by reading the bucket.
- Storage is billed on compressed bytes. Columnar compression often gives 3 to 5 times reduction over raw CSV.
- Storage includes historical data kept for Time Travel and Fail-safe, so a table you keep rewriting costs more than its current size.

## Related

- [[Three-Layer Architecture]]
- [[Micro-partitions]]
- [[Query Pruning]]
- [[Compute Layer]]
- [[Credits and Billing]]

## Explain it to a teammate (fill in yourself)

> 
