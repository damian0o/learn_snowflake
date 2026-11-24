# Day 1 Senior Rewrite Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Rewrite the 22 Day 1 concept notes and the Day 1 syllabus note at senior-engineer pitch (diagram first, 300-word prose cap, Numbers / Probe / Cost sections), and add a gate that enforces that pitch.

**Architecture:** Content lives in `vault/`; a new `tools/check_pitch.py` (pure functions + CLI, same shape as `tools/check_links.py`) enforces the style contract and joins `checks/run.sh`. Notes keep their titles, folders and tags so `check_links`, the quiz bank and the flashcards stay valid. Mermaid is used for diagrams (rendered by Obsidian natively and by Quartz's ObsidianFlavoredMarkdown).

**Tech Stack:** Markdown + Mermaid, Python 3.9 (stdlib only for tools), pytest.

**Spec:** `docs/superpowers/specs/2026-11-23-day1-senior-rewrite-design.md` (amends `docs/superpowers/specs/2026-11-18-snowflake-learning-environment-design.md`).

## Global Constraints

- Python 3.9 compatible; tools use the standard library only.
- Note titles, folder placement and `tags:` are unchanged. The quiz bank's `concept:` values and all existing wikilinks must still resolve (`python3 tools/check_links.py` → `OK`).
- Prose budget: 300 words for `Concepts/` and `Conventions/`, 900 for `Syllabus/`. Prose = words outside fenced blocks, table lines, heading lines, frontmatter and the "Explain it to a teammate" section. List items and callouts count.
- Required headings in `Concepts/`: `## Numbers`, `## How it works`, `## Probe`, `## Cost`, `## Traps`, `## Related`. In `Conventions/`: `**Rule:**` line plus `## Examples`, `## Why`, `## Probe`, `## Related`.
- Banned phrases (case-insensitive) in `Concepts/`, `Conventions/`, `Syllabus/`: `seamless`, `effortless`, `elastic`, `in one sentence`, `why it matters`, `coming from hadoop`, `the brain`, `the muscles`.
- Every number in a note comes from the `docs:` page or an inline-linked doc page; where this plan says *verify*, the executor opens the page before writing the number and ledgers any deviation.
- Each note ends with `## Related` with ≥ 3 wikilinks (the `vs Cloudera` line was dropped on 2026-11-24 at the learner's request), and the unchanged `## Explain it to a teammate (fill in yourself)` block with an empty `>` line.
- Commits end with the attribution lines in force for this session.

## Review Focus

1. A note whose Mermaid block contains `|` characters at line start (edge labels) must not be miscounted as a table by `check_pitch` → test with a fenced block containing `|--`-style lines inside the fence (Task 1).
2. A note with `~~~` fences instead of backticks → fenced text must still be excluded (Task 1).
3. Frontmatter with `tags:` on multiple lines (YAML list form) → `--day 1` scoping must still find the note (Task 1).
4. A learner on the team account without `ACCOUNTADMIN` → every Probe that needs a privilege names it, and the Day 1 lab still completes with `SYSADMIN` except step 8 (Task 8 acceptance wording).
5. Quartz must render every Mermaid block; a syntax error leaves raw text on the public site → Task 10 greps `public/` for `language-mermaid` leftovers after a local build.

---

### Task 1: `tools/check_pitch.py`

**Files:**
- Create: `tools/check_pitch.py`
- Test: `tools/tests/test_check_pitch.py`

**Interfaces:**
- Produces:
  - `strip_frontmatter(text: str) -> Tuple[List[str], str]` → (tags, body)
  - `prose_words(body: str) -> int`
  - `missing_headings(body: str, required: Sequence[str]) -> List[str]`
  - `banned_hits(body: str, phrases: Sequence[str] = BANNED) -> List[str]`
  - `check_note(path: Path, vault_dir: Path, budgets: Dict[str, int] = BUDGETS) -> List[str]` (issue strings without the path prefix)
  - `main(argv: Optional[Sequence[str]] = None) -> int`; CLI `check_pitch.py [--vault vault] [--day N] [note ...]`; prints `PITCH <rel path>: <issue>` per issue or `OK: N notes checked`; exit 1 on any issue.
  - Constants: `BUDGETS = {"Concepts": 300, "Conventions": 300, "Syllabus": 900}`, `REQUIRED = {"Concepts": [...6 headings...], "Conventions": ["## Examples", "## Why", "## Probe", "## Related"]}`, `BANNED` (the eight phrases), `EXPLAIN_HEADING = "## Explain it to a teammate"`.
  - Folders scanned: `Concepts`, `Conventions`, `Syllabus` only.

- [ ] **Step 1: Write the failing tests**

```python
# tools/tests/test_check_pitch.py
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import check_pitch  # noqa: E402

FM = "---\ntags: [concept, day1, compute]\ndocs: https://x\n---\n"

def note(body, fm=FM):
    return fm + body

def test_strip_frontmatter_returns_tags_and_body_for_inline_and_block_lists():
    tags, body = check_pitch.strip_frontmatter(FM + "# T\n\nx")
    assert tags == ["concept", "day1", "compute"] and body == "# T\n\nx"
    tags2, _ = check_pitch.strip_frontmatter("---\ntags:\n  - concept\n  - day2\n---\nbody")
    assert tags2 == ["concept", "day2"]

def test_prose_words_excludes_fences_tables_headings_and_explain_section():
    body = ("# Title\n\none two three\n\n```mermaid\nA --> B\n|--x\n```\n\n"
            "| a | b |\n|---|---|\n| c | d |\n\n~~~\nfour five\n~~~\n\n- six seven\n\n"
            "## Explain it to a teammate (fill in yourself)\n\n> eight nine ten\n")
    assert check_pitch.prose_words(body) == 5   # one two three six seven

def test_prose_words_counts_wikilink_words_and_callouts():
    assert check_pitch.prose_words("> [!warning] Not yet\n> alpha [[Query Pruning]]\n") == 7

def test_missing_headings_reports_only_absent_ones():
    body = "## Numbers\n## How it works\n## Probe\n## Related\n"
    assert check_pitch.missing_headings(body, check_pitch.REQUIRED["Concepts"]) == ["## Cost", "## Traps"]

def test_banned_hits_is_case_insensitive_and_reports_phrase():
    assert check_pitch.banned_hits("Our Elastic compute is Seamless.") == ["elastic", "seamless"]
    assert check_pitch.banned_hits("nothing here") == []

def test_check_note_flags_budget_headings_and_banned(tmp_path):
    v = tmp_path / "vault"; (v / "Concepts").mkdir(parents=True)
    p = v / "Concepts" / "X.md"
    p.write_text(note("# X\n\n" + ("word " * 301) + "\n\nseamless\n\n## Related\n"))
    issues = check_pitch.check_note(p, v)
    assert any(i.startswith("prose 3") and "> 300" in i for i in issues)
    assert "missing heading ## Numbers" in issues
    assert "banned phrase 'seamless'" in issues

def test_check_note_uses_syllabus_budget_and_no_heading_rule(tmp_path):
    v = tmp_path / "vault"; (v / "Syllabus").mkdir(parents=True)
    p = v / "Syllabus" / "Day 9.md"
    p.write_text("---\ntags: [syllabus, day9]\n---\n# D\n\n" + ("w " * 850))
    assert check_pitch.check_note(p, v) == []

def test_main_scopes_by_day_and_accepts_explicit_paths(tmp_path, capsys):
    v = tmp_path / "vault"; (v / "Concepts").mkdir(parents=True)
    good = v / "Concepts" / "Good.md"
    good.write_text(note("# G\n\nfine\n\n## Numbers\n## How it works\n## Probe\n## Cost\n## Traps\n## Related\n"))
    bad = v / "Concepts" / "Bad.md"
    bad.write_text(note("# B\n\nelastic\n", fm="---\ntags: [concept, day2]\n---\n"))
    assert check_pitch.main(["--vault", str(v), "--day", "1"]) == 0
    assert "OK: 1 notes checked" in capsys.readouterr().out
    assert check_pitch.main(["--vault", str(v)]) == 1
    assert "PITCH Concepts/Bad.md: banned phrase 'elastic'" in capsys.readouterr().out
    assert check_pitch.main(["--vault", str(v), str(good)]) == 0
```

- [ ] **Step 2: Run tests to verify they fail**

Run: `python3 -m pytest tools/tests/test_check_pitch.py -q`
Expected: FAIL at import (`ModuleNotFoundError: check_pitch`)

- [ ] **Step 3: Implement `tools/check_pitch.py`**

Prose counting: cut the body at `EXPLAIN_HEADING`; remove fenced blocks with a regex that matches both ```` ``` ```` and `~~~` fences (`re.sub(r"^(```|~~~).*?^\1\s*$", "", body, flags=re.S | re.M)`); drop lines whose stripped form starts with `|` or `#`; count `re.findall(r"[A-Za-z0-9_']+", rest)`. Tags: parse `tags:` inline `[a, b]` or following `- ` lines inside the frontmatter. Folder = first path part relative to vault; skip files in other folders. Issue strings: `prose N > B`, `missing heading H`, `banned phrase 'p'`, `missing **Rule:** line` (Conventions only).

- [ ] **Step 4: Run tests to verify they pass**

Run: `python3 -m pytest tools/tests -q`
Expected: all pass (existing 10 tool tests + 8 new)

- [ ] **Step 5: Run the check on the current vault to see the baseline**

Run: `python3 tools/check_pitch.py --day 1; echo "exit $?"`
Expected: exit 1, `PITCH` lines for every Day 1 concept note (missing headings, banned phrases). This is the backlog Tasks 3–8 clear.

- [ ] **Step 6: Commit**

```bash
git add tools/check_pitch.py tools/tests/test_check_pitch.py
git commit -m "feat(tools): check_pitch enforces prose budget, required headings and banned phrases"
```

---

### Task 2: Templates

**Files:**
- Modify: `vault/Templates/Concept.md`, `vault/Templates/Convention.md`

- [ ] **Step 1: Replace `Concept.md`** with the anatomy from the spec ("Concept note anatomy"), `{{title}}` as the H1, placeholders in angle brackets, an empty Mermaid fence, the Numbers table header `| Thing | Value | Source |`, and the closing `**vs Cloudera:**`, `## Related`, Explain block.

- [ ] **Step 2: Replace `Convention.md`** with: frontmatter `tags: [convention, day3, naming]`, `# Naming - {{title}}`, `**Rule:**`, `**Pattern:**`, `## Examples` (Good/Bad/Why table), `## Why` (≤ 3 bullets), `## Probe` (SQL fence: a `SHOW` or `INFORMATION_SCHEMA` query proving the rule), `## Cost` (optional, "No direct cost." default), `**vs Hive:**` one line, `## Related`, Explain block.

- [ ] **Step 3: Verify the link checker still skips Templates**

Run: `python3 tools/check_links.py`
Expected: `OK: 40 notes, 297 links`

- [ ] **Step 4: Commit**

```bash
git add vault/Templates
git commit -m "docs(vault): templates for the senior-pitch note anatomy"
```

---

### Task 3: Checkpoint notes — Virtual Warehouse, Micro-partitions

**Files:**
- Modify: `vault/Concepts/Virtual Warehouse.md`, `vault/Concepts/Micro-partitions.md`

**Interfaces:**
- Consumes: `check_pitch.py <note>` (Task 1), templates (Task 2).

Each rewritten note follows the template exactly. Briefs:

**Virtual Warehouse** (`docs:` warehouses-overview)
- Diagram: `flowchart LR` Session `--USE WAREHOUSE-->` WH[`WH_<TEAM>_<PURPOSE>_<SIZE>`] with sub-nodes `n nodes (size)`, `SSD cache`; WH `--reads-->` Storage; `Cloud Services --plan--> WH`; states `suspended → resuming → running → suspending` as a second small `stateDiagram-v2`.
- Numbers: size default via SQL `XSMALL`, via Snowsight `XLARGE`; `AUTO_SUSPEND` default 600 s; `AUTO_RESUME` default TRUE; billing minimum 60 s per resume; resize live, running queries unaffected; `INITIALLY_SUSPENDED` default FALSE; one current warehouse per session; Gen2 standard warehouses exist (`GENERATION` column of `SHOW WAREHOUSES`) *verify*.
- How it works: ≤ 8 arrows: create → (suspended|running) → statement arrives → auto-resume → nodes provisioned → executes plan from Cloud Services → cache fills → idle timer → suspend → cache dropped.
- Probe: `SHOW WAREHOUSES;` (columns `state`, `size`, `auto_suspend`, `running`, `queued`), then `ALTER WAREHOUSE WH_LEARN_XS SUSPEND; SHOW WAREHOUSES LIKE 'WH_LEARN_XS';` → `state = SUSPENDED`.
- Cost: credits/second by size while `state = STARTED` → `ACCOUNT_USAGE.WAREHOUSE_METERING_HISTORY.CREDITS_USED_COMPUTE`.
- Traps: Snowsight default XL; `SHOW`/`DESCRIBE`/result-reuse/metadata-only statements need no warehouse; dropping a warehouse loses nothing.
- vs Cloudera: YARN queue with fixed executors → created, resized and suspended in seconds; holds no data so nothing rebalances.

**Micro-partitions** (`docs:` tables-clustering-micropartitions)
- Diagram: `flowchart TB` Table → MP1[MP: 50–500 MB uncompressed, columnar] + MP2 + MPn; each MP → `metadata: min/max per column, distinct, nulls, row count` stored in Cloud Services; DML → new MPs, old MPs retained (Time Travel) → purged.
- Numbers: 50–500 MB uncompressed; immutable; created in load order; metadata per column: min, max, number of distinct values, null count (docs wording); `SYSTEM$CLUSTERING_INFORMATION` / `SYSTEM$CLUSTERING_DEPTH` output fields `total_partition_count`, `average_overlaps`, `average_depth` *verify names*.
- How it works: load → split by arrival order → columnar encode + compress → write to object storage → register metadata; query → prune by metadata → read only needed columns of surviving MPs; UPDATE/DELETE/MERGE → rewrite affected MPs.
- Probe: `SELECT SYSTEM$CLUSTERING_INFORMATION('SNOWFLAKE_SAMPLE_DATA.TPCH_SF1.LINEITEM','(L_SHIPDATE)');` → JSON with `total_partition_count` and `average_depth`; then Query Profile of a date-filtered query → `Partitions scanned` ≪ `Partitions total`.
- Cost: storage = compressed bytes incl. retained MPs → `ACCOUNT_USAGE.TABLE_STORAGE_METRICS` (`ACTIVE_BYTES`, `TIME_TRAVEL_BYTES`, `FAILSAFE_BYTES`) *verify column names*.
- Traps: size quoted uncompressed; no `PARTITION BY` for standard tables; row rewrites keep old MPs for a while (storage).
- vs Cloudera: Hive partition directories you named → automatic, invisible, per-column stats; no `MSCK REPAIR`.

- [ ] **Step 1: Rewrite the two notes** per the briefs.
- [ ] **Step 2: Verify**

Run: `python3 tools/check_pitch.py "vault/Concepts/Virtual Warehouse.md" "vault/Concepts/Micro-partitions.md" && python3 tools/check_links.py && python3 quiz/quiz.py lint`
Expected: `OK: 2 notes checked`, `OK: 40 notes, …`, lint OK.

- [ ] **Step 3: Commit, then stop for the learner checkpoint**

```bash
git add vault/Concepts
git commit -m "docs(vault): rewrite Virtual Warehouse and Micro-partitions at senior pitch"
```

Report to the learner with both notes and wait for their verdict before Task 4. This stop is required by the spec ("first two notes are the checkpoint"); it overrides continuous execution.

---

### Task 4: Architecture notes (5)

**Files:** `What Snowflake Is`, `Three-Layer Architecture`, `Cloud Services Layer`, `Compute Layer`, `Database Storage Layer` under `vault/Concepts/`.

**What Snowflake Is** — diagram: `flowchart LR` Client(SQL, drivers, Snowsight) → Account[(one cloud, one region, one edition)] → three layer boxes; Numbers: 3 clouds; delivery = SaaS, no on-prem; serverless features list (Snowpipe, Automatic Clustering, serverless tasks, search optimization, MV maintenance); Probe: `SELECT CURRENT_REGION(), CURRENT_ACCOUNT(), CURRENT_VERSION();`; Cost: none directly, points to [[Credits and Billing]]; Traps: not built on Hadoop/Spark; "serverless" = Snowflake-managed compute billed in credits; no local edition; vs Cloudera: whole platform → one account; nothing to run.

**Three-Layer Architecture** — diagram: `flowchart TB` Cloud Services (auth, metadata, optimizer, access control, transactions, result cache) → Compute (WH boxes, isolated) → Storage (micro-partitions in object storage); label "hybrid: shared-disk storage, shared-nothing execution". Numbers: layers you provision = 1 (compute); Cloud Services billed above 10 % of daily warehouse credits. Probe: Query Profile of any query → `Partitions scanned/total` (Cloud Services pruning) and `bytes scanned from cache` (compute). Cost: per layer → warehouse credits, storage TB-month, cloud services excess. Traps: "Query Processing" = Compute; only compute is sized by you; hybrid means both. vs Cloudera: HDFS+YARN+Metastore in one cluster → three independently scaled layers.

**Cloud Services Layer** — diagram: `sequenceDiagram` Client→CS: authenticate; CS→CS: parse, optimise, prune (metadata); alt result reuse → return; else CS→WH: plan; WH→Storage: read; WH→CS: result; CS→Client. Numbers: 10 % rule (daily, UTC, excess only, serverless excluded); `CREDITS_USED_CLOUD_SERVICES` latency ≤ 6 h in `WAREHOUSE_METERING_HISTORY`. Probe: `SHOW TABLES IN SNOWFLAKE_SAMPLE_DATA.TPCH_SF1;` with warehouse suspended → runs; `SELECT COUNT(*) FROM …LINEITEM;` → runs, warehouse stays suspended. Cost: `METERING_DAILY_HISTORY.CREDITS_ADJUSTMENT_CLOUD_SERVICES`, `CREDITS_BILLED`. Traps: not free above 10 %; optimizer here not in WH; not configurable. vs Cloudera: Metastore + Ranger + ResourceManager + compiler, plus per-MP stats and result cache.

**Compute Layer** — diagram: `flowchart LR` plan → WH[n nodes, MPP] → each node: share of MPs → exchange → result; several WHs side by side reading one Storage. Numbers: nodes double per size; per-second billing, 60 s minimum; isolation = no shared compute between WHs; local SSD cache per node. Probe: Query Profile → operator tree, `bytes spilled to local/remote storage` *verify labels*. Cost: `CREDITS_USED_COMPUTE`. Traps: "Query Processing layer" synonym; WH stores no tables; two WHs never share compute. vs Cloudera: executors inside one YARN cluster → one cluster per workload, no contention.

**Database Storage Layer** — diagram: `flowchart LR` Load → Snowflake format (columnar, compressed, encrypted) → micro-partitions → S3 / Blob / GCS (account region); readers = all WHs; retained versions → Time Travel → Fail-safe → purge. Numbers: MP 50–500 MB; Time Travel default 1 day, Standard max 1, Enterprise+ max 90; Fail-safe 7 days; storage billed on average daily compressed bytes. Probe: `SELECT * FROM SNOWFLAKE.ACCOUNT_USAGE.TABLE_STORAGE_METRICS WHERE TABLE_NAME='…' ` *verify* or `SHOW TABLES` `bytes` column. Cost: `ACCOUNT_USAGE.STORAGE_USAGE` (`STORAGE_BYTES`, `STAGE_BYTES`, `FAILSAFE_BYTES`) *verify*. Traps: no file access to the bucket; compressed bytes billed; history counts. vs Cloudera: HDFS files you laid out → format and layout owned by Snowflake; exit via SQL/COPY/share only.

- [ ] **Step 1: Rewrite the five notes.**
- [ ] **Step 2: Verify** — Run: `python3 tools/check_pitch.py vault/Concepts/"What Snowflake Is.md" vault/Concepts/"Three-Layer Architecture.md" vault/Concepts/"Cloud Services Layer.md" vault/Concepts/"Compute Layer.md" vault/Concepts/"Database Storage Layer.md" && python3 tools/check_links.py` — Expected: `OK: 5 notes checked`, links OK.
- [ ] **Step 3: Commit** — `git commit -am "docs(vault): architecture notes at senior pitch"`

---

### Task 5: Storage and caching notes (6)

**Files:** `Query Pruning`, `Clustering Keys`, `Caching`, `Result Cache`, `Warehouse Cache`, `Metadata Cache`.

**Query Pruning** — diagram: `flowchart LR` predicate → compare with per-MP min/max (Cloud Services, compile time) → surviving MPs → columnar read of referenced columns only (WH) → runtime join-filter pruning. Numbers: pruning operators that work (`=`, `<`, `>`, `BETWEEN`, `IN`); what defeats it (function on column, `LIKE '%x'`, type mismatch). Probe: run the Day 1 lab query, Query Profile TableScan → `Partitions scanned` vs `Partitions total`; rerun with `TO_CHAR(L_SHIPDATE,'YYYY-MM') = '1995-01'` → scanned ≈ total. Cost: fewer MPs → fewer seconds → `CREDITS_USED_COMPUTE`; `QUERY_HISTORY.PARTITIONS_SCANNED/PARTITIONS_TOTAL`. Traps: compile-time vs runtime pruning; functions kill it; evidence is the ratio. vs Cloudera: partition pruning only on `PARTITIONED BY` columns → every column, no DDL.

**Clustering Keys** — diagram: before/after MP ranges on the key (`flowchart` with two rows of MP boxes showing overlapping vs disjoint ranges); Automatic Clustering (serverless) loop. Numbers: multi-TB tables only; ≤ 3–4 columns, low→high cardinality; `SYSTEM$CLUSTERING_DEPTH` lower is better; serverless credits service type `AUTO_CLUSTERING`; clones have Automatic Clustering suspended; not on hybrid tables. Probe: `SELECT SYSTEM$CLUSTERING_DEPTH('…LINEITEM','(L_SHIPDATE)');` and `ALTER TABLE … CLUSTER BY (…)` syntax. Cost: `METERING_DAILY_HISTORY WHERE SERVICE_TYPE='AUTO_CLUSTERING'`, `AUTOMATIC_CLUSTERING_HISTORY` *verify view name*. Traps: small tables burn credits; serverless; resume after clone. vs Cloudera: bucketing/sort at write time you maintained → background reclustering, pay per credit.

**Caching** — diagram: `flowchart TB` query → result cache? → metadata-only? → warehouse → SSD cache? → remote storage; each cache box labelled with layer and lifetime. Numbers: table of three caches (lives in, holds, lifetime, dropped by). Probe: `ALTER SESSION SET USE_CACHED_RESULT = FALSE;` then run twice → second run `bytes scanned from cache` > 0 in Query Profile. Cost: result/metadata hits = 0 warehouse credits; SSD hits = fewer seconds. Traps: three places; only SSD cache dies on suspend; benchmarks lie twice. vs Cloudera: HDFS cache / Impala buffers → three distinct caches with distinct scopes.

**Result Cache** — diagram: `flowchart LR` conditions as a decision chain (identical text → data unchanged → privileges → deterministic → `USE_CACHED_RESULT`) → REUSE node `QUERY RESULT REUSE`; else execute. Numbers: 24 h after last use, reset on reuse, max 31 days; per account, not per user; hybrid tables excluded *verify*. Probe: run the lab query twice → `QUERY_HISTORY.EXECUTION_STATUS`… simpler: Query Profile node `QUERY RESULT REUSE`; `SELECT query_id, bytes_scanned FROM TABLE(INFORMATION_SCHEMA.QUERY_HISTORY()) ORDER BY start_time DESC LIMIT 2;` → second has `bytes_scanned = 0`. Cost: 0 warehouse credits; cloud services only. Traps: byte-identical text; reclustering counts as change; different user same role reuses. vs Cloudera: no equivalent except app-side caching.

**Warehouse Cache** — diagram: `flowchart LR` WH nodes with SSD boxes ← remote storage; events: suspend → drop all; downsize → drop removed nodes' share; upsize → keep + empty nodes. Numbers: lifetime = while running; bounded by node SSD; shared within WH, private to WH. Probe: with `USE_CACHED_RESULT = FALSE`, run twice → Query Profile `Percentage scanned from cache` *verify label*; `QUERY_HISTORY.PERCENTAGE_SCANNED_FROM_CACHE`. Cost: faster scans → fewer credits; the trade against `AUTO_SUSPEND`. Traps: cold after resume; data not results; per warehouse. vs Cloudera: OS page cache on DataNodes → explicit per-warehouse SSD cache that suspend wipes.

**Metadata Cache** — diagram: `flowchart LR` every write → metadata store (row count, min/max, NDV, nulls per column per MP) → serves `COUNT(*)`, `MIN`, `MAX` whole-table; `SHOW`, `DESCRIBE`; pruning. Numbers: always current; no `ANALYZE`; whole-table only (filters/`GROUP BY` → warehouse); "for most data types". Probe: suspend WH; `SELECT COUNT(*), MIN(L_SHIPDATE), MAX(L_SHIPDATE) FROM …LINEITEM;` → returns, `SHOW WAREHOUSES` still `SUSPENDED`; add `WHERE L_QUANTITY > 10` → resumes. Cost: 0 warehouse credits for metadata answers. Traps: filter breaks it; never stale; lives in Cloud Services. vs Cloudera: Hive stats via `ANALYZE TABLE`, often stale → maintained on every write.

- [ ] **Step 1: Rewrite the six notes.**
- [ ] **Step 2: Verify** — `python3 tools/check_pitch.py` on the six paths and `python3 tools/check_links.py` — Expected: `OK: 6 notes checked`, links OK.
- [ ] **Step 3: Commit** — `git commit -am "docs(vault): storage and caching notes at senior pitch"`

---

### Task 6: Compute notes (4)

**Files:** `Warehouse Sizes and Credits`, `Auto-suspend and Auto-resume`, `Scaling Up vs Scaling Out`, `Multi-cluster Warehouse`.

**Warehouse Sizes and Credits** — Numbers table is the centre: size, credits/hour Gen1 (1…512), nodes (doubling), availability (5XL/6XL AWS and Azure only); Gen2 multiplier *verify on the warehouse credit page*; billing: per second, 60 s minimum per resume, resize bills new size from provisioning, multi-cluster = size × running clusters. Diagram: `flowchart LR` timeline example `61 s run → suspend → 30 s run = 60 + 1 + 60 = 121 s`. Probe: `SELECT start_time, warehouse_name, credits_used_compute FROM TABLE(INFORMATION_SCHEMA.WAREHOUSE_METERING_HISTORY(DATEADD('day',-1,CURRENT_DATE()))) ORDER BY 1 DESC;`. Cost: this *is* the meter; `WAREHOUSE_METERING_HISTORY`. Traps: doubling; minimum per resume; credit price by edition/cloud/region. vs Cloudera: node-hours of a fixed cluster → seconds × size.

**Auto-suspend and Auto-resume** — diagram: `stateDiagram-v2` running → (idle ≥ AUTO_SUSPEND) suspending → suspended → (statement, AUTO_RESUME) resuming → running; annotate "cache dropped" on suspend, "60 s minimum" on resume. Numbers: default 600 s; `0`/`NULL` disables; check interval ~30 s *verify wording*; `AUTO_RESUME` default TRUE, FALSE → statements fail; multi-cluster semantics; suggested timeouts table (ELT 60–300 s, ad-hoc ~300 s, BI ≥ 600 s). Probe: `ALTER WAREHOUSE WH_LEARN_XS SET AUTO_SUSPEND = 60;` wait, `SHOW WAREHOUSES LIKE 'WH_LEARN_XS'` → `SUSPENDED`; then a query → `STARTED`. Cost: idle seconds = `CREDITS_USED_COMPUTE − CREDITS_ATTRIBUTED_COMPUTE_QUERIES`. Traps: 0 disables; suspend kills cache; resume latency. vs Cloudera: always-on cluster → per-warehouse idle timer you set.

**Scaling Up vs Scaling Out** — diagram: two `flowchart` columns: UP (S → L, same query, more nodes) vs OUT (M, M, M; same size, more clusters, queue drains). Numbers: resize immediate for new/queued, running finish on old nodes; downsize drops cache share; out needs Enterprise+. Probe: `SELECT total_elapsed_time, execution_time, queued_overload_time, bytes_spilled_to_local_storage, bytes_spilled_to_remote_storage FROM TABLE(INFORMATION_SCHEMA.QUERY_HISTORY()) ORDER BY start_time DESC LIMIT 10;` → long `execution_time`/spills ⇒ up; long `queued_overload_time` ⇒ out *verify column names*. Cost: up multiplies credits/second; out multiplies by running clusters. Traps: symptom → direction; resize does not interrupt; edition. vs Cloudera: bigger executors vs more executors on one shared queue → two independent knobs, no contention.

**Multi-cluster Warehouse** — diagram: `flowchart LR` queue → cluster 1 … cluster MAX; policy box Standard vs Economy with start/stop rules; modes Maximized (MIN = MAX) vs Auto-scale (MIN < MAX). Numbers: Enterprise+; Snowsight max 10 clusters; SQL limits by size *verify table*; Standard: start on first queued query, stop after 2–3 consecutive checks at 1-minute intervals; Economy: start only if ≥ 6 min of work, stop after 5–6 checks *verify*; cost = size × running clusters. Probe: `SHOW WAREHOUSES` columns `min_cluster_count`, `max_cluster_count`, `scaling_policy`, `started_clusters`; `ALTER WAREHOUSE … SET MAX_CLUSTER_COUNT = 2` on Enterprise. Cost: `WAREHOUSE_METERING_HISTORY` sums across clusters; `WAREHOUSE_LOAD_HISTORY` for queueing *verify*. Traps: Standard edition max 1; min=max means maximized; policies named Standard/Economy. vs Cloudera: queue capacity scheduler → identical clusters added per queue depth.

- [ ] **Step 1: Rewrite the four notes.**
- [ ] **Step 2: Verify** — `check_pitch` on the four paths, `check_links` — Expected: `OK: 4 notes checked`, links OK.
- [ ] **Step 3: Commit** — `git commit -am "docs(vault): compute notes at senior pitch"`

---

### Task 7: Platform notes (5)

**Files:** `Snowflake Editions`, `Cloud Providers and Regions`, `Organizations and Accounts`, `Snowsight`, `Credits and Billing`.

**Snowflake Editions** — Numbers table is the note (Standard / Enterprise / Business Critical / VPS × features: Time Travel max 1 vs 90 days, multi-cluster, MVs, search optimization, masking & row access, periodic rekeying, query acceleration, Tri-Secret Secure, private connectivity, failover/failback, isolated environment). Diagram: `flowchart LR` Standard → Enterprise → Business Critical → VPS as a superset chain. Probe: `SHOW PARAMETERS LIKE 'DATA_RETENTION_TIME_IN_DAYS' IN ACCOUNT;` and `SELECT SYSTEM$…`? Use Snowsight Admin » Accounts → edition, or `SELECT CURRENT_ACCOUNT_NAME()` plus the org view `ORGANIZATION_USAGE.ACCOUNTS` *verify a SQL way to read edition; else state Snowsight path*. Cost: price per credit rises with edition, consumption does not; `RATE_SHEET_DAILY` *verify* (capstone). Traps: Fail-safe 7 days everywhere; BC = ESD historically; features start at the named edition. vs Cloudera: licence tiers per node → per-account edition, switchable.

**Cloud Providers and Regions** — diagram: `flowchart TB` Org → Account(cloud, region) → Storage+Compute in region; cross-region replication/share arrows labelled "egress". Numbers: 3 providers; 5XL/6XL AWS+Azure only; identifier `<orgname>-<account_name>`; locator legacy; ingress free, egress charged. Probe: `SELECT CURRENT_REGION(), CURRENT_ORGANIZATION_NAME(), CURRENT_ACCOUNT_NAME();` *verify function names*; `SHOW REGIONS;`. Cost: `ACCOUNT_USAGE.DATA_TRANSFER_HISTORY` (`BYTES_TRANSFERRED`, `TARGET_CLOUD`, `TARGET_REGION`) *verify*. Traps: one account = one cloud + region; egress; identifier form. vs Cloudera: one datacenter → region choice drives egress for AEP/Pega feeds.

**Organizations and Accounts** — diagram: `flowchart TB` Organization → Accounts → account-level objects (users, roles, warehouses, resource monitors, integrations) and Database → Schema → objects. Numbers: `ORGADMIN` creates/lists accounts; organization account + `GLOBALORGADMIN`; account names unique within org, no hyphens; nothing crosses accounts without share/replication. Probe: `SHOW ORGANIZATION ACCOUNTS;` (ORGADMIN) or `SELECT CURRENT_ORGANIZATION_NAME(), CURRENT_ACCOUNT_NAME();`. Cost: billing rolls up to the organization → `ORGANIZATION_USAGE` (capstone). Traps: ORGADMIN ≠ ACCOUNTADMIN; object ownership levels; env-per-database is the Day 3 route. vs Cloudera: one cluster, env by HDFS path → account or database per environment.

**Snowsight** — Numbers table = menu map (Projects » Worksheets; Monitoring » Query History; Query Profile fields; Admin » Warehouses; Admin » Cost management; Admin » Accounts; Data » Databases). Diagram: `flowchart LR` Worksheet → Query History → Query Profile with the four fields to read. Probe: open the lab query's profile → name `Partitions scanned`, `Bytes scanned from cache`, `Bytes spilled`, `QUERY RESULT REUSE`. Cost: Snowsight itself is free; its queries use the worksheet's warehouse. Traps: XL default; profile is the evidence; classic console gone. vs Cloudera: Hue/CM → one UI, same SQL as drivers.

**Credits and Billing** — diagram: `flowchart LR` meters (warehouse compute, serverless, cloud services excess; storage; transfer) → credits / TB-month / bytes → invoice; 10 % rule on the cloud-services arrow. Numbers: three meters; warehouse per-second + 60 s; serverless list; 10 % daily UTC excess, serverless excluded; storage average daily compressed bytes incl. TT/Fail-safe/stages; ingress free. Probe: Snowsight Admin » Cost management » Consumption, and `SELECT usage_date, service_type, credits_billed FROM SNOWFLAKE.ACCOUNT_USAGE.METERING_DAILY_HISTORY WHERE usage_date >= DATEADD('day',-7,CURRENT_DATE()) ORDER BY 1 DESC;`. Cost: this note *is* the map; forward link to the phase 1 capstone (`[[Day 3]]`). Traps: three meters; excess only; compressed + history. vs Cloudera: capex + node-hours → three metered lines.

- [ ] **Step 1: Rewrite the five notes.**
- [ ] **Step 2: Verify** — `check_pitch` on the five paths, `check_links` — Expected: `OK: 5 notes checked`, links OK.
- [ ] **Step 3: Full Day 1 pitch check** — Run: `python3 tools/check_pitch.py --day 1` — Expected: `OK: 23 notes checked` (22 concepts + Day 1 note still at old text may fail on budget/banned → if so, expected failure is only `Syllabus/Day 1.md`; Task 8 clears it).
- [ ] **Step 4: Commit** — `git commit -am "docs(vault): platform notes at senior pitch"`

---

### Task 8: Day 1 note

**Files:** Modify `vault/Syllabus/Day 1.md`

- Opening: two lines (what you can do by the end), the Rhythm line, prerequisites line.
- Diagram: `flowchart LR` Client → CS[Cloud Services: auth → parse → optimise → prune → result reuse?] → WH[Warehouse: SSD cache → remote storage] → Result → CS result cache; annotations: `credits/second` on WH, `10 % rule` on CS, `micro-partitions` on storage.
- Sections, each 3–6 bullets with the wikilinks and one hard fact per bullet: Cloud Services; Storage; Compute; Caching; Platform; Cost (two bullets: the three meters, where Day 1's credits show up, forward pointer "full metrics and price evaluation at the end of Day 3").
- Hadoop bridge: 5-row table (Cloudera → Snowflake → what changes).
- Hands-on: steps 1–8 kept verbatim including the author's warning callout; step 8 ends with "the full read of metrics and price comes at the end of Day 3".
- Drill: keep; card count wording "about 65 cards" → the real count from `grep -c '::' vault/Flashcards/*.md` after Task 9 (do this step after Task 9 or update in Task 9).
- Acceptance: keep six items.
- Budget: ≤ 900 prose words; no banned phrases.

- [ ] **Step 1: Rewrite the note.**
- [ ] **Step 2: Verify** — Run: `python3 tools/check_pitch.py --day 1 && python3 tools/check_links.py` — Expected: `OK: 23 notes checked`, links OK.
- [ ] **Step 3: Commit** — `git commit -am "docs(vault): Day 1 as a per-layer article with the query-path diagram"`

---

### Task 9: Flashcards, quiz and Rosetta Stone reconciliation

**Files:** `vault/Flashcards/*.md`, `quiz/bank/day1.yaml`, `vault/Migration/Hadoop to Snowflake Rosetta Stone.md`, `vault/Syllabus/Day 1.md` (card count line)

- [ ] **Step 1: Rosetta Stone** — replace "elastic" in the `What Snowflake Is` row with a concrete difference (e.g. "per-second billed, per-workload warehouses"). The Migration folder is not pitch-checked, but the phrase is banned by the spec's anti-goals.
- [ ] **Step 2: Flashcards** — read each deck against the rewritten notes; reword any card whose answer quotes removed text; add cards for new facts introduced by the rewrite (candidates: Snowsight default XL vs SQL default XS; `CREDITS_USED_COMPUTE − CREDITS_ATTRIBUTED_COMPUTE_QUERIES = idle`; `AUTO_SUSPEND = 0` disables; multi-cluster SQL vs UI limits; `SYSTEM$CLUSTERING_DEPTH`; `PERCENTAGE_SCANNED_FROM_CACHE`). Keep every card's trailing `[[Concept]]` link.
- [ ] **Step 3: Quiz** — reword explanations that quote removed text; add ≥ 6 questions for added mechanisms with ids continuing the existing `d1-<area>-NNN` sequences; keep type mix rules (lint).
- [ ] **Step 4: Update the card count** in `Day 1.md` Drill and Acceptance from `grep -c '::' vault/Flashcards/Cards\ -\ *.md | awk -F: '{s+=$2} END {print s}'`.
- [ ] **Step 5: Verify** — Run: `python3 quiz/quiz.py lint && python3 tools/check_links.py && python3 tools/check_pitch.py --day 1 && python3 -m pytest quiz/tests tools/tests -q` — Expected: all OK/pass.
- [ ] **Step 6: Commit** — `git commit -am "docs: flashcards, quiz and Rosetta Stone reconciled with the senior-pitch notes"`

---

### Task 10: Gate, docs, site check

**Files:** `checks/run.sh`, `README.md`, `vault/Setup/Quiz Runner.md`, `checks/Dockerfile` (no change expected: `tools/` already copied)

- [ ] **Step 1: Add the pitch check to `checks/run.sh`** after the vault links step:

```bash
echo "== vault pitch (prose budget, headings, banned phrases)"
python3 tools/check_pitch.py
```

- [ ] **Step 2: Docs** — README "Checks" section: add `python3 tools/check_pitch.py` to the individual commands with one line on what it enforces; Quiz Runner note "Checks (author side)": same line.
- [ ] **Step 3: Run the whole gate** — Run: `checks/run.sh` — Expected: ends with `== all checks passed`.
- [ ] **Step 4: Local Quartz build renders Mermaid** — Run (Quartz clone from the earlier session at the scratchpad, or re-clone v4.5.2): apply overlay, `python3 tools/stage_site.py vault <quartz>/content`, `npx quartz build`, then `grep -rl 'language-mermaid' <quartz>/public | wc -l` and `grep -rl '<svg' <quartz>/public/Concepts | wc -l` — Expected: Mermaid blocks are emitted as `<pre class="mermaid">` or rendered; zero pages with a raw `language-mermaid` code block. Quartz renders Mermaid client-side, so the gate is: every `Concepts/*.html` contains `class="mermaid"` where the note has a diagram, and the build log has no errors.
- [ ] **Step 5: Docker checks image** — Run: `docker compose build checks && docker compose run --rm checks` — Expected: `== all checks passed`.
- [ ] **Step 6: Commit and push** — `git add -A && git commit -m "ci: pitch check joins the gate; docs"` then `git push` and watch `gh run list --limit 2` → both workflows `success`; open the site and confirm one concept page shows its diagram.

---

## Self-review notes

- Spec coverage: pitch contract → Task 1 + Global Constraints; anatomy and templates → Task 2; 22 notes → Tasks 3–7; Day 1 → Task 8; flashcards/quiz → Task 9; enforcement in gate → Task 10; capstone explicitly deferred to increment 3 (spec). Checkpoint stop → Task 3.
- Type consistency: `check_pitch` names used in Tasks 3–10 match Task 1's Interfaces.
- Review Focus items 1–3 are pinned by Task 1 tests; 4 by Task 8 wording; 5 by Task 10 step 4.
