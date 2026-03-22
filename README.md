# Norvig Spell Checker

A Python implementation of Peter Norvig's statistical spell checker, extended with bigram context.

## How It Works

Generates all strings 1-2 edits away from a misspelled word (deletes, inserts, transposes, replaces), then picks the candidate with the highest probability given the previous word. Falls back to unigram frequency for the first word in a sentence.

## Setup

Download the training corpus:
```python
import urllib.request
urllib.request.urlretrieve("https://norvig.com/big.txt", "big.txt")
```

The Brown corpus is downloaded automatically via NLTK on first run.

Then run:
```bash
python spell_checker.py
```

## Limitations

- Valid words are never corrected even if wrong in context
- High-frequency words can still override correct low-frequency corrections
- Corpus startup time is ~5 seconds on first load
- Corpus quality matters more than size — web-scale data worsened accuracy due to informal spellings being treated as valid words

## Changelog

### v0.2.0 — 2026-03-22
- Added bigram context: correction now uses the previous word as context
- Replaced unigram `correct_sentence` with bigram-aware version

### v0.1.0 — 2026-03-20
- Unigram spell checker using Norvig's algorithm
- Punctuation-aware correction and case restoration
- Rolled back web-scale corpus augmentation because it introduced informal spellings as valid words, worsening accuracy

## Reference
[Peter Norvig — How to Write a Spelling Corrector](https://norvig.com/spell-correct.html)