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

###### unigram done, bigram below

def prob_bigram(prev_word, cur_word, V=len(WORDS)):
        return (BIGRAMS[(prev_word, cur_word)]+1)/(WORDS[prev_word]+V)

######## - channel model - correct typos based on keyboard distance

KEYBOARD={
    'a':'qwsz', 'b':'vghn', 'c':'xdfv', 'd':'serfcx', 'e':'wsdr','f':'drtgvc', 'g':'ftyhbv', 'h':'gyujnb','i':'ujko', 'j':'huikmn', 
    'l':'pok','m':'njk', 'n':'bhjm','o':'iklp','p':'ol','q':'aw','r':'edft','s':'awedxz','t':'rfgy','u':'yhji','v':'cfgb','w':'qase',
    'x':'zsdc','y':'tghu','z':'asx'
}

def keyboard_distance(c1, c2):
    if c1==c2:
        return 0
    elif c2 in KEYBOARD.get(c1):
        return 1
    return 2

def edit_types(typed, candidate):
    lt, lc=len(typed), len(candidate) 

    if lt==lc:
        diff=[(t,c) for t,c in zip(typed, candidate) if t!=c]
        if len(diff)==2:
            (a,b), (c,d)=diff
            if a==d and b==c:
                return 'transpose'
        return 'replace'   
    if lt==lc+1:
        return 'delete'  
    if lt==lc-1:
        return 'insert'
    return 'unknown'

def channel_prob(typed, candidate):
    if typed==candidate:
        return 1.0
    edit_type=edit_types(typed, candidate)
    if edit_type=='transpose':
        return 0.8
    elif edit_type=='replace':
        diffs=[(t,c) for t,c in zip(typed, candidate) if t!=c]
        t_char, c_char=diffs[0]
        dist=keyboard_distance(t_char, c_char)
        return 0.6 if dist==1 else 0.2
    elif edit_type=='insert':
        return 0.4
    elif edit_type=='delete':
        return 0.3
    return 0.1


def correction(word):
    return max(candidates(word), key=lambda x: prob(x)*channel_prob(word, x))

def correction_bigram(prev_word, cur_word):
    return max(candidates(cur_word), key=lambda x: prob_bigram(prev_word,x)*channel_prob(cur_word, x))


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

