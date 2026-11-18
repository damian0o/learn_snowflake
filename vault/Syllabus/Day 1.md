---
tags: [syllabus, day1]
---
# Day 1 - The big picture

Today you learn what Snowflake is made of and how it bills you. By the end you can explain the three layers, size a warehouse, and say why a query that took eight seconds a minute ago now takes none.

**Rhythm (about 3 hours):** read the notes below in order (60 to 90 min) → hands-on in Snowsight (45 min) → flashcards deck `day1` (15 min) → `python3 quiz/quiz.py day1` (20 min) → fill in the "Explain it to a teammate" box at the bottom of each note (10 min).

Before you start: [[Obsidian Setup]], [[Snowflake Account]], [[Quiz Runner]].

## Read in this order

**Architecture (the shape of the thing)**
1. [[What Snowflake Is]]
2. [[Three-Layer Architecture]]
3. [[Cloud Services Layer]]
4. [[Compute Layer]]
5. [[Database Storage Layer]]

**Storage (how data sits)**
6. [[Micro-partitions]]
7. [[Query Pruning]]
8. [[Clustering Keys]]

**Compute (where the money goes)**
9. [[Virtual Warehouse]]
10. [[Warehouse Sizes and Credits]]
11. [[Auto-suspend and Auto-resume]]
12. [[Scaling Up vs Scaling Out]]
13. [[Multi-cluster Warehouse]]

**Caching (why things get fast)**
14. [[Caching]]
15. [[Result Cache]]
16. [[Warehouse Cache]]
17. [[Metadata Cache]]

**Platform (the container around it all)**
18. [[Snowflake Editions]]
19. [[Cloud Providers and Regions]]
20. [[Organizations and Accounts]]
21. [[Snowsight]]
22. [[Credits and Billing]]

## Hadoop bridge

Read the Day 1 rows of [[Hadoop to Snowflake Rosetta Stone]]. The five mappings to carry in your head today:

- HDFS and the Parquet files on it → the [[Database Storage Layer]] and its [[Micro-partitions]]. You no longer design files or directories, and you cannot read them directly.
- YARN queues and Spark executors → [[Virtual Warehouse|virtual warehouses]]. A warehouse is a cluster you can create, resize and switch off in seconds because it holds no data.
- Hive Metastore (plus Ranger and the ResourceManager) → the [[Cloud Services Layer]], which also keeps per-partition statistics and query results.
- Hive partitions and bucketing → automatic micro-partitioning with [[Query Pruning]] on every column; [[Clustering Keys]] only for multi-TB tables.
- Impala and Hive query planning → the optimizer in Cloud Services, which prunes by metadata before any compute starts.

## Hands-on in Snowsight

> [!warning] Not yet executed by the author
> These steps follow the docs but were written without an account to run them on. If a menu name or result differs, note it; it goes into the next revision.

1. **Account and warehouse.** Complete [[Snowflake Account]]: you should have a login and a warehouse `WH_LEARN_XS` (X-Small, auto-suspend 60 s).
2. **Tour.** In [[Snowsight]] find: Projects → Worksheets; Monitoring → Query History; Admin → Warehouses; Admin → Cost Management. Open a new worksheet and set its role to `ACCOUNTADMIN`, warehouse to `WH_LEARN_XS`.
3. **Result cache.** Run this twice:
   ```sql
   SELECT COUNT(*), SUM(L_QUANTITY)
   FROM SNOWFLAKE_SAMPLE_DATA.TPCH_SF1.LINEITEM
   WHERE L_SHIPDATE BETWEEN '1995-01-01' AND '1995-01-31';
   ```
   Open Monitoring → Query History. The second run should show near-zero duration; open its Query Profile and look for the single node **QUERY RESULT REUSE**. See [[Result Cache]].
4. **Pruning.** Open the Query Profile of the *first* run. In the TableScan node read **Partitions scanned** versus **Partitions total**. Now run the same query with `WHERE TO_CHAR(L_SHIPDATE,'YYYY-MM') = '1995-01'` and compare the two numbers. See [[Query Pruning]].
5. **Metadata cache.** Suspend the warehouse (`ALTER WAREHOUSE WH_LEARN_XS SUSPEND;`), then run `SELECT COUNT(*) FROM SNOWFLAKE_SAMPLE_DATA.TPCH_SF1.LINEITEM;`. Check Admin → Warehouses: it should still be suspended. Then add `WHERE L_QUANTITY > 10` and run again; the warehouse resumes. See [[Metadata Cache]].
6. **Warehouse cache.** With the warehouse running, turn result reuse off for the session (`ALTER SESSION SET USE_CACHED_RESULT = FALSE;`) and run the step-3 query twice. In the second Query Profile find the share of bytes scanned **from cache** versus **from remote storage**. See [[Warehouse Cache]].
7. **Sizes.** `ALTER WAREHOUSE WH_LEARN_XS SET WAREHOUSE_SIZE = SMALL;` then back to `XSMALL`. Note that nothing is lost and no restart happens. See [[Scaling Up vs Scaling Out]].
8. **Cost.** Admin → Cost Management: find today's credits for `WH_LEARN_XS`. With a 60 s auto-suspend and an X-Small, the whole session should cost a fraction of one credit. See [[Credits and Billing]].

## Drill

1. Open the Spaced Repetition deck `flashcards/day1` and review every card once (about 65 cards, 10 to 15 minutes).
2. From the repository root run `python3 quiz/quiz.py day1`. Pass bar: 80 %.
3. Below 80 %: reread the notes listed under *Missed concepts*, then `python3 quiz/quiz.py review` until the missed questions come back right, then take `day1` again.
4. `python3 quiz/quiz.py stats` shows your weakest concepts and which note to reread.
5. Finish by writing two sentences in the "Explain it to a teammate" box of at least five notes. Pick the ones that felt shakiest.

## Acceptance

Tick these off, then tick "Day 1" on [[00 Home]]:

- [ ] The vault opens in Obsidian and the graph shows seven colour groups.
- [ ] The Spaced Repetition deck `day1` lists about 65 cards.
- [ ] `python3 quiz/quiz.py day1` runs end to end and shows a score.
- [ ] `python3 tools/check_links.py` and `python3 quiz/quiz.py lint` print no problems.
- [ ] The hands-on steps worked, or you noted which step differed from the description.
- [ ] Quiz score of 80 % or better.

Next: [[Day 2]].
