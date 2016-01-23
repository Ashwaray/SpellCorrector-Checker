import re, collections
import esSearch

def words(text): return re.findall('[a-z]+', text.lower()) 

def train(features):
    model = collections.defaultdict(lambda: 1)
    for f in features:
        model[f] += 1
    return model

#NWORDS = train(words(file('ispell.txt').read()))
#NWORDS = ''#train(words(esSearch.search("roposo")))
alphabet = 'abcdefghijklmnopqrstuvwxyz'

def edits1(word, NWORDS):
   splits     = [(word[:i], word[i:]) for i in range(len(word) + 1)]
   deletes    = [a + b[1:] for a, b in splits if b]
   transposes = [a + b[1] + b[0] + b[2:] for a, b in splits if len(b)>1]
   replaces   = [a + c + b[1:] for a, b in splits for c in alphabet if b]
   inserts    = [a + c + b     for a, b in splits for c in alphabet]
   return set(deletes + transposes + replaces + inserts)

def known_edits2(word, NWORDS):
    return set(e2 for e1 in edits1(word, NWORDS) for e2 in edits1(e1, NWORDS) if e2 in NWORDS)

def known(words, NWORDS): return set(w for w in words if w in NWORDS)

def correct(word):
    NWORDS = train(words(esSearch.search(word)))
    #print 'NWORDS type = ',type(NWORDS)
    #print 'file read type = ',type(file('hashtags.txt').read())
    #print file('hashtags.txt').read()
    #print esSearch.search(word)
    print 'known(word) = ', known(word, NWORDS)
    print 'known1(word) = ', edits1(word, NWORDS)
    print 'known2(word) = ', known_edits2(word, NWORDS)
    candidates = known([word], NWORDS) or known(edits1(word, NWORDS), NWORDS) or known_edits2(word, NWORDS) or [word]
    #print 'max(candidates, key=NWORDS.get) = ', max(candidates, key=NWORDS.get)
    return max(candidates, key=NWORDS.get)
