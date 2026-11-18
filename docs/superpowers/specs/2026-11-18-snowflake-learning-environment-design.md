# Snowflake Learning Environment — Design

Date: 2026-11-18
Status: draft, awaiting approval (revised after builder check and migration context)

## Intent and why

Damianos wants to learn Snowflake well enough to build a warehouse for their team, and then pass the SnowPro Core certification. The team is migrating from a Cloudera platform (Hadoop, HDFS, Hive, Spark) to Snowflake, and Snowflake is new to everyone on it. The team already has a Snowflake account. The material therefore teaches every Snowflake concept next to the Hadoop concept it replaces, and the naming standard is greenfield but written so Hive-era habits translate cleanly.

Damianos is a data engineer. The team's job is pipelines and platform: ingest data into Snowflake, model it, and deliver it to external systems such as Adobe Experience Platform (AEP) and Pega, with more targets expected later. Snowflake is a hub, not a terminus. The material is pitched at an engineer (SQL, scripts, automation), and phase 1 gives outbound delivery the same weight as ingestion. The learning track has three phases:

1. **Foundations (this design):** 2–3 days on Snowflake components and naming conventions, with a syllabus, interactive tests, flashcards and memory techniques.
2. **Team warehouse project:** a working test project on a scenario, built in Snowflake, learning by example. (Separate design, later.)
3. **SnowPro Core prep:** mock exams and gap-filling built on the material from phases 1 and 2. (Separate design, later.)

Everything lives in `/Users/damianospara/playground/learn_snowflake`. Two things must come out of phase 1: an **Obsidian vault** whose graph view genuinely shows how Snowflake concepts relate, and a **working, interactive quiz runner** that scores the learner and re-drills weak spots. Both are built so that phases 2 and 3 extend them rather than replace them.

## Goals

- A 3-day syllabus (about 3 hours per day) covering Snowflake architecture, every major object type, access control, and identifier/naming conventions, ending with a team naming standard the project phase will follow.
- One atomic Obsidian note per concept, heavily cross-linked, so the graph view is informative rather than a hairball or a star.
- Flashcards reviewable with spaced repetition inside Obsidian.
- A command-line quiz with scoring, explanations, per-concept stats, and a Leitner-style review mode for missed questions.
- A memory-techniques note with concrete mnemonics for the hardest-to-remember facts.
- Every quiz question and flashcard points back to the concept note that teaches it.
- Every concept note has a "Coming from Hadoop" line mapping it to the Cloudera-world equivalent, and one Rosetta-stone note collects all those mappings in a single table.
- A trial Snowflake account set up on day 1 and used hands-on each day.

## Non-goals

- Building actual pipelines, Snowpark code, Streamlit, Cortex, dbt and the team scenario. These belong to phase 2. Phase 1 teaches what each component is, what it is for, and how it is named; it does not build with them beyond the day-3 skeleton.
- Configuring AEP or Pega. Phase 1 only explains which Snowflake mechanisms those systems consume (connector pulling from a published schema, files on cloud storage, secure share, JDBC).
- SnowPro exam simulation. Phase 3. The quiz runner is designed so an `exam` mode can be added then, but it is not built now.
- A web UI for the quiz. The CLI is enough and keeps the build small.
- Installing Obsidian or its plugins programmatically. The learner installs them through the Obsidian UI following a short checklist in the vault.

## Anti-goals

What would make this a failure even if it technically works:

- A documentation dump. Notes must be short, in plain words, and each must say why the concept matters and how it connects to neighbours.
- Dangling links or orphan notes. The graph is the product; a link checker enforces this.
- Quiz questions that test trivia not covered by a note, or notes with no question testing them.
- Analogies that mislead. The Hadoop mapping is a bridge, not an equivalence; every mapping line must say where the analogy breaks (e.g. micro-partitions are not Hive partitions you manage).
- Stale facts. Snowflake changes often; every concept note cites the official docs page it was checked against, and the builder verifies against docs.snowflake.com while writing.
- Content that cannot be extended. Phase 2 and 3 notes must slot into the same vault and the same question bank.

## Constraints

- macOS, zsh, Python 3.9.6 via pyenv. No Snowflake tooling installed. Docker available but not needed for this phase.
- Not a git repository today. The builder initialises one as the first step so the vault and quiz are versioned.
- Obsidian community plugins must be installed by the learner (Settings → Community plugins). The vault ships the plugin configuration files so, once installed, the plugin works without further setup.
- Hands-on work in phase 1 uses the Snowsight web UI only. Snowflake CLI is introduced in phase 2.
- Hands-on needs an account where the learner holds `ACCOUNTADMIN` (or at least `SYSADMIN` plus `SECURITYADMIN`), because days 2 and 3 create warehouses, roles and grants. Default: a personal 30-day trial, Enterprise edition, so Time Travel up to 90 days and multi-cluster warehouses can be demonstrated. Alternative: the team's own non-production Snowflake account if the learner has those roles there. The Setup note gives a two-line test (`SHOW GRANTS TO USER`) to decide. Production accounts are never used for exercises.

## Approaches considered

The vault and syllabus are common to all three; they differ in how tests and flashcards work.

1. **Everything inside Obsidian.** Flashcards via the Spaced Repetition plugin; tests as markdown with folded answer callouts. One tool, every card in the graph, but no scoring, no tracking of weak areas.
2. **Obsidian vault + small quiz runner in the project folder (chosen).** Flashcards still in the vault via the Spaced Repetition plugin, so the graph stays rich. Tests are a YAML question bank plus a small Python CLI that asks, scores, records, and re-drills. One script to maintain; real interactivity; the bank grows straight into SnowPro mock exams in phase 3.
3. **Obsidian vault + Anki.** Best spaced repetition engine, but a third app and cards vanish from the graph.

Damianos chose approach 2 because it serves both "nice graph" and "working interactive tests", and the runner becomes the exam simulator later.

## Decisions made

### Folder layout

```
learn_snowflake/
  README.md                     how to use this folder (open vault, install plugin, run quiz)
  .gitignore                    quiz/results/, .obsidian/workspace*.json, caches
  docs/superpowers/specs/       this design and later ones
  docs/superpowers/plans/       implementation plans
  vault/                        <- open THIS folder as the Obsidian vault
    .obsidian/                  app.json, graph.json (colour groups), community-plugins.json,
                                plugins/obsidian-spaced-repetition/data.json (settings only, no plugin code)
    00 Home.md                  dashboard: links to syllabus days, progress checklist, how-to
    Syllabus/                   Day 1.md, Day 2.md, Day 3.md
    Concepts/                   one note per concept (architecture, objects, security)
    Migration/                  Hadoop to Snowflake Rosetta Stone.md plus a few deeper mapping notes
    Conventions/                identifier rules + the team naming standard, one note per object class
    Flashcards/                 one note per topic cluster (4-5 per day, e.g. "Cards - Virtual Warehouses"),
                                tagged #flashcards/dayN so the plugin shows one deck per day
    Memory/                     Memory Techniques.md, Mnemonics.md, Cheat Sheet Day N.md
    Setup/                      Trial Account.md, Obsidian Setup.md, Quiz Runner.md
    Templates/                  Concept.md, Convention.md
    Project/                    placeholder README, filled in phase 2
    Certification/              placeholder README, filled in phase 3
  quiz/
    quiz.py                     the CLI entry point
    quizlib/                    bank loading, validation, question types, Leitner scheduler, stats
    bank/                       day1.yaml, day2.yaml, day3.yaml, cumulative.yaml
    results/progress.json       learner progress (gitignored)
    requirements.txt            pyyaml, pytest
    tests/                      pytest suite for quizlib
  tools/
    check_links.py              fails on dangling wikilinks, orphan notes, and quiz->note references that don't resolve
  project/
    README.md                   phase 2 lives here
    setup/00_team_skeleton.sql  day-3 artifact: the team skeleton named by the standard (see Day 3)
    setup/99_teardown.sql       drops everything the skeleton created
```

### The vault

**Note anatomy.** Every concept note follows `Templates/Concept.md`:

```
---
tags: [concept, dayN, <area>]
docs: <official docs URL checked>
---
# <Concept name>

**In one sentence:** ...
**Why it matters:** ...

**Coming from Hadoop:** <the Cloudera-world thing this replaces, and where the analogy breaks>

## How it works
(short, plain words, a diagram in text if it helps)

## Gotchas / exam traps
- ...

## Related
[[...]] [[...]]  (at least 3 outgoing links; the builder keeps these meaningful)

## Explain it to a teammate (fill in yourself)
> (empty; the learner writes 2 sentences — Feynman technique)
```

**Linking rules** so the graph is informative:

- Syllabus day notes link to every concept covered that day, grouped in reading order.
- Concept notes link up (to the parent idea), sideways (to siblings), and down (to specifics). Example: `Virtual Warehouse` links to `Three-Layer Architecture`, `Warehouse Sizes and Credits`, `Multi-cluster Warehouse`, `Caching`, `Resource Monitor`.
- Convention notes link to the concept they name (e.g. `Naming - Warehouses` → `Virtual Warehouse`). Note titles never contain colons, since Obsidian does not allow them in file names.
- The Rosetta Stone note links to every concept it maps, and each concept's "Coming from Hadoop" line links back to it, so the graph shows the Hadoop bridge as its own coloured cluster (`migration` tag).
- Flashcards contain wikilinks to the concept note in the answer side, so cards hang off their concept in the graph. Flashcard notes are split per topic cluster (4-5 notes per day, each covering 3-6 related concepts) rather than one note per day: one note per day would give three yellow hubs with 25 edges each, which is the star shape the anti-goals forbid. Builder's call.
- Tags give the graph colour groups: `concept`, `convention`, `flashcards`, `syllabus`, `memory`, `setup`, `migration`. `graph.json` ships with these colour groups preset (flashcards in yellow).
- `tools/check_links.py` fails if any wikilink has no target or any note in `Concepts/` or `Conventions/` has zero inbound links.

**Flashcards** use the Obsidian Spaced Repetition plugin syntax: single-line `Question::Answer`, multi-line with `?` separator, cloze with `==highlight==`. Every card note for a day is tagged `#flashcards/dayN` so the plugin treats each day as one deck. About 35–45 cards per day across that day's 4-5 card notes. The plugin stores scheduling as HTML comments in the note; those are committed so progress survives.

**Memory techniques note** covers, with concrete examples tied to Snowflake: spaced repetition (the plugin schedule), active recall (cards and quiz), the Feynman section in every note, chunking (the object hierarchy tree), a memory palace (the "Snowflake building": storage in the basement, compute on the office floors, cloud services on the roof), interleaving (the cumulative quiz), and one-page cheat sheets per day as the "yellow card" to stick on the wall. The `Mnemonics.md` note holds acronyms and images for the hard lists: the six system roles in hierarchy order, table types vs Time Travel vs Fail-safe retention, the three stage kinds and their `@~`, `@%`, `@` prefixes, the three caches and where each lives, warehouse sizes and credits per hour, and the Snowflake editions. The builder invents the actual mnemonics; they must be short and visual.

### The syllabus

Each day follows the same rhythm, stated at the top of the day note: read concept notes (60–90 min) → hands-on in Snowsight (45 min) → flashcards (15 min) → `quiz.py dayN` (20 min) → fill in the "Explain it to a teammate" sections (10 min).

**Day 1 — The big picture.** What Snowflake is (cloud data platform, fully managed SaaS, separation of storage and compute). Three-layer architecture: Cloud Services, Query Processing (virtual warehouses), Database Storage; why it is called a hybrid of shared-disk and shared-nothing. Micro-partitions and clustering metadata, partition pruning. Virtual warehouses: sizes and credits, auto-suspend/resume, scaling up vs scaling out, multi-cluster warehouses and scaling policies. The three caches: result cache, warehouse local disk cache, metadata cache. Editions (Standard, Enterprise, Business Critical, Virtual Private Snowflake) and what each unlocks. Cloud providers and regions. Organisation → account. Hadoop bridge for the day: HDFS and Parquet/ORC files on it → the storage layer; YARN queues and Spark executors → virtual warehouses (and why a warehouse is not a cluster you keep warm); Hive Metastore → Cloud Services metadata; Hive partitions and bucketing → micro-partitions and clustering keys; Impala/Hive query planning → the optimizer and pruning. Hands-on: create the trial account, tour Snowsight, create a warehouse, run a query twice and observe the result cache in Query Profile.

**Day 2 — Objects and security.** Object hierarchy: account → database → schema → schema objects. Tables: permanent, transient, temporary, external, plus a one-paragraph mention of dynamic, hybrid and Iceberg tables. Views: standard, secure, materialized. Stages: internal (user, table, named) and external; file formats; `COPY INTO` at a conceptual level; Snowpipe. Streams and tasks. Sequences, UDFs, stored procedures. Time Travel, Fail-safe, zero-copy cloning. **Getting data out**, as its own cluster: unloading with `COPY INTO <location>` and storage integrations; secure data sharing (shares, listings, reader accounts) as the zero-copy way to hand data to another Snowflake account; drivers and connectors (JDBC/ODBC, Kafka connector, Spark connector, Python connector) as the way systems like Pega read Snowflake; external access integrations and network rules for calling outside APIs; a one-paragraph positioning of Snowpark. Each outbound mechanism is tagged with which kind of consumer it suits (a SaaS platform with a Snowflake source connector, such as AEP; a JDBC consumer, such as Pega; a file-based consumer; another Snowflake account). Access control: RBAC and DAC, securable objects, privileges and grants, ownership, future grants, the system roles (ORGADMIN, ACCOUNTADMIN, SECURITYADMIN, USERADMIN, SYSADMIN, PUBLIC) and the recommended role hierarchy. Users and authentication at a glance. Resource monitors. Hadoop bridge for the day: Hive database → Snowflake schema (and the extra database level above it); Hive external table on HDFS → stage plus `COPY INTO`, or an external table; Sqoop and Flume → `COPY INTO` and Snowpipe; Oozie workflows → tasks; Spark structured streaming CDC → streams; Hive UDFs → Snowflake UDFs; HDFS snapshots and trash → Time Travel and Fail-safe; `hdfs dfs -cp` of a whole table → zero-copy clone; Ranger / Sentry policies → RBAC, roles and grants. Hands-on: create a database, schema, the three table kinds, a view, a named stage, clone a table, drop and undrop it, create a small role hierarchy and grant it.

**Day 3 — Naming conventions and the team standard.** Identifier rules: unquoted identifiers (upper-cased, letters/digits/underscore/dollar, length limit), quoted identifiers (case-sensitive, any characters), the pitfalls that follow, `QUOTED_IDENTIFIERS_IGNORE_CASE`, fully qualified names, reserved words. A short note on how Hive naming habits translate: Hive database names become schemas, HDFS path hierarchies (`/data/raw/<source>/<table>`) become `DATABASE.SCHEMA.TABLE`, Hive partition columns become ordinary columns, and `db_name.table_name` lowercase habits meet Snowflake's upper-casing of unquoted identifiers. Then the **team naming standard**, one note per object class, each with the rule, examples, and the reasoning: databases per environment and domain, schema layers (RAW / STAGING / INTERMEDIATE / MARTS / PUBLISH, where PUBLISH holds the stable, contract-like views and tables that external systems read, with the medallion names as the alternative), table prefixes (`DIM_`, `FCT_`, `STG_`) and suffixes (`_HIST`), views, secure and materialized views, stages (inbound and outbound), file formats, pipes, streams, tasks, sequences, procedures and functions, integrations (storage, API, notification, external access) and shares, warehouses (`WH_<TEAM>_<PURPOSE>_<SIZE>`), the two-tier role model (access roles per database/schema with R / RW / OWNER, functional roles per job), users and service users, resource monitors, column conventions (`snake_case`, `_ID`, `_AT`, `_DATE`, `IS_`, `_AMT`, `_CNT`), comments and tags on every object. Hands-on: run `project/setup/00_team_skeleton.sql` in Snowsight. Its scope (builder's call): one resource monitor, one warehouse, one `DEV` database with the five schema layers, access roles with `R` and `RW` per schema layer, two functional roles (`ANALYST`, `ENGINEER`) granted the access roles, future grants so new tables inherit permissions, and the role tree hung under `SYSADMIN`. Everything uses `IF NOT EXISTS` so it can be re-run, and `99_teardown.sql` reverses it. It needs `ACCOUNTADMIN` on the trial, which the learner has. It is the first real artifact of phase 2 and phase 2 extends it with `PROD`. Cumulative quiz covering all three days.

### The quiz runner

**Language and dependencies.** Python 3.9-compatible, stdlib plus PyYAML. Tests with pytest. No other dependencies.

**Question bank format** (YAML, one file per day plus `cumulative.yaml`):

```yaml
- id: d1-arch-001
  type: mcq            # mcq | multi | tf | fill
  concept: Three-Layer Architecture    # must match a note title in vault/Concepts or Conventions
  tags: [day1, architecture]
  difficulty: 1        # 1 recall, 2 understanding, 3 application
  prompt: Which layer of Snowflake's architecture runs queries?
  options:             # mcq/multi only
    - Cloud Services
    - Query Processing
    - Database Storage
  answer: Query Processing          # mcq: one option; multi: list; tf: true/false; fill: list of accepted strings
  explanation: Virtual warehouses live in the Query Processing layer; Cloud Services plans and coordinates.
```

Target size: 30 questions per day, 20 in `cumulative.yaml` written as application questions that mix days, about 110 in total. Each day includes 4-6 "Hadoop bridge" questions of the form "on Cloudera you did X; what is the Snowflake way?" tagged `migration`. Difficulty mix per day roughly 50% recall, 35% understanding, 15% application.

**Commands.**

- `python3 quiz/quiz.py day1` — all questions for that day, options shuffled, immediate feedback with explanation and the note to read, score at the end.
- `--n 10` and `--tag architecture` filters; `--seed` for reproducible runs.
- `python3 quiz/quiz.py review` — Leitner mode. Three boxes. A new or wrongly answered question sits in box 1; each correct answer moves it up one box; box 3 questions are only re-asked occasionally. Review asks box 1 first, then box 2, then a sample of box 3.
- `python3 quiz/quiz.py stats` — accuracy per concept and per day, the five weakest concepts with the note to reread, and the Leitner box distribution.
- `python3 quiz/quiz.py lint` — validates the bank: unique ids, valid types, answers that are in the options, concept names that resolve to a vault note, every concept note having at least one question.
- `python3 quiz/quiz.py cumulative` — the day-3 cumulative test.

**Answer matching** for `fill`: case-insensitive, whitespace-trimmed, accepts any string in the answer list. `multi` requires the exact set. The user answers with letters for options, `t`/`f` for true/false.

**Progress** is stored in `quiz/results/progress.json`: per question id, box number, times asked, times correct, last asked timestamp, last result. Gitignored.

**Testing.** `quizlib` is pure logic with the terminal interaction isolated in one thin module, so pytest covers bank loading and validation, answer matching, shuffling with a seed, Leitner transitions, stats aggregation, and progress persistence. The CLI is checked by a smoke test feeding scripted answers through stdin.

### Setup notes

- `Setup/Snowflake Account.md`: first, the two-line check on the team account (which roles the learner holds; is it non-production). If it passes, use it. Otherwise sign up for a trial at signup.snowflake.com, pick Enterprise edition and a nearby cloud region, verify email, note the account identifier, first login to Snowsight.
- `Setup/Obsidian Setup.md`: open `vault/` as a vault, trust the folder, enable community plugins, install "Spaced Repetition" (and optionally "Dataview" for the progress table on Home), open the graph and confirm the colour groups appear.
- `Setup/Quiz Runner.md`: `pip install -r quiz/requirements.txt`, run `quiz.py lint`, run `quiz.py day1`.

### Who verifies what

The builder has no Snowflake account and cannot drive the Obsidian UI. So:

- The builder runs everything automatable: the link checker, the bank linter, pytest, and a syntax read-through of the SQL against the docs.
- The SQL scripts and the Snowsight click-paths are marked in the notes as "not yet executed by the author"; day 1 ends with a learner acceptance step ("open the vault, confirm the graph and the decks, run `quiz.py day1`") and day 3 ends with another ("run the skeleton, report anything that fails").
- If the learner is willing to share a connection to the trial account (a `~/.snowflake/connections.toml` entry), the builder can execute the skeleton script with Snowflake CLI and remove those markers. Optional, not assumed.

### Delivery sequencing

Built and handed over in three increments, Day 1 first, so studying can start before days 2 and 3 are written. The first increment contains the whole skeleton (vault config, templates, Home, Setup notes, quiz runner with tests, link checker) plus all Day 1 content. Increments 2 and 3 add content only. Because of this, `check_links.py` and `quiz.py lint` accept a `--day N` scope so that a partially built vault passes its own checks; the full unscoped run is the final gate.

### Verification before done

- `python3 tools/check_links.py` passes: no dangling links, no orphan concept or convention notes, every quiz `concept` resolves.
- `python3 quiz/quiz.py lint` passes.
- `pytest quiz/tests` passes.
- Manual: open the vault in Obsidian, graph shows the colour groups and the flashcard notes hanging off their concepts; the Spaced Repetition plugin detects the three decks; `quiz.py day1` runs end to end.
- Each concept note's `docs:` link was opened and the facts in the note checked against it during writing.

## What's left to the builder

- The exact wording of notes, cards, questions and mnemonics, within the anatomy and sizes above.
- Graph colour choices beyond "flashcards are yellow".
- The exact split of concepts into notes, as long as every item named in the syllabus above has a home and the link rules hold.
- Internal structure of `quizlib`.
- The scenario for phase 2 is explicitly not decided here; the day-3 skeleton script uses the generic names from the standard (team placeholder `ANALYTICS`) and phase 2 may rename.

- The phase 2 scenario is not decided here, but given the migration and the team's job it will most likely be "move one Hive/Parquet dataset from the data lake into Snowflake, model it, and publish a feed that AEP and Pega can consume". The day-3 skeleton (with its PUBLISH layer) should not preclude that.

## Resolved questions

- Naming standard: greenfield. The team has a Snowflake account but no conventions yet; they come from Cloudera (Hadoop, HDFS, Hive, Spark). Day 3 invents the standard and shows how Hive-era habits translate.
- Audience: a data engineer building ingestion-to-delivery pipelines. Outbound delivery to external platforms (AEP, Pega, future systems) is a first-class topic, not an afterthought.
