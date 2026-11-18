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

## Checks

```
python3 tools/check_links.py        # vault graph integrity
python3 quiz/quiz.py lint           # question bank integrity
python3 -m pytest quiz/tests tools/tests -q
```
