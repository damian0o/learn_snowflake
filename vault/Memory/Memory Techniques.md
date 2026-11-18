---
tags: [memory]
---
# Memory Techniques

Seven techniques, each wired into this vault so you use them without thinking about it. The quiz and the cards are not a test of what you know; they are the way you learn it.

## 1. Spaced repetition

Review a fact just before you would forget it, and the interval grows each time. The Spaced Repetition plugin does the scheduling: open the deck `flashcards/day1` once a day and grade honestly (Hard, Good, Easy). Ten minutes a day beats an hour on Sunday. Setup: [[Obsidian Setup]].

## 2. Active recall

Retrieving a fact strengthens it; rereading does not. That is why every card asks a question before it shows the answer, and why the [[Quiz Runner]] makes you answer before it explains. Rule: never flip a card or type an answer before you have committed to one in your head.

## 3. The Feynman technique

Every concept note ends with **Explain it to a teammate (fill in yourself)**. Write two sentences a Hadoop colleague would understand, with no Snowflake jargon. If you cannot, you have found the gap; reread the "How it works" section and try again. Example for [[Result Cache]]: "If anyone ran this exact query today and nothing changed in the tables, Snowflake hands back the saved answer without starting any compute."

## 4. Chunking

Twenty-two facts are hard; four groups of five are easy. Day 1 is chunked into architecture, warehouses, caching, and platform, and the flashcard notes follow the same four chunks. When a list is long (editions, sizes, caches), learn the shape first (how many, in what order), then the items.

## 5. The memory palace: the Snowflake building

Walk through one building and put every Day 1 fact in a room.

- **Basement: Database Storage.** Rows of identical sealed boxes, 50 to 500 MB each: the [[Micro-partitions]]. Each box has a label listing the min and max of everything inside (the metadata). Nobody enters the basement; you request boxes through a hatch (SQL only). Old boxes are never opened and repacked, new ones are added (immutability). A worker occasionally re-sorts boxes by one label so that related ones sit together ([[Clustering Keys]]).
- **Office floors: Compute.** Each office is a [[Virtual Warehouse]]. Bigger offices have twice the desks and twice the rent (sizes and credits). Lights off means suspended and free, but the whiteboards get wiped ([[Warehouse Cache]] lost). A busy floor can open identical offices next door at peak ([[Multi-cluster Warehouse]]).
- **Roof: Cloud Services.** The receptionist checks your badge (authentication, roles), keeps the ledger of every box's label ([[Metadata Cache]]) so some questions ("how many boxes?") are answered at the desk, and pins the answer to every recent question on a noticeboard for 24 hours ([[Result Cache]]). The receptionist works for free unless you keep her busier than 10 % of the office rent.

Rehearse the walk once a day for a week; it takes under a minute.

## 6. Interleaving

Mixing topics in one session is harder and sticks better than drilling one. `python3 quiz/quiz.py day1` shuffles across all four chunks; on Day 3 the cumulative quiz mixes all three days. Resist the urge to filter the quiz to one tag except when repairing a specific weak spot (`stats` tells you which).

## 7. One-page cheat sheet

Compress a day onto one page in your own hand. [[Cheat Sheet Day 1]] is a model; print it, stick it on the wall by your desk, and after a week try to rewrite it from memory. This is the "yellow card" trick: the act of compressing is the learning, the card on the wall is the reminder.

## Putting it together, daily

1. Review the flashcard deck (10 min).
2. Read today's notes, filling in the Feynman box as you go.
3. Run the quiz; for anything missed, reread the note it points at, then `review`.
4. Walk the building once before you close the laptop.

See also [[Mnemonics]] for the hard lists.
