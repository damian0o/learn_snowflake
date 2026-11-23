# Learn Snowflake

A self-paced Snowflake learning environment for a data engineer moving a team from Cloudera (Hadoop, HDFS, Hive, Spark) to Snowflake. Phase 1 (this folder today) teaches components and naming conventions in three days. Phase 2 builds a working team warehouse. Phase 3 prepares for SnowPro Core.

## Folder map

```
vault/        open this folder in Obsidian; concepts, syllabus, flashcards, memory notes
quiz/         interactive quiz runner (python3 quiz/quiz.py ...) and its question bank
tools/        check_links.py (graph integrity), check_pitch.py (style contract), stage_site.py (website)
project/      the team warehouse project (phase 2), day-3 setup SQL lives here
checks/       the quality gate (run.sh) and its Docker image
site/         Quartz config overlay for the GitHub Pages website
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

## Website (GitHub Pages)

The vault is published as a static site with [Quartz](https://quartz.jzhao.xyz/): wikilinks, backlinks, search and the graph view, read-only. `.github/workflows/pages.yml` runs on every push to `main`: it clones Quartz at a pinned tag, overlays `site/quartz.config.ts` and `site/quartz.layout.ts`, stages the vault with `tools/stage_site.py` (drops `Templates/` and `.obsidian/`, turns the Home note into the site root) and deploys to Pages.

One-time setup after the first push: repository **Settings → Pages → Build and deployment → Source: GitHub Actions**. The site then lives at `https://damian0o.github.io/learn_snowflake/`.

Preview locally (needs Node 22+):

```bash
git clone --depth 1 --branch v4.5.2 https://github.com/jackyzha0/quartz.git /tmp/quartz
cp site/quartz.config.ts site/quartz.layout.ts /tmp/quartz/
python3 tools/stage_site.py vault /tmp/quartz/content
(cd /tmp/quartz && npm ci && npx quartz build --serve)   # http://localhost:8080
```

## Licence

Code (quiz runner, tools, workflows) is under the MIT licence, see `LICENSE`. The notes in `vault/` are under [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/): reuse them with attribution.

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
python3 tools/check_pitch.py        # prose budget, required headings, banned phrases per note
python3 quiz/quiz.py lint           # bank ids, types, answers, concepts, coverage
```
