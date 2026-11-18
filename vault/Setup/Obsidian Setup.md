---
tags: [setup]
---
# Obsidian Setup

1. In Obsidian choose **Open folder as vault** and pick the `vault/` folder of this repository. Choose *Trust author and enable plugins* if asked.
2. Settings → Community plugins → **Turn on community plugins** → Browse → search **Spaced Repetition** (by Stephen Mwangi) → Install → Enable.
3. Open the graph view (left ribbon, or `Ctrl/Cmd+G`). You should see seven colour groups already configured: Concepts blue, Conventions green, Flashcards yellow, Syllabus red, Memory purple, Setup grey, Migration orange.
4. Click the Spaced Repetition icon in the left ribbon (a stack of cards). The deck list should show `flashcards` with a sub-deck `day1`. Days 2 and 3 appear when their cards are written.

## How flashcards work here

- Cards live in notes under `Flashcards/`, in plain text: `Question::Answer` on one line, or a question, a line with `?`, then the answer. `==highlighted==` text becomes a cloze.
- Review a deck: click it, read the question, press to reveal, then grade yourself **Hard**, **Good** or **Easy**. The plugin schedules the next review and writes that schedule into the card note as an HTML comment like `<!--SR:!2026-11-21,3,250-->`. Those comments are committed with the vault, so your review history travels with it.
- Every answer links to the concept note. If a card surprises you, click through and reread.

## Related

- [[00 Home]]
- [[Memory Techniques]]
- [[Quiz Runner]]
