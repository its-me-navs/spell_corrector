# Norvig Spell Checker

A Python implementation of Peter Norvig's statistical spell checker.

## How It Works

Generates all strings 1-2 edits away from a misspelled word (deletes, inserts, transposes, replaces), then picks the candidate that appears most frequently in a training corpus.

## Setup

Download the training corpus:
```python
import urllib.request
urllib.request.urlretrieve("https://norvig.com/big.txt", "big.txt")
```

Then run:
```bash
python spell_checker.py
```

## Limitations

- No context awareness — valid words are never corrected even if wrong in context
- Corpus quality matters more than size — web-scale data worsened accuracy due to informal spellings being treated as valid words

## Changelog

### v0.1.0 — 2026-03-20
- Unigram spell checker using Norvig's algorithm
- Punctuation-aware correction and case restoration
- Rolled back web-scale corpus augmentation because it introduced informal spellings as valid words, worsening accuracy

## Reference
[Peter Norvig — How to Write a Spelling Corrector](https://norvig.com/spell-correct.html)