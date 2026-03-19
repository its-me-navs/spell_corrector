""" 
Norvig's Unigram Spell Checker
Algorithm: edit distance (deletes, inserts, transposes, replaces) + corpus frequency
Limitation: no context awareness — selects highest frequency candidate regardless
of surrounding words. Attempted augmenting with count_1w.txt (web-scale corpus)
but it introduced informal spellings as valid words, worsening accuracy. Rolled back to big.txt only.

"""

import re
import os
import urllib.request
from collections import Counter

def words(text): 
    return re.findall(r'\w+', text.lower())

def edits1(word):
    "All edits that are 1 edit away from the word 'word' "
    letters='abcdefghijklmnopqrstuvwxyz'
    splits=[(word[:i],word[i:]) for i in range(len(word)+1)]
    deletes=[L+R[1:] for L,R in splits]
    inserts=[L+c+R for L,R in splits for c in letters]
    transposes=[L+R[1]+R[0]+R[2:] for L,R in splits if len(R)>1]  # swapping two adjacent characters
    replaces=[L+c+R[1:] for L,R in splits for c in letters]
    return set(deletes + inserts + transposes + replaces)  # set because it  removes duplicates

def edits2(word):
    "All edits that are 2 edits away from the word 'word' "
    return (e2 for e1 in edits1(word) for e2 in edits1(e1))  # creates a generator - () - produces output on demand, not all at once

def create_words():
    WORDS=Counter(words(open("big.txt").read()))
    return WORDS

WORDS=create_words()

def prob(word, N=sum(WORDS.values())):
    "Probability of the word 'word' "
    return WORDS[word]/N

def known(words):
    "Subsets of 'words' that appear in the dictionary 'WORDS' "
    return set(w for w in words if w in WORDS)

def candidates(word):
    "Generate possible correct spellings of the word 'word' "
    return (known([word]) or known(edits1(word)) or known(edits2(word)) or [word])

def correction(word):
    "Most probable correct spelling of the word 'word' "
    return max(candidates(word), key=prob)

def correct_word(word):
    match=re.match(r'^([^a-zA-Z]*)([a-zA-Z]+)([^a-zA-Z]*)', word)
    if not match:
        return word
    prefix, core, suffix=match.groups()
    corrected=correction(core.lower())
    if core.isupper():
        corrected=corrected.upper()
    elif core[0].isupper():
        corrected=corrected.capitalize()
    return prefix+corrected+suffix

def correct_sentence(sentence):
    return ' '.join(correct_word(word) for word in sentence.split())

def check():
    sen=input("Enter a sentence to correct : ")
    print(correct_sentence(sen))

check()

