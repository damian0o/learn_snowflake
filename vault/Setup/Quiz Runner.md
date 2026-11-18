---
tags: [setup]
---
# Quiz Runner

The interactive tests run in your terminal from the repository root.

```
pip install -r quiz/requirements.txt
```

| Command | What it does |
|---------|--------------|
| `python3 quiz/quiz.py day1` | Every Day 1 question, shuffled, with explanation after each answer and a score at the end |
| `python3 quiz/quiz.py day1 --n 10 --tag migration` | A subset: at most 10 questions, only those tagged `migration` |
| `python3 quiz/quiz.py review` | Re-asks what you got wrong (Leitner boxes, below) |
| `python3 quiz/quiz.py stats` | Accuracy per day, your five weakest concepts with the note to reread, box distribution |
| `python3 quiz/quiz.py lint` | Checks the question bank itself; used by the author |

Answer multiple choice with a letter (`b`), multi-select with all the letters (`ac`), true/false with `t` or `f`, and fill-in questions with a short answer (case and punctuation do not matter). Press `Ctrl+D` to stop early; answered questions are saved.

**Pass bar:** 80 %. Below that, run `review` until the missed questions come back right, reread the notes it points at, then take the day's quiz again.

## Leitner boxes

Every question sits in one of three boxes. New and missed questions are in box 1. Each correct answer moves a question up one box; a wrong answer sends it back to box 1. `review` asks box 1 first, then box 2, then a handful from box 3 so known things are not forgotten. This is the same idea as the flashcards in [[Obsidian Setup]], applied to test questions.

Results are stored in `quiz/results/progress.json` (ignored by git). Delete that file to start over.

## Related

- [[00 Home]]
- [[Memory Techniques]]
