# Spellr — Norvig Spell Checker

A Python implementation of Peter Norvig's statistical spell checker, extended with 
bigram context and a keyboard-aware noisy channel model. Served via FastAPI with a 
minimal web frontend.

![demo](demo.gif)

## How It Works

Uses the **noisy channel model**:
```
P(intended | typed) ∝ P(typed | intended) × P(intended)
                         channel model       language model
```

1. **Candidate generation** — all strings 1-2 edits away (delete, insert, transpose, replace)
2. **Language model** — unigram + bigram frequency from Brown corpus, Gutenberg, and big.txt
3. **Channel model** — keyboard adjacency scoring per edit type (transpose > adjacent replace > far replace)
4. **Bigram context** — uses previous word to disambiguate candidates via conditional probability

## Example

| Input | Output | Why |
|-------|--------|-----|
| "teh" | "the" | transpose detected, high channel score |
| "say helo" | "say hello" | bigram context disambiguates from "help" |
| "I recieve" | "I receive" | transpose: i↔e |

## Setup

Download the training corpus:
```python
import urllib.request
urllib.request.urlretrieve("https://norvig.com/big.txt", "big.txt")
```

NLTK corpora download automatically on first run. Then:
```bash
pip install -r requirements.txt
uvicorn main:app --reload
```

Open `index.html` in your browser.

## Limitations

- Edit distance capped at 2 — words 3+ edits away are unreachable
- High-frequency words can override correct low-frequency corrections in isolation 
  (e.g. "helo" → "help" without context, "say helo" → "say hello" with context)
- No sentence-level optimization — corrects left to right, not globally
- ~5 second startup due to corpus loading

## Changelog

### v0.3.0 
- Added keyboard-aware noisy channel model
- FastAPI backend + HTML/JS frontend

### v0.2.0
- Added bigram context: correction now uses the previous word as context
- Replaced unigram `correct_sentence` with bigram-aware version

### v0.1.0 
- Unigram spell checker using Norvig's algorithm
- Punctuation-aware correction and case restoration
- Rolled back web-scale corpus augmentation because it introduced informal spellings as valid words, worsening accuracy

## Reference
[Peter Norvig — How to Write a Spelling Corrector](https://norvig.com/spell-correct.html)