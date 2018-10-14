import re

#complete negation word: no, not, never, none, nobody, nothing
def detectCompleteNegationWord(word):
    return re.search("^n(o+((t(hing)?|ne|body)?)|(ever))+$", word, re.I)

#detect short form of negation: n't
def detectShortFormNegationWord(word):
    return re.search("n't", word)