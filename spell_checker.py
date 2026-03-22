""" 
Norvig's Spell Checker (Unigram + Bigram)
Algorithm: edit distance (deletes, inserts, transposes, replaces) + corpus frequency
Bigram context: uses previous word to disambiguate candidates via conditional probability
Limitation: no context awareness beyond one previous word. 

"""

import re
from collections import Counter
import nltk
import nltk.data

try:
    nltk.data.find('corpora/brown')
except LookupError:
    nltk.download('brown')
from nltk.corpus import brown

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
    word_list=words(open("big.txt").read()) + [w.lower() for w in brown.words()]
    WORDS=Counter(word_list)
    BIGRAMS=Counter(zip(word_list, word_list[1:]))
    return WORDS, BIGRAMS

WORDS, BIGRAMS=create_words()

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
    return max(candidates(word), key=prob)

###### unigram done, bigram below

def prob_bigram(prev_word, cur_word):
        if WORDS[prev_word]!=0:
            bigram_prob = BIGRAMS[(prev_word, cur_word)] / WORDS[prev_word]
            return bigram_prob if bigram_prob > 0 else prob(cur_word)
        return prob(cur_word)

def correction_bigram(prev_word, cur_word):
    return max(candidates(cur_word), key=lambda x: prob_bigram(prev_word,x))

def correct_sentence(sentence):
    word_list=sentence.split()
    corrected=[]
    for i, word in enumerate(word_list):
        match=re.match(r'^([^a-zA-Z]*)([a-zA-Z]+)([^a-zA-Z]*)', word)
        if not match:
            corrected.append(word)
            continue
        prefix, core, suffix=match.groups()
        prev_word=corrected[i-1] if i>0 else None
        if prev_word:
            prev_word=re.sub(r'[^a-zA-Z]', '', prev_word).lower()
            fixed=correction_bigram(prev_word, core.lower())
        else:
            fixed=correction(core.lower())
        if core.isupper():
            fixed=fixed.upper()
        elif core[0].isupper():
            fixed=fixed.capitalize()
        corrected.append(prefix+fixed+suffix)
    return ' '.join(corrected)

def check():
    sen=input("Enter a sentence to correct : ")
    print(correct_sentence(sen))

check()