# Snowflake Learning Environment, Increment 1: Skeleton + Day 1 — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Deliver the complete working skeleton (git repo, Obsidian vault config and templates, quiz runner with tests, link checker) plus every piece of Day 1 content, so Damianos can start studying while Days 2 and 3 are written.

**Architecture:** A markdown Obsidian vault under `vault/` where every concept is one note and every flashcard/quiz item links back to its concept. A pure-logic Python package `quiz/quizlib` (bank loading, answer matching, Leitner boxes, progress, stats) with a thin CLI in `quiz/quiz.py`. A standalone `tools/check_links.py` that enforces the graph rules (no dangling links, no orphan concepts, quiz concepts resolve). Increments 2 and 3 add only content to the same structure.

**Tech Stack:** Python 3.9 (pyenv), PyYAML 6, pytest 8, Obsidian with the community plugin "Spaced Repetition" (id `obsidian-spaced-repetition`), git.

**Spec:** `docs/superpowers/specs/2026-11-18-snowflake-learning-environment-design.md`

## Global Constraints

- Python code must run on Python 3.9.6: no `match`, no `X | Y` types, no `list[str]` at runtime (use `typing`), no `tomllib`.
- Only dependencies: `pyyaml`, `pytest`. Everything else stdlib.
- Note titles (file stems) never contain `:`, `/`, `\`, `|`, `#`, `^`, `[`, `]` (Obsidian forbids them). Convention notes are titled `Naming - <Thing>`, card notes `Cards - <Topic>`.
- Every concept note follows `vault/Templates/Concept.md` exactly: frontmatter with `tags` (`concept`, `dayN`, area) and `docs` URL; sections **In one sentence**, **Why it matters**, **Coming from Hadoop**, `## How it works`, `## Gotchas / exam traps`, `## Related` (≥3 wikilinks), `## Explain it to a teammate (fill in yourself)` left empty.
- Every "Coming from Hadoop" line names the Cloudera-world equivalent AND where the analogy breaks.
- Every concept note's `docs:` URL is opened (web-fetch agent) and the note's facts checked against it before the note's task is committed.
- Flashcards use Spaced Repetition syntax: `Question::Answer` single-line, multi-line with a `?` line between front and back, cloze with `==text==`. Cards are separated by a blank line. Each card note has frontmatter `tags: [flashcards/day1, ...]`. Answers contain a wikilink to the concept note.
- Quiz question ids match `^(d[1-3]|cum)-[a-z]+-\d{3}$`. Types are exactly `mcq`, `multi`, `tf`, `fill`. `concept` must equal a note stem in `vault/Concepts/` or `vault/Conventions/`.
- Day 1 content sizes: ~20 concept notes, 4 card notes with 35–45 cards total, 30 quiz questions of which 4–6 tagged `migration`, difficulty mix ≈ 15 recall / 10 understanding / 5 application.
- Snowsight hands-on steps and the account check are marked `> [!warning] Not yet executed by the author` in the note, because the builder has no Snowflake account.
- Commit after every task. Commit messages end with `Co-Authored-By: Claude Fable 5.1 <noreply@anthropic.com>`.

## Review Focus

Failure modes the spec implies but a straightforward implementation would miss. Each has a pinned test in the owning task.

1. **Invalid or empty keyboard input during a quiz** (a letter not among the options, an empty line, EOF). Expected: re-prompt on invalid, treat EOF as "quit and save progress", never a traceback. Test in Task 7 (`test_invalid_letter_reprompts`, `test_eof_ends_session_and_saves`).
2. **Corrupt or missing progress file.** Expected: missing → empty progress; unparsable JSON → warning on stderr, start fresh, keep a `.bak` copy. Test in Task 5 (`test_missing_file_gives_empty`, `test_corrupt_file_backed_up_and_reset`).
3. **Wikilink variants** (`[[Note|alias]]`, `[[Note#Heading]]`, `![[Embed]]`, links inside fenced code blocks, case differences). Expected: alias/heading stripped, embeds counted, code blocks ignored, matching case-insensitive like Obsidian. Test in Task 9 (`test_find_wikilinks_variants`, `test_links_in_code_blocks_ignored`, `test_case_insensitive_resolution`).
4. **YAML type coercion in the bank** (`answer: No` becomes `False`, `answer: 1.5` becomes a float, an option `yes` becomes `True`). Expected: lint rejects any option or fill/mcq answer that is not a string, with the id in the message. Test in Task 6 (`test_lint_rejects_non_string_options_and_answers`).
5. **`--n` larger than the available questions, or a `--tag` that matches nothing.** Expected: ask everything available; for zero matches print "No questions match" and exit 0 without touching progress. Test in Task 8 (`test_n_larger_than_bank_asks_all`, `test_no_match_exits_cleanly`).

---

## File structure

```
.gitignore
README.md
docs/superpowers/{specs,plans}/
vault/
  .obsidian/app.json, appearance.json, core-plugins.json, community-plugins.json, graph.json
  .obsidian/plugins/obsidian-spaced-repetition/data.json
  00 Home.md
  Templates/Concept.md, Convention.md, Cards.md
  Setup/Snowflake Account.md, Obsidian Setup.md, Quiz Runner.md
  Syllabus/Day 1.md, Day 2.md (stub), Day 3.md (stub)
  Concepts/<20 Day-1 notes>
  Migration/Hadoop to Snowflake Rosetta Stone.md
  Flashcards/Cards - Architecture.md, Cards - Virtual Warehouses.md, Cards - Caching.md, Cards - Editions Accounts and Billing.md
  Memory/Memory Techniques.md, Mnemonics.md, Cheat Sheet Day 1.md
  Project/README.md, Certification/README.md
quiz/
  quiz.py                      entry point, adds its dir to sys.path, calls quizlib.cli.main
  requirements.txt             pyyaml>=6,<7 ; pytest>=8,<9
  quizlib/__init__.py
  quizlib/bank.py              Question dataclass, load_bank, load_named
  quizlib/lint.py              concept_notes, lint_bank
  quizlib/matching.py          Presented, present, check_answer, normalize_fill
  quizlib/leitner.py           Card, update, select_review
  quizlib/progress.py          load_progress, save_progress
  quizlib/stats.py             ConceptStat, per_concept, per_day, weakest, box_distribution
  quizlib/session.py           SessionResult, run_session
  quizlib/cli.py               main(argv) -> int
  bank/day1.yaml
  tests/test_bank.py test_lint.py test_matching.py test_leitner.py test_progress.py test_stats.py test_session.py test_cli.py
tools/
  check_links.py               find_wikilinks, scan_vault, dangling, orphans, unresolved_quiz_concepts, main
  tests/test_check_links.py
project/README.md
```

Run all tests from the repo root with `python3 -m pytest quiz/tests tools/tests -q`. `quiz/tests/conftest.py` inserts `quiz/` into `sys.path`; `tools/tests/conftest.py` inserts `tools/`.

---

### Task 1: Repository and vault skeleton

**Files:**
- Create: `.gitignore`, `README.md`, `quiz/requirements.txt`, `project/README.md`, `vault/Project/README.md`, `vault/Certification/README.md`
- Create: `vault/.obsidian/app.json`, `appearance.json`, `core-plugins.json`, `community-plugins.json`, `graph.json`, `plugins/obsidian-spaced-repetition/data.json`
- Create: `vault/Templates/Concept.md`, `vault/Templates/Convention.md`, `vault/Templates/Cards.md`

**Interfaces:**
- Produces: the vault root `vault/`, the template texts every later content task copies, the `.gitignore` rules.

- [ ] **Step 1: `git init` in the repo root, commit the existing spec**

```bash
cd /Users/damianospara/playground/learn_snowflake && git init -b main && git add docs && git commit -m "docs: design for Snowflake learning environment" -m "Co-Authored-By: Claude Fable 5.1 <noreply@anthropic.com>"
```

- [ ] **Step 2: Write `.gitignore`**

Exact contents:
```
quiz/results/
__pycache__/
.pytest_cache/
*.pyc
vault/.obsidian/workspace.json
vault/.obsidian/workspace-mobile.json
vault/.obsidian/cache
.DS_Store
```

- [ ] **Step 3: Write the Obsidian config files**

`app.json`: `{"alwaysUpdateLinks": true, "newFileLocation": "folder", "newFileFolderPath": "Concepts", "attachmentFolderPath": "Attachments", "useMarkdownLinks": false, "showFrontmatter": true}`

`appearance.json`: `{"baseFontSize": 16}`

`core-plugins.json`: a JSON list containing `"file-explorer"`, `"global-search"`, `"switcher"`, `"graph"`, `"backlink"`, `"outgoing-link"`, `"tag-pane"`, `"page-preview"`, `"templates"`, `"note-composer"`, `"command-palette"`, `"editor-status"`, `"starred"`, `"outline"`, `"word-count"`, `"file-recovery"`.

`community-plugins.json`: `["obsidian-spaced-repetition"]`

`plugins/obsidian-spaced-repetition/data.json`: `{"flashcardTags": ["#flashcards"], "convertFoldersToDecks": false, "cardCommentOnSameLine": false, "burySiblingCards": false, "showContextInCards": true, "flashcardEasyText": "Easy", "flashcardGoodText": "Good", "flashcardHardText": "Hard"}` (the plugin merges these over its defaults; nested tags `#flashcards/day1` become sub-decks automatically).

`graph.json`: Obsidian's format, `colorGroups` entries are `{"query": "...", "color": {"a": 1, "rgb": <int>}}`. Use `path:` queries and these colours (decimal RGB): `path:Concepts` 4886754 (blue 0x4A90E2), `path:Conventions` 5025616 (green 0x4CAF50), `path:Flashcards` 16766720 (yellow 0xFFD700), `path:Syllabus` 15158332 (red 0xE74C3C), `path:Memory` 10181046 (purple 0x9B59B6), `path:Setup` 9868950 (grey 0x969696), `path:Migration` 16750848 (orange 0xFF9800). Other keys: `"showTags": false, "showAttachments": false, "hideUnresolved": false, "showOrphans": true, "showArrow": false, "textFadeMultiplier": 0, "nodeSizeMultiplier": 1.2, "lineSizeMultiplier": 1, "centerStrength": 0.45, "repelStrength": 12, "linkStrength": 1, "linkDistance": 220, "scale": 1, "close": false, "collapse-filter": true, "collapse-color-groups": false, "collapse-display": true, "collapse-forces": true, "search": ""`.

- [ ] **Step 4: Write the three templates**

`Templates/Concept.md` is exactly the anatomy in the spec's "Note anatomy" block, with `{{title}}` as the H1 and placeholders in angle brackets. `Templates/Convention.md`: frontmatter `tags: [convention, day3, naming]`, `docs:`; H1 `Naming - {{title}}`; sections **Rule**, **Pattern** (a code line), **Examples** (a table good / bad), **Why**, **Coming from Hive**, `## Related`. `Templates/Cards.md`: frontmatter `tags: [flashcards/dayN, cards]`, H1 `Cards - {{title}}`, a one-line intro "Cards for: [[A]], [[B]]", then one example of each syntax (single-line, multi-line, cloze) as commented guidance inside an HTML comment so the plugin ignores it.

- [ ] **Step 5: Write `README.md`, `quiz/requirements.txt`, and the three placeholder READMEs**

`README.md` sections: What this is (3 lines), Folder map (the tree above, trimmed), Start here (1. open `vault/` in Obsidian, 2. follow `Setup/Obsidian Setup`, 3. `pip install -r quiz/requirements.txt`, 4. `python3 quiz/quiz.py day1`), Checks (`python3 tools/check_links.py` and `python3 quiz/quiz.py lint`). `project/README.md`, `vault/Project/README.md`, `vault/Certification/README.md`: two lines each saying which phase fills them and linking the spec.

- [ ] **Step 6: Commit**

```bash
git add -A && git commit -m "chore: repo skeleton, Obsidian vault config and templates" -m "Co-Authored-By: Claude Fable 5.1 <noreply@anthropic.com>"
```

---

### Task 2: Question bank loading

**Files:**
- Create: `quiz/quizlib/__init__.py` (empty), `quiz/quizlib/bank.py`, `quiz/tests/conftest.py`, `quiz/tests/test_bank.py`

**Interfaces:**
- Produces:
  ```python
  @dataclass
  class Question:
      id: str; type: str; concept: str; tags: List[str]; difficulty: int
      prompt: str; options: List[str]; answer: Any; explanation: str
      source: str = ""   # bank file stem, e.g. "day1"
  def load_bank(paths: List[Path]) -> List[Question]      # concatenates, sets source from path.stem
  def load_named(bank_dir: Path, name: str) -> List[Question]   # bank_dir / f"{name}.yaml"; raises FileNotFoundError with message "No bank named '<name>' in <bank_dir>"
  def available_banks(bank_dir: Path) -> List[str]        # sorted stems of *.yaml
  ```
  `options` defaults to `[]` for `tf`/`fill`. `answer` is kept exactly as YAML parsed it (lint judges types).

- [ ] **Step 1: Write `quiz/tests/conftest.py`** inserting `Path(__file__).resolve().parents[1]` into `sys.path`, and a fixture `tmp_bank(tmp_path)` that writes a 4-question YAML file (one of each type) named `day1.yaml` and returns `tmp_path`.

- [ ] **Step 2: Write failing tests in `test_bank.py`**

```python
def test_load_named_reads_all_fields(tmp_bank):
    qs = load_named(tmp_bank, "day1")
    assert [q.id for q in qs] == ["d1-arch-001", "d1-arch-002", "d1-arch-003", "d1-arch-004"]
    assert qs[0].type == "mcq" and qs[0].options == ["Cloud Services", "Query Processing", "Database Storage"]
    assert qs[0].source == "day1"
def test_tf_and_fill_have_empty_options(tmp_bank): ...
def test_load_named_missing_raises(tmp_bank):
    with pytest.raises(FileNotFoundError, match="No bank named 'day9'"): load_named(tmp_bank, "day9")
def test_available_banks_sorted(tmp_bank): assert available_banks(tmp_bank) == ["day1"]
```

- [ ] **Step 3: Run `python3 -m pytest quiz/tests/test_bank.py -q`**, expect ImportError.

- [ ] **Step 4: Implement `bank.py`** with `yaml.safe_load`; a file whose top level is not a list raises `ValueError("<path>: bank must be a list of questions")`.

- [ ] **Step 5: Run the tests, expect 4 passed. Commit** `feat(quiz): question bank loading`.

---

### Task 3: Answer presentation and matching

**Files:**
- Create: `quiz/quizlib/matching.py`, `quiz/tests/test_matching.py`

**Interfaces:**
- Consumes: `Question` from Task 2.
- Produces:
  ```python
  LETTERS = "abcdefgh"
  @dataclass
  class Presented:
      question: Question
      options: List[str]              # shuffled copy for mcq/multi, [] otherwise
      def correct_letters(self) -> str   # e.g. "b" or "ac" (sorted), "" for tf/fill
  def present(q: Question, rng: random.Random) -> Presented
  def normalize_fill(s: str) -> str   # lower, strip, collapse inner whitespace, strip trailing . , ; and surrounding quotes/backticks
  def parse_letters(given: str) -> Optional[Set[str]]   # "a, c" / "ac" / "A C" -> {"a","c"}; None if any char not a letter
  def check_answer(p: Presented, given: str) -> Optional[bool]
      # None means "input not understood, re-prompt": a letter outside the options, empty string,
      # tf input not in {t,f,true,false,y,n,yes,no}, fill empty.
  ```

- [ ] **Step 1: Write failing tests**

```python
def test_present_shuffles_deterministically_with_seed(mcq): ...   # same seed same order, options are a permutation
def test_mcq_correct_letter_follows_shuffle(mcq): p = present(mcq, random.Random(3)); assert check_answer(p, p.correct_letters()) is True
def test_mcq_wrong_letter_false_and_out_of_range_none(mcq): ...
def test_multi_requires_exact_set(multi): ...   # "ac" True, "a" False, "a,c" True, "abc" False
def test_tf_accepts_variants(tf): assert check_answer(present(tf, rng), "T") is True; assert check_answer(..., "maybe") is None
def test_fill_normalizes(fill):   # answer ["Query Processing", "compute layer"]
    for s in ["query processing", "  Query   Processing. ", "`compute layer`", '"Compute Layer"']: assert check_answer(..., s) is True
def test_fill_empty_is_none(fill): ...
```

- [ ] **Step 2: Run, expect ImportError. Step 3: Implement. Step 4: Run, expect pass. Step 5: Commit** `feat(quiz): option shuffling and answer matching`.

---

### Task 4: Leitner scheduler

**Files:**
- Create: `quiz/quizlib/leitner.py`, `quiz/tests/test_leitner.py`

**Interfaces:**
- Produces:
  ```python
  MAX_BOX = 3
  @dataclass
  class Card:
      box: int = 1; asked: int = 0; correct: int = 0
      last_asked: Optional[str] = None; last_result: Optional[bool] = None
  def update(card: Card, correct: bool, now: str) -> Card   # returns a new Card; correct: box=min(box+1,3), correct+=1; wrong: box=1; asked+=1; last_* set
  def select_review(progress: Dict[str, Card], all_ids: List[str], rng: random.Random, box3_sample: int = 5) -> List[str]
      # ids not in progress count as box 1. Order: all box-1 ids (shuffled), then all box-2 ids (shuffled), then up to box3_sample box-3 ids (random sample)
  ```

- [ ] **Step 1: Write failing tests**: `test_new_card_defaults`, `test_correct_moves_up_and_caps_at_3`, `test_wrong_resets_to_1_from_any_box`, `test_update_is_pure` (input unchanged), `test_select_review_order_and_unseen_as_box1`, `test_box3_sample_size_respected`.
- [ ] **Step 2–5:** run (fail), implement, run (pass), commit `feat(quiz): Leitner boxes`.

---

### Task 5: Progress persistence

**Files:**
- Create: `quiz/quizlib/progress.py`, `quiz/tests/test_progress.py`

**Interfaces:**
- Consumes: `Card` from Task 4.
- Produces:
  ```python
  def load_progress(path: Path, warn: Callable[[str], None] = _stderr) -> Dict[str, Card]
  def save_progress(path: Path, progress: Dict[str, Card]) -> None   # creates parent dirs; JSON {"version": 1, "cards": {id: asdict(card)}}, sorted keys, indent 2; atomic via temp file + os.replace
  def now_iso() -> str   # UTC, seconds precision, "2026-11-18T09:15:00Z"
  ```

- [ ] **Step 1: Write failing tests**

```python
def test_missing_file_gives_empty(tmp_path): assert load_progress(tmp_path / "p.json") == {}
def test_roundtrip(tmp_path): ...
def test_corrupt_file_backed_up_and_reset(tmp_path):
    p = tmp_path / "p.json"; p.write_text("{not json")
    warnings = []
    assert load_progress(p, warn=warnings.append) == {}
    assert (tmp_path / "p.json.bak").exists() and warnings and "corrupt" in warnings[0].lower()
def test_unknown_version_is_treated_as_corrupt(tmp_path): ...
```

- [ ] **Step 2–5:** run (fail), implement, run (pass), commit `feat(quiz): progress persistence`.

---

### Task 6: Bank lint

**Files:**
- Create: `quiz/quizlib/lint.py`, `quiz/tests/test_lint.py`

**Interfaces:**
- Consumes: `Question`.
- Produces:
  ```python
  ID_RE = re.compile(r"^(d[1-3]|cum)-[a-z]+-\d{3}$")
  TYPES = ("mcq", "multi", "tf", "fill")
  def concept_notes(vault_dir: Path) -> Dict[str, Set[str]]
      # stem -> frontmatter tags, for every *.md under vault_dir/Concepts and vault_dir/Conventions (recursive). Tags read from YAML frontmatter `tags:` as list or single string.
  def lint_bank(questions: List[Question], notes: Dict[str, Set[str]], day: Optional[int] = None) -> List[str]
      # each message starts with the question id (or "coverage:") then ": " then the problem
  ```
  Rules: id matches `ID_RE`; ids unique; type in TYPES; difficulty in {1,2,3}; tags non-empty list of strings; prompt and explanation non-empty strings; `concept` in `notes`; mcq: ≥3 string options, unique, answer is a string equal to one option; multi: ≥3 string options, answer is a list of ≥2 strings all in options; tf: answer is `bool`; fill: answer is a non-empty list of non-empty strings, options empty; coverage: every note in `notes` (restricted to notes whose tags contain `f"day{day}"` when `day` is given) has ≥1 question whose `concept` is that note.

- [ ] **Step 1: Write failing tests** including `test_clean_bank_has_no_errors`, `test_duplicate_id_reported`, `test_mcq_answer_not_in_options`, `test_lint_rejects_non_string_options_and_answers` (an option parsed as `True`, a fill answer parsed as `False`, an mcq answer parsed as `1`), `test_unknown_concept`, `test_coverage_scoped_by_day` (a day2 note with no question passes with `day=1`, fails with `day=None`), `test_concept_notes_reads_frontmatter_tags` (one note with list tags, one with a single string tag, one with no frontmatter → empty set).
- [ ] **Step 2–5:** run (fail), implement, run (pass), commit `feat(quiz): bank lint`.

---

### Task 7: Quiz session

**Files:**
- Create: `quiz/quizlib/session.py`, `quiz/tests/test_session.py`

**Interfaces:**
- Consumes: `present`, `check_answer`, `Presented` (Task 3); `Card`, `update` (Task 4); `now_iso` (Task 5).
- Produces:
  ```python
  @dataclass
  class SessionResult:
      asked: int; correct: int; missed_ids: List[str]; aborted: bool
  def format_question(index: int, total: int, p: Presented) -> str
      # "Q3/30  [Three-Layer Architecture]\n<prompt>\n  a) ...\n  b) ...\n" ; tf shows "(t/f)"; fill shows "(type your answer)"; multi shows "(choose all that apply, e.g. ac)"
  def run_session(questions: List[Question], progress: Dict[str, Card], ask: Callable[[str], str], out: Callable[[str], None], rng: random.Random, vault_dir: Path, now: Callable[[str], str] = now_iso) -> SessionResult
  ```
  Behaviour: for each question, `out(format_question(...))`, then loop `ask("> ")` until `check_answer` is not `None`, printing `Not understood. Answer with <hint>.` on `None`. `ask` raising `EOFError` or `KeyboardInterrupt` sets `aborted=True`, stops, and returns (progress for answered questions already updated). After each answer: `Correct.` or `Wrong. Correct answer: <letters/true/false/first fill answer>`, then the explanation, then `Read: vault/Concepts/<concept>.md` (or `Conventions/` if that file exists instead). After the last question: `Score: <correct>/<asked> (<pct>%)` and, when `missed_ids`, `Missed concepts: <unique concept names, comma separated>`. Progress is updated via `update` after each answer.

- [ ] **Step 1: Write failing tests** with a scripted `ask` from a list and `out` appending to a list:
`test_full_run_scores_and_updates_progress`, `test_invalid_letter_reprompts` (inputs `["z", "a"]` → one "Not understood" line, one answer recorded), `test_eof_ends_session_and_saves` (second `ask` raises EOFError → `aborted is True`, first question's Card updated, second absent), `test_wrong_answer_prints_explanation_and_read_path`, `test_read_path_prefers_conventions_when_concept_lives_there`.
- [ ] **Step 2–5:** run (fail), implement, run (pass), commit `feat(quiz): interactive session`.

---

### Task 8: Stats and CLI

**Files:**
- Create: `quiz/quizlib/stats.py`, `quiz/quizlib/cli.py`, `quiz/quiz.py`, `quiz/tests/test_stats.py`, `quiz/tests/test_cli.py`

**Interfaces:**
- Consumes: everything above.
- Produces:
  ```python
  # stats.py
  @dataclass
  class ConceptStat: name: str; asked: int; correct: int
      @property accuracy -> float   # 0.0 when asked == 0
  def per_concept(progress: Dict[str, Card], questions: List[Question]) -> List[ConceptStat]   # one per distinct concept in questions, sorted by name
  def per_day(progress, questions) -> List[ConceptStat]       # grouped by Question.source
  def weakest(stats: List[ConceptStat], n: int = 5) -> List[ConceptStat]   # asked > 0, ascending accuracy then name
  def box_distribution(progress, all_ids: List[str]) -> Dict[int, int]    # {1: n, 2: n, 3: n}, unseen counted in box 1
  # cli.py
  def main(argv: Optional[List[str]] = None, stdin=None, stdout=None, stderr=None) -> int
  ```
  CLI grammar (argparse): `quiz.py <command> [--n N] [--tag TAG] [--seed S] [--day D] [--vault PATH] [--bank-dir PATH] [--progress PATH]`. `command` is `review`, `stats`, `lint`, or a bank name (any stem returned by `available_banks`). Defaults: `--vault` = `<repo>/vault`, `--bank-dir` = `<repo>/quiz/bank`, `--progress` = `<repo>/quiz/results/progress.json`, where `<repo>` is `Path(__file__).resolve().parents[2]`. Unknown command → stderr `Unknown command 'x'. Banks: day1, ...; or review | stats | lint` and return 2. `--n` and `--tag` filter before shuffling the question order; `--seed` seeds one `random.Random` used for order and option shuffling. Zero matching questions → stdout `No questions match.` return 0, progress untouched. `review` loads all banks, orders by `select_review`, then applies `--n`. `stats` prints per-day accuracy table, weakest five concepts each with `Read: vault/Concepts/<name>.md`, and the box distribution. `lint` runs `lint_bank` over all banks (or only `day{D}` bank when `--day` given, with coverage scoped to that day), prints each message, returns 1 if any.

- [ ] **Step 1: Write failing stats tests**: `test_per_concept_aggregates`, `test_weakest_excludes_unasked_and_sorts`, `test_box_distribution_counts_unseen_as_box1`, `test_per_day_groups_by_source`.
- [ ] **Step 2: Write failing CLI tests** using `main([...], stdin=io.StringIO(...), stdout=io.StringIO())` against a temp vault (two concept notes) and temp bank dir:
`test_runs_named_bank_end_to_end` (answers scripted, output contains `Score: `, progress file written), `test_n_larger_than_bank_asks_all`, `test_no_match_exits_cleanly` (`--tag nothing` → "No questions match.", no progress file), `test_unknown_command_returns_2`, `test_lint_reports_and_returns_1`, `test_stats_after_session_lists_weakest`, `test_review_puts_box1_first` (seed fixed).
- [ ] **Step 3: Run, expect failures. Step 4: Implement `stats.py`, `cli.py`, `quiz.py`.** `quiz.py` body: insert its own directory into `sys.path`, `from quizlib.cli import main`, `sys.exit(main())`.
- [ ] **Step 5: Run `python3 -m pytest quiz/tests -q`, expect all pass. Commit** `feat(quiz): stats and CLI`.

---

### Task 9: Vault link checker

**Files:**
- Create: `tools/check_links.py`, `tools/tests/conftest.py`, `tools/tests/test_check_links.py`

**Interfaces:**
- Consumes: `quizlib.bank.load_bank`, `quizlib.lint.concept_notes` (the script inserts `<repo>/quiz` into `sys.path`).
- Produces (module-level functions, script runnable as `python3 tools/check_links.py [--vault V] [--bank-dir B] [--day D]`):
  ```python
  WIKILINK_RE   # matches [[...]] and ![[...]]
  def find_wikilinks(text: str) -> Set[str]     # strips alias (|), heading (#), block (^); ignores fenced ``` blocks and inline `code`
  @dataclass
  class VaultIndex:
      notes: Dict[str, Path]           # key: stem.lower()
      display: Dict[str, str]          # stem.lower() -> stem as written
      links: Dict[str, Set[str]]       # source stem.lower() -> target stem.lower()
      tags: Dict[str, Set[str]]        # stem.lower() -> frontmatter tags
  def scan_vault(vault_dir: Path, skip_dirs: Tuple[str, ...] = ("Templates", ".obsidian")) -> VaultIndex
  def dangling(index: VaultIndex) -> List[Tuple[str, str]]          # (source display, missing target as written in link)
  def orphans(index: VaultIndex, folders: Tuple[str, ...] = ("Concepts", "Conventions"), day: Optional[int] = None) -> List[str]
      # notes in those folders with zero inbound links; when day given, only notes tagged day{day}
  def unresolved_quiz_concepts(concepts: Set[str], index: VaultIndex) -> List[str]
  def main(argv=None) -> int   # prints "OK: N notes, M links" or each problem on its own line prefixed "DANGLING", "ORPHAN", "QUIZ"; returns 1 on any problem
  ```
  Duplicate stems in different folders → reported as `DUPLICATE <stem>` and return 1 (Obsidian link resolution would be ambiguous).

- [ ] **Step 1: Write failing tests** against a temp vault built by a fixture: `test_find_wikilinks_variants` (`[[A]]`, `[[B|alias]]`, `[[C#Head]]`, `![[D]]`, `[[E^blk]]` → {A,B,C,D,E}), `test_links_in_code_blocks_ignored`, `test_case_insensitive_resolution` (link `[[virtual warehouse]]` resolves to `Virtual Warehouse.md`), `test_dangling_reported_with_source`, `test_orphans_only_in_concept_folders_and_scoped_by_day`, `test_templates_skipped`, `test_duplicate_stems_reported`, `test_main_returns_1_on_problem_and_0_when_clean`.
- [ ] **Step 2–5:** run (fail), implement, run (pass), commit `feat(tools): vault link checker`.

---

### Task 10: Setup notes, Home, syllabus stubs

**Files:**
- Create: `vault/00 Home.md`, `vault/Setup/Snowflake Account.md`, `vault/Setup/Obsidian Setup.md`, `vault/Setup/Quiz Runner.md`, `vault/Syllabus/Day 1.md` (structure only; concept list filled in Task 14), `vault/Syllabus/Day 2.md`, `vault/Syllabus/Day 3.md`

**Interfaces:**
- Produces: the note titles `00 Home`, `Snowflake Account`, `Obsidian Setup`, `Quiz Runner`, `Day 1`, `Day 2`, `Day 3` that later tasks link to.

- [ ] **Step 1: Write `00 Home.md`** (tags `[home]`): one-paragraph purpose; "Start here" numbered list linking `[[Obsidian Setup]]`, `[[Snowflake Account]]`, `[[Quiz Runner]]`; "Syllabus" linking `[[Day 1]]`, `[[Day 2]]`, `[[Day 3]]`; "Memory" linking `[[Memory Techniques]]`, `[[Mnemonics]]`, `[[Cheat Sheet Day 1]]`; "Bridge" linking `[[Hadoop to Snowflake Rosetta Stone]]`; "Progress" as a checklist of 9 items (3 per day: read, hands-on, quiz passed ≥ 80%).
- [ ] **Step 2: Write `Snowflake Account.md`** (tags `[setup]`): section "Which account" with the two SQL lines `SHOW GRANTS TO USER <your_user>;` and `SELECT CURRENT_ACCOUNT_NAME(), CURRENT_REGION(), CURRENT_ROLE();` and the rule: use the team account only if it is non-production and the grants include `ACCOUNTADMIN`, or both `SYSADMIN` and `SECURITYADMIN`; otherwise "Trial account" section with steps: signup.snowflake.com, Enterprise edition, cloud and region nearest to the team, verify email, save the account identifier (`<orgname>-<account_name>`), first Snowsight login, create a warehouse named `WH_LEARN_XS` size X-Small with auto-suspend 60 seconds. Both sections carry the `> [!warning] Not yet executed by the author` callout.
- [ ] **Step 3: Write `Obsidian Setup.md`** (tags `[setup]`): open `vault/` as vault; Settings → Community plugins → Turn on → Browse → install and enable "Spaced Repetition"; open graph view and confirm seven colour groups; open the Spaced Repetition sidebar icon and confirm deck `flashcards` with sub-deck `day1`; how to review (Hard/Good/Easy); note that scheduling is written into the card notes as HTML comments and is committed.
- [ ] **Step 4: Write `Quiz Runner.md`** (tags `[setup]`): install, the five commands with one line each, the pass bar (80 %), how `review` works (three boxes), and that results live in `quiz/results/progress.json`.
- [ ] **Step 5: Write `Syllabus/Day 1.md` header** (tags `[syllabus, day1]`): title "Day 1 - The big picture", the rhythm block from the spec (read 60–90 min → hands-on 45 → flashcards 15 → `quiz.py day1` 20 → Feynman 10), empty `## Read in this order`, `## Hadoop bridge`, `## Hands-on in Snowsight`, `## Drill` sections to be filled in Task 14. Write `Day 2.md` and `Day 3.md` as stubs: tags `[syllabus, day2]`/`[syllabus, day3]`, title, one line "Coming in increment 2/3", link back to `[[00 Home]]`.
- [ ] **Step 6: Run `python3 tools/check_links.py --day 1`.** Expected: DANGLING lines for `Memory Techniques`, `Mnemonics`, `Cheat Sheet Day 1`, `Hadoop to Snowflake Rosetta Stone` only (created in Tasks 13 and 12). Commit `docs(vault): home, setup notes, syllabus stubs`.

---

### Task 11: Day 1 concept notes, batch A — architecture and storage

**Files:**
- Create in `vault/Concepts/`: `What Snowflake Is.md`, `Three-Layer Architecture.md`, `Cloud Services Layer.md`, `Query Processing Layer.md`, `Database Storage Layer.md`, `Micro-partitions.md`, `Clustering Keys.md`, `Query Pruning.md`

**Interfaces:**
- Produces: those eight note titles. Later batches link to them.

Pinned facts (verify each against the `docs:` URL you put in the note; if docs disagree, docs win and you note the discrepancy in the commit message):
- Architecture: three layers, Cloud Services / Query Processing / Database Storage; described by Snowflake as a hybrid of shared-disk (central storage all compute can reach) and shared-nothing (MPP compute clusters each holding part of the data locally during a query). Docs: `https://docs.snowflake.com/en/user-guide/intro-key-concepts`.
- Cloud Services: authentication, infrastructure management, metadata management, query parsing and optimisation, access control. Billed only when daily cloud-services usage exceeds 10 % of daily warehouse compute credits.
- Storage: columnar, compressed, encrypted, stored in the cloud provider's object storage; customers pay for compressed size; not directly accessible, only via SQL.
- Micro-partitions: contiguous units of 50–500 MB uncompressed; columnar within; immutable; metadata per partition includes min/max per column, distinct counts, null counts; created automatically on load in insertion order. Docs: `https://docs.snowflake.com/en/user-guide/tables-clustering-micropartitions`.
- Clustering keys: explicit `CLUSTER BY`, maintained by Automatic Clustering (a serverless feature that costs credits); worthwhile only for very large tables (multi-TB) with filter/join columns; `SYSTEM$CLUSTERING_INFORMATION`. Hadoop break: Hive partitions are directories you design and must filter on exactly; micro-partitions are automatic and pruning works on any column with good natural ordering.
- Query pruning: the optimizer uses micro-partition metadata to skip partitions whose min/max cannot match the predicate; visible in Query Profile as "Partitions scanned / Partitions total".

- [ ] **Step 1: For each note, fetch its `docs:` page with the web-fetch agent and confirm the pinned facts.** Record any correction.
- [ ] **Step 2: Write the eight notes from `Templates/Concept.md`.** Each `## Related` has ≥3 links; links among this batch plus forward links to `[[Virtual Warehouse]]`, `[[Caching]]`, `[[Hadoop to Snowflake Rosetta Stone]]` are allowed (they resolve by Task 13). Tags: `[concept, day1, architecture]` (storage notes: `storage`).
- [ ] **Step 3: Run `python3 tools/check_links.py --day 1`.** Expected: only DANGLING targets that Tasks 12–14 create (Virtual Warehouse, Caching, Rosetta Stone, Memory notes) and ORPHAN lines for notes not yet linked from Day 1 (filled in Task 14). No typos in any target that already exists.
- [ ] **Step 4: Commit** `docs(vault): day 1 concepts, architecture and storage`.

---

### Task 12: Day 1 concept notes, batch B — compute, caching, platform

**Files:**
- Create in `vault/Concepts/`: `Virtual Warehouse.md`, `Warehouse Sizes and Credits.md`, `Auto-suspend and Auto-resume.md`, `Scaling Up vs Scaling Out.md`, `Multi-cluster Warehouse.md`, `Caching.md`, `Result Cache.md`, `Warehouse Cache.md`, `Metadata Cache.md`, `Snowflake Editions.md`, `Cloud Providers and Regions.md`, `Organizations and Accounts.md`, `Snowsight.md`, `Credits and Billing.md`
- Create: `vault/Migration/Hadoop to Snowflake Rosetta Stone.md`

Pinned facts (verify against docs as in Task 11):
- Warehouse: a named cluster of compute; sizes X-Small through 6X-Large; credits per hour double per size: XS 1, S 2, M 4, L 8, XL 16, 2XL 32, 3XL 64, 4XL 128, 5XL 256, 6XL 512; billed per second with a 60-second minimum each time it starts or resumes; resizing takes effect for new queries. Docs: `https://docs.snowflake.com/en/user-guide/warehouses-overview`, `.../warehouses-considerations`.
- Auto-suspend default via SQL `AUTO_SUSPEND = 600` seconds; `AUTO_RESUME = TRUE` default; suspending drops the warehouse cache.
- Scaling up = bigger size for heavier single queries; scaling out = more clusters for concurrency (multi-cluster, Enterprise+); multi-cluster modes Maximized (min = max) and Auto-scale (min < max), scaling policies Standard and Economy; max 10 clusters.
- Caches: Result Cache in Cloud Services, exact-same query text, same role, underlying data unchanged, result reused for 24 h, and each reuse extends it, up to 31 days total; Warehouse (local disk) cache holds raw table data on the warehouse's SSD, lost on suspend; Metadata cache in Cloud Services answers `COUNT(*)`, `MIN`, `MAX` on whole tables without a running warehouse. Docs: `https://docs.snowflake.com/en/user-guide/querying-persisted-results`.
- Editions: Standard, Enterprise (multi-cluster, Time Travel up to 90 days, materialized views, search optimization, column-level security), Business Critical (HIPAA/PCI, Tri-Secret Secure, private connectivity, database failover), Virtual Private Snowflake (dedicated isolated environment). Docs: `https://docs.snowflake.com/en/user-guide/intro-editions`.
- Providers: AWS, Azure, Google Cloud; an account lives in one region of one provider; account identifier `<orgname>-<account_name>`; cross-region/cloud via replication. Organization groups accounts, `ORGADMIN` role.
- Snowsight: the web UI; worksheets, Query Profile, Activity → Query History, Admin → Warehouses / Cost Management.
- Billing: three meters, compute (credits), storage (per compressed TB per month), data transfer (egress); serverless features (Snowpipe, Automatic Clustering, tasks without a warehouse) bill credits without a user warehouse. Docs: `https://docs.snowflake.com/en/user-guide/cost-understanding-overall`.
- Rosetta Stone (tags `[migration, day1]`): a table with columns Cloudera / Snowflake / Where it breaks / Note, one row per concept note in Day 1 (HDFS → Database Storage Layer; Parquet/ORC files → micro-partitions; YARN queue + Spark executors → Virtual Warehouse; cluster sizing → Warehouse Sizes; keeping a cluster warm → Auto-suspend; adding nodes → Scaling Up vs Scaling Out; Hive Metastore → Cloud Services Layer / Metadata Cache; Hive partitions and bucketing → Clustering Keys / Query Pruning; Spark cache → Warehouse Cache; Hue → Snowsight; CDH licence tiers → Snowflake Editions; on-prem datacentre → Cloud Providers and Regions; Cloudera Manager cluster → Organizations and Accounts; node-hours → Credits and Billing). Every Snowflake cell is a wikilink. Section "Rows added on Day 2 and Day 3" left as an empty heading.

- [ ] **Step 1: Fetch each `docs:` page and confirm the pinned facts.**
- [ ] **Step 2: Write the fourteen concept notes and the Rosetta Stone.** `Caching` links down to the three cache notes; each cache note links up to `[[Caching]]` and sideways to the other two. Every concept note's "Coming from Hadoop" line ends with `(see [[Hadoop to Snowflake Rosetta Stone]])`.
- [ ] **Step 3: Run `python3 tools/check_links.py --day 1`.** Expected: DANGLING only for the Memory notes; ORPHAN lines only for notes not yet linked from `Day 1`.
- [ ] **Step 4: Commit** `docs(vault): day 1 concepts, compute/caching/platform, and Rosetta Stone`.

---

### Task 13: Day 1 flashcards and memory notes

**Files:**
- Create: `vault/Flashcards/Cards - Architecture.md`, `Cards - Virtual Warehouses.md`, `Cards - Caching.md`, `Cards - Editions Accounts and Billing.md`
- Create: `vault/Memory/Memory Techniques.md`, `vault/Memory/Mnemonics.md`, `vault/Memory/Cheat Sheet Day 1.md`

Card allocation (35–45 total): Architecture 12 (covers What Snowflake Is, Three-Layer Architecture, the three layer notes, Micro-partitions, Clustering Keys, Query Pruning), Virtual Warehouses 12 (Virtual Warehouse, Sizes and Credits, Auto-suspend, Scaling, Multi-cluster), Caching 7 (Caching + three caches), Editions Accounts and Billing 9 (Editions, Providers, Organizations, Snowsight, Billing). Mix: about 60 % single-line `::`, 25 % multi-line `?`, 15 % cloze `==`. Every answer side contains the concept wikilink. At least one card per concept note. Frontmatter `tags: [flashcards/day1, cards]`.

Memory notes (tags `[memory]`):
- `Memory Techniques.md`: one section per technique named in the spec (spaced repetition, active recall, Feynman, chunking, memory palace, interleaving, one-page cheat sheet) with 3–5 lines each and a concrete Snowflake example; "The Snowflake building" palace: basement = Database Storage (rows of boxes = micro-partitions), office floors = Query Processing (each office a warehouse, lights off = suspended, bigger offices = bigger sizes, more offices on a floor = multi-cluster), roof = Cloud Services (the receptionist with the metadata ledger and the result cache noticeboard). Links to `[[Mnemonics]]`, `[[Cheat Sheet Day 1]]`, `[[Quiz Runner]]`, `[[Obsidian Setup]]`.
- `Mnemonics.md`: Day 1 entries only in this increment, each with the list, the mnemonic, and a wikilink: the three layers; warehouse sizes and credits (doubling from 1); the three caches and their homes and lifetimes (24 h / lost on suspend / always); the four editions in order; the 10 % cloud-services rule; multi-cluster policies. Headings `## Day 2` and `## Day 3` left empty with one line "added in increment 2/3".
- `Cheat Sheet Day 1.md`: one printable page: architecture diagram in text, sizes/credits table, caches table, editions table, five Hadoop mappings, five exam traps. Every term is a wikilink.

- [ ] **Step 1: Write the four card notes.** Check: `grep -c '::' ` plus multi-line and cloze counts land in 35–45; every `Concepts/` day1 stem appears in at least one card note.
- [ ] **Step 2: Write the three memory notes.**
- [ ] **Step 3: Run `python3 tools/check_links.py --day 1`.** Expected: zero DANGLING; ORPHAN lines only for concept notes not yet in `Day 1` (if any remain, fix in Task 14).
- [ ] **Step 4: Commit** `docs(vault): day 1 flashcards, memory techniques, mnemonics, cheat sheet`.

---

### Task 14: Day 1 quiz bank and syllabus

**Files:**
- Create: `quiz/bank/day1.yaml`
- Modify: `vault/Syllabus/Day 1.md` (fill the four sections)

Bank: 30 questions, ids `d1-<area>-NNN` with areas `arch`, `store`, `wh`, `cache`, `plat`, `mig`; types roughly 16 mcq, 4 multi, 5 tf, 5 fill; difficulty 15/10/5; 5 questions tagged `migration` of the form "On Cloudera you did X. What is the Snowflake way?"; every day1 concept note (22 incl. none from Conventions) is the `concept` of at least one question; every `explanation` is one or two sentences that teach, not just restate.

- [ ] **Step 1: Write `day1.yaml`.**
- [ ] **Step 2: Run `python3 quiz/quiz.py lint --day 1`.** Expected: no output lines, exit 0. Fix until clean.
- [ ] **Step 3: Fill `Syllabus/Day 1.md`:** `## Read in this order` lists all 22 day-1 concept notes as wikilinks in teaching order (What Snowflake Is → Three-Layer → the three layers → Micro-partitions → Pruning → Clustering → Virtual Warehouse → Sizes → Auto-suspend → Scaling → Multi-cluster → Caching → three caches → Editions → Providers → Organizations → Snowsight → Billing); `## Hadoop bridge` links `[[Hadoop to Snowflake Rosetta Stone]]` and lists the five Day 1 mappings from the spec; `## Hands-on in Snowsight` (with the not-yet-executed callout): the steps from `[[Snowflake Account]]`, then create `WH_LEARN_XS`, run `SELECT COUNT(*) FROM SNOWFLAKE_SAMPLE_DATA.TPCH_SF1.LINEITEM;` twice and open Query Profile to see the second run served from the result cache, run a filtered query on `L_SHIPDATE` and read "Partitions scanned" vs "total", suspend the warehouse and run the count again to see the metadata cache answer with the warehouse still suspended; `## Drill`: review deck `flashcards/day1`, run `python3 quiz/quiz.py day1`, pass bar 80 %, then `review`; `## Acceptance` checklist: vault opens, graph shows seven colour groups, Spaced Repetition shows deck day1 with 35–45 cards, `quiz.py day1` runs end to end, `check_links.py` and `quiz.py lint` are clean.
- [ ] **Step 4: Run the full gates:** `python3 tools/check_links.py --day 1` → `OK`, `python3 quiz/quiz.py lint --day 1` → clean, `python3 -m pytest quiz/tests tools/tests -q` → all pass. Also run the unscoped `python3 tools/check_links.py` and `python3 quiz/quiz.py lint`; both must be clean too, because Day 2/3 stubs contain no concept notes.
- [ ] **Step 5: Smoke-run the quiz by hand:** `printf 'a\n' | python3 quiz/quiz.py day1 --n 1 --seed 1` prints a question, a verdict, an explanation, a `Read:` path and a `Score:` line, exit 0.
- [ ] **Step 6: Commit** `feat: day 1 quiz bank and syllabus; increment 1 complete`.

---

### Task 15: Increment 1 hand-over

- [ ] **Step 1: Re-read `Syllabus/Day 1.md` and `00 Home.md` as the learner would**, fix anything that assumes knowledge not yet taught.
- [ ] **Step 2: Produce the hand-over message** for Damianos: where to open the vault, the two setup notes to follow first, the Day 1 acceptance checklist, and the three things marked "not yet executed by the author" that they should report back on.
