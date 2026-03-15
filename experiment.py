import re
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

    return set(deletes + inserts + transposes + replaces)  # set coz removes duplicates

def edits2(word):
    "All edits that are 2 edits away from the word 'word' "

    return (e2 for e1 in edits1(word) for e2 in edits1(e1))  # creates a generator - produces output on demand, not all at once

print(edits2("hello"))