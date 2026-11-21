---
tags: [roadmap]
---
# Roadmap

Three phases, each with its own design document in `docs/superpowers/specs/`. Phase 1 is in progress. Durations are rough and depend on study pace; dates are written down when a phase starts.

## Where we are (19 Nov 2026)

- Skeleton done and stable: vault, quiz runner, link checker, Docker images, checks gate, CI workflow.
- Publishing prepared: the vault builds into a public website with Quartz via GitHub Actions and GitHub Pages (see the repo README). Goes live on the first push to GitHub.
- [[Day 1]] content complete and reviewed. [[Day 2]] and [[Day 3]] are stubs.
- Open verification: the Day 1 Snowsight hands-on steps have not been executed yet.

## Phase 1 - Foundations (1 to 2 weeks)

**Learner**

- [ ] Study [[Day 1]]: read order, flashcards deck `day1`, quiz (`docker compose run --rm quiz day1`).
- [ ] Day 1 hands-on in Snowsight using the account from [[Snowflake Account]]. Report any step that does not match the UI.
- [ ] Fill in "Explain it to a teammate" on at least five concept notes.
- [ ] Repeat for Day 2 and Day 3 as they land.

**Builder**

- [ ] Increment 2, [[Day 2]]: object hierarchy, table and view kinds, stages and `COPY INTO`, Snowpipe, streams and tasks, Time Travel, Fail-safe, cloning, RBAC and the role hierarchy, resource monitors. "Getting data out" as its own cluster: unloading, secure data sharing, connectors for consumers such as Pega, external access for calling APIs such as AEP. Adds Day 2 rows to the [[Hadoop to Snowflake Rosetta Stone]], Day 2 [[Mnemonics]], flashcards and `quiz/bank/day2.yaml`.
- [ ] Increment 3, [[Day 3]]: identifier rules, Hive habit translations, one convention note per object class with the RAW / STAGING / INTERMEDIATE / MARTS / PUBLISH layers, warehouse and role naming. Ships `project/setup/00_team_skeleton.sql`, `99_teardown.sql` and `quiz/bank/cumulative.yaml`.
- [ ] Full unscoped gate (`checks/run.sh`) and the three Spaced Repetition decks confirmed in Obsidian.

**Exit criterion:** cumulative quiz at 80 % or better, and the team skeleton script runs clean in your account.

## Phase 2 - Team warehouse project (3 to 4 weeks)

Starts with a brainstorming session and a design document. Proposed scenario, open to change: take one Hive or Parquet dataset from the lake, land it in RAW through a stage, model it through STAGING to MARTS, expose a PUBLISH view, and deliver it two ways: a Snowflake source connector for AEP and a JDBC-style read for Pega. Lives in [[Project]].

Milestones:

- Environment: extend the skeleton with `PROD`, warehouses per workload, resource monitors, service users.
- Ingest: file landing, `COPY INTO`, then Snowpipe for continuous load. Decide where lake-side Spark stops and Snowflake starts.
- Transform: streams and tasks or a tool such as dbt for the layer pipeline. Tool choice is a phase 2 decision.
- Publish: contract views, data sharing or unload, one end-to-end run to a real or mocked AEP and Pega target.
- Engineering hygiene: fakesnow (DuckDB-backed Snowflake emulator) for unit tests, real Snowflake for the integration run, both wired into the checks gate and CI.
- Team onboarding: the Project section grows so the rest of the team can read it, since Snowflake is new to everyone.

## Phase 3 - SnowPro Core prep (2 to 3 weeks)

Own design document. Builds on phases 1 and 2 rather than replacing them. Lives in [[Certification]].

- Gap analysis of the exam domains against the vault; new notes for anything missing (data protection details, performance tuning specifics, account usage views).
- Quiz runner gains an `exam` mode: timed, 100 questions, weighted by official domain percentages, explanations only at the end.
- Two or three full mock exams, Leitner review of everything missed, then book the exam.

## Decisions waiting on the learner

- Does the Day 1 hands-on match the real Snowsight UI?
- Go-ahead to plan increment 2. Nothing else blocks it.
- Phase 2: real AEP and Pega sandboxes, or mocked targets?

## Local alternatives to Snowflake

Snowflake has no local edition. For phase 2 tests: fakesnow (open source, Python) or LocalStack for Snowflake (commercial, Docker). For offline SQL practice: DuckDB, whose dialect is the closest match. None of these teach Snowflake-specific components; use the real account for Days 1 to 3.

Back to [[00 Home]].
