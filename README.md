# Learn Snowflake

A self-paced Snowflake learning environment for a data engineer moving a team from Cloudera (Hadoop, HDFS, Hive, Spark) to Snowflake. Phase 1 (this folder today) teaches components and naming conventions in three days. Phase 2 builds a working team warehouse. Phase 3 prepares for SnowPro Core.

## Folder map

```
vault/        open this folder in Obsidian; concepts, syllabus, flashcards, memory notes
quiz/         interactive quiz runner (python3 quiz/quiz.py ...) and its question bank
tools/        check_links.py keeps the vault graph free of dangling links and orphans
project/      the team warehouse project (phase 2), day-3 setup SQL lives here
docs/         design specs and implementation plans
```

## Start here

1. Open `vault/` as a vault in Obsidian.
2. Follow `vault/Setup/Obsidian Setup.md`, then `vault/Setup/Snowflake Account.md`.
3. Install the quiz runner: `pip install -r quiz/requirements.txt`
4. Start Day 1: open `vault/Syllabus/Day 1.md`, and when told, run `python3 quiz/quiz.py day1`.

## Run the quiz in Docker

No local Python needed. From the repo root:

```
docker compose run --rm quiz day1      # also: review | stats
```

The first run builds the image. Scores persist in `quiz/results/` on the host; the question bank is mounted read-only, so question edits apply without a rebuild. The image holds only the quiz code and the bank.

## Checks (for whoever edits content or code)

One script is the whole gate, locally and in CI:

```
checks/run.sh                       # tests, vault link checker, question bank lint
docker compose run --rm checks      # the same, in a container
```

The GitHub Actions workflow in `.github/workflows/checks.yml` runs the same script on every push once the repo has a remote. The individual checks, if you want one at a time:

```
python3 -m pytest quiz/tests tools/tests -q
python3 tools/check_links.py        # no dangling links, no orphan concept notes
python3 quiz/quiz.py lint           # bank ids, types, answers, concepts, coverage
```
