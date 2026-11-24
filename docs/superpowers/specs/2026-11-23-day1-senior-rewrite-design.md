# Day 1 Senior Rewrite — Design

Amends `2026-11-18-snowflake-learning-environment-design.md`. Everything not restated here still holds (folder layout, linking rules, quiz runner, checks).

## Intent and why

Day 1 as shipped reads as a reading list plus a lab, and the 22 concept notes explain fundamentals the learner already has. The learner is a senior data engineer: storage/compute separation, columnar formats, clusters and schedulers need no motivation. What they want from each note is the Snowflake-specific mechanism, the numbers, a way to observe it, and what it costs. Cost visibility in particular must be concrete: which view, which column, which query.

## Goals

- Every Day 1 concept note rewritten at senior pitch: diagram or table first, prose last, no basics, no benefits language.
- Cost is a one-line section in every note (how the subject is metered, which view and column). The full metrics-and-price picture is one capstone note at the end of phase 1, not a Day 1 topic.
- Day 1 note becomes a per-layer article built around one diagram of a query's path.
- The new pitch is enforced by a check, so Days 2 and 3 inherit it.

## Non-goals

- Exam-wording depth (phase 3). Numbers and defaults yes; "which option is the distractor" no.
- Day 2 and Day 3 content. They are written to this anatomy when their increments come.
- Renaming notes. Titles, folders, tags and quiz `concept` references stay valid.

## Anti-goals

- A note that explains why separating storage from compute is a good idea, what a cluster is, or what columnar storage is.
- Sentences that could appear in a vendor brochure ("elastic", "seamless", "effortlessly").
- Facts without a source. Every number comes from the doc page named in the note's `docs:` frontmatter or a page linked inline.

## Approaches considered

1. **Rewrite the 22 notes in place, Day 1 as a per-layer article.** Chosen. Fixes the complaint where it lives, keeps the graph and quiz intact.
2. Keep notes, add "Internals" notes. Rejected: basics stay in the reading path, near-duplicate nodes in the graph.
3. One long guide, notes untouched. Rejected: abandons the atomic-note graph.

## The pitch (style contract)

Audience: senior data engineer, Cloudera background, new to Snowflake only.

- **Prose budget:** at most 300 words of prose per concept note and 900 per syllabus day note. Prose is every word outside code fences, Mermaid blocks, tables, frontmatter and the Explain box. List items and callouts count: bullets are the medium, so they are budgeted.
- **Show, then tell:** if a thing has a structure or a sequence, it is a Mermaid diagram (`flowchart` or `sequenceDiagram`). If it has values, it is a table. Prose only for what neither can carry.
- **Official names only:** Cloud Services layer, query processing layer, virtual warehouse, micro-partition, result reuse, warehouse (local disk) cache, metadata, clustering depth, credit, `ACCOUNT_USAGE`. No invented shorthand.
- **No basics:** nothing the audience assumption already covers. No Hadoop comparison inside notes: the Cloudera-to-Snowflake mapping lives in one separate article (today the Rosetta Stone; expanded into a standalone "Hadoop to Snowflake" article in increment 3), linked once from Home and from each Day note.
- **Observable:** every note has at least one thing to run and the output to expect.
- **Cost:** every note says how its subject is metered and where that shows up (view and column), or states "no direct cost" explicitly.

## Concept note anatomy (replaces the Day 1 template)

```markdown
---
tags: [concept, day1, <area>]
docs: <primary doc URL>
---
# <Title>

<One sentence, precise, no adjectives.>

```mermaid
<flowchart or sequence when the subject has structure; omit only if a table carries it>
```

## Numbers
| Thing | Value | Source |      ← defaults, limits, units; Source = doc page

## How it works
- ≤ 8 bullets, arrows allowed (A → B), mechanism not motivation

## Probe
```sql
-- what to run
```
Where to look (Snowsight path or view) → what you should see.

## Cost
How it is metered → view.column. Or "No direct cost; see [[...]]".

## Traps
- ≤ 3

**vs Cloudera:** one line of differences. See [[Hadoop to Snowflake Rosetta Stone]].

## Related
- ≥ 3 wikilinks

## Explain it to a teammate (fill in yourself)
>
```

`vault/Templates/Concept.md` is replaced by this.

`vault/Templates/Convention.md` becomes: Rule → Pattern → Examples (table) → Why (at most 3 bullets; a naming standard's reasoning is substance, not motivation) → Probe (a query against `INFORMATION_SCHEMA` or `SHOW` that proves the rule holds) → Cost (optional; most rules have none) → one `vs Hive` line → Related. Same 300-word budget. Required headings for `Conventions/`: Rule, Examples, Why, Probe, Related.

## Phase 1 capstone (built in increment 3, specified here): `Metrics and Price Evaluation`

Lives in `vault/Syllabus/` as the last reading of Day 3, tagged `[syllabus, day3, cost]`. Purpose: at the end of phase 1 the learner can (a) read the metrics of what their account did, (b) read the price it came to, (c) estimate the price of the team setup from `project/setup/00_team_skeleton.sql`, and (d) know where each number lives.

- **Metrics (credits, bytes):** `ACCOUNT_USAGE.WAREHOUSE_METERING_HISTORY` (hourly, ≤ 180 min latency, 365 d; `CREDITS_USED_COMPUTE`, `CREDITS_ATTRIBUTED_COMPUTE_QUERIES` → idle = compute − attributed), `QUERY_ATTRIBUTION_HISTORY` (per query, ≤ 8 h, excludes idle and queries ≤ ~100 ms), `QUERY_HISTORY` (≤ 45 min; `BYTES_SCANNED`, `PERCENTAGE_SCANNED_FROM_CACHE`, `PARTITIONS_SCANNED/TOTAL`), `STORAGE_USAGE`, `DATA_TRANSFER_HISTORY`; `INFORMATION_SCHEMA.WAREHOUSE_METERING_HISTORY()` for "right now" (6 months back, needs `ACCOUNTADMIN` or `MONITOR USAGE`).
- **Billed credits:** `METERING_DAILY_HISTORY` per day and service type; `CREDITS_BILLED = CREDITS_USED_COMPUTE + CREDITS_USED_CLOUD_SERVICES + CREDITS_ADJUSTMENT_CLOUD_SERVICES` (the 10 % rule written back as a negative number). Everything else, Snowsight included, is pre-adjustment.
- **Price (currency):** `SNOWFLAKE.ORGANIZATION_USAGE.USAGE_IN_CURRENCY_DAILY` and `RATE_SHEET_DAILY` (effective price per credit and per TB for this account's edition, cloud and region). Needs `ORGADMIN` or a grant; the note says what to ask for. Verified at build time against the docs, including latency and which role sees them.
- **Snowsight:** Admin » Cost management: Account overview, Consumption (filter by warehouse, usage type), Budgets, Resource monitors. Which screen answers which question.
- **Price evaluation worksheet:** one query that joins credits by warehouse to the rate sheet to give currency per warehouse per day, and a short table to estimate the team setup: warehouses × size × expected hours/day × credit price, plus storage TB × rate, plus egress estimate for the outbound feeds. Filled with the learner's own numbers, not vendor list prices.
- **Guardrails pointer:** resource monitors and budgets (Day 2 notes) as where limits are set.
- **Access fallback:** `GRANT DATABASE ROLE SNOWFLAKE.USAGE_VIEWER TO ROLE <role>` for `ACCOUNT_USAGE`; `GRANT MONITOR USAGE ON ACCOUNT TO ROLE <role>` for the table function; `ORGANIZATION_USAGE` via the organization account or `ORGADMIN`.

The six query drafts for this note are in Appendix A so they survive until increment 3.

## Day 1 note

- Opening: one Mermaid `flowchart` of a query's path: client → Cloud Services (auth → parse → optimise → prune → result reuse check) → warehouse (SSD cache → remote storage) → result → result cache; the credit meter drawn on the warehouse box, the 10 % rule on Cloud Services.
- One section per layer and theme (Cloud Services, Storage, Compute, Caching, Platform, Cost), each 3 to 6 bullets with the wikilinks, no narrative paragraphs.
- No Hadoop bridge section; one pointer to the Rosetta Stone in the preamble.
- Hands-on: the existing lab with the author's warning kept. Step 8 (Cost Management) stays as the only cost step and points forward to the capstone note.
- Drill and Acceptance keep their steps; card counts are updated to the new totals.

## Flashcards and quiz

- Flashcards: existing decks keep their cards; cards that quoted removed prose are reworded, not deleted. New cards only for mechanisms and numbers the rewrite adds.
- Quiz: existing questions reworded where the note text changed; new `d1-*` questions for added mechanisms. Lint rules unchanged. Cost-view questions belong to the capstone in increment 3.

## Enforcement: `tools/check_pitch.py`

Fails the gate when a concept or convention note breaks the contract:

- prose words > 300 (`Concepts/`, `Conventions/`) or > 900 (`Syllabus/`), counted as the pitch defines prose;
- a required heading missing: Numbers, How it works, Probe, Cost, Traps, Related under `Concepts/`; Rule, Examples, Why, Probe, Related under `Conventions/`;
- a banned phrase present (configurable list: "seamless", "effortless", "elastic", "in one sentence", "why it matters").

Scoped by `--day N` like the other checks. Added to `checks/run.sh` after `check_links`.

## Verification before done

- Each number in each note traced to a doc page during writing (the `docs:` link or an inline link).
- `checks/run.sh` green, including the new pitch check over all Day 1 notes.
- Local Quartz build renders every Mermaid block (no raw ```` ```mermaid ```` text in `public/`).
- Learner: reads two rewritten notes and says whether the pitch is right before the remaining twenty are written (first two notes are the checkpoint).

## What's left to the builder

- Exact diagrams per note.
- Which existing flashcards and questions need rewording.
- The banned-phrase list beyond the five above.

## Resolved questions

- **Day 1 budget vs an unchanged lab?** The lab stays; the syllabus budget is 900 words and lists count. Builder's call.
- **Convention template?** Decided above; `Why` survives capped at three bullets. Builder's call.
- **Which role runs the cost queries?** Capstone concern (increment 3): assume `ACCOUNTADMIN`, name the grants as the fallback. Builder's call.
- **A money note on Day 1?** No. Cost is a one-line section per note on Day 1; the metrics and price evaluation come once, at the end of phase 1. Learner's call.

- **Keep the "Explain it to a teammate" box?** Yes. It is the only part of a note the learner writes.
- **Keep the "Coming from Hadoop" paragraph?** No, and (learner's call, 2026-11-24) no per-note `vs Cloudera` line either. The comparison is one separate article; notes never repeat it.
- **Rename notes to match official terms?** No renames; `Compute Layer` already says "query processing layer" in its first line.

## Appendix A: query drafts for the capstone note

Column names, latencies and retention checked against the Snowflake docs on 2026-11-23. Re-verify at build time.

```sql
-- 1. What did today cost, per warehouse, right now (no latency)?
SELECT warehouse_name, SUM(credits_used) AS credits
FROM TABLE(INFORMATION_SCHEMA.WAREHOUSE_METERING_HISTORY(DATEADD('hour', -24, CURRENT_TIMESTAMP())))
GROUP BY 1 ORDER BY 2 DESC;

-- 2. Last 7 days per warehouse, compute vs cloud services
SELECT warehouse_name,
       ROUND(SUM(credits_used_compute), 3)        AS compute,
       ROUND(SUM(credits_used_cloud_services), 3) AS cloud_services
FROM SNOWFLAKE.ACCOUNT_USAGE.WAREHOUSE_METERING_HISTORY
WHERE start_time >= DATEADD('day', -7, CURRENT_TIMESTAMP())
GROUP BY 1 ORDER BY 2 DESC;

-- 3. How much of that was idle (running, no query)?
SELECT warehouse_name,
       ROUND(SUM(credits_used_compute), 3)                                             AS compute,
       ROUND(SUM(credits_attributed_compute_queries), 3)                               AS attributed,
       ROUND(SUM(credits_used_compute) - SUM(credits_attributed_compute_queries), 3)   AS idle
FROM SNOWFLAKE.ACCOUNT_USAGE.WAREHOUSE_METERING_HISTORY
WHERE start_time >= DATEADD('day', -7, CURRENT_TIMESTAMP())
GROUP BY 1 ORDER BY idle DESC;

-- 4. What will the invoice say, per day?
SELECT usage_date, service_type, credits_used, credits_adjustment_cloud_services, credits_billed
FROM SNOWFLAKE.ACCOUNT_USAGE.METERING_DAILY_HISTORY
WHERE usage_date >= DATEADD('day', -7, CURRENT_DATE())
ORDER BY usage_date DESC, credits_billed DESC;

-- 5. Ten most expensive queries, last 7 days
SELECT query_id, warehouse_name, user_name, ROUND(credits_attributed_compute, 4) AS credits, query_text
FROM SNOWFLAKE.ACCOUNT_USAGE.QUERY_ATTRIBUTION_HISTORY
WHERE start_time >= DATEADD('day', -7, CURRENT_TIMESTAMP())
ORDER BY credits DESC LIMIT 10;

-- 6. Why was one query expensive?
SELECT bytes_scanned, percentage_scanned_from_cache, partitions_scanned, partitions_total,
       execution_time, credits_used_cloud_services
FROM SNOWFLAKE.ACCOUNT_USAGE.QUERY_HISTORY
WHERE query_id = '<id>';
```
