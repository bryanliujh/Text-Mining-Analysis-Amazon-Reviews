import nltk
import string

exclude = set(string.punctuation)
exclude.remove("'")
exclude.remove(".")
exclude.remove(",")
exclude.remove("?")
exclude.remove("!")

def tokenize(sentence):
    #considering cases where no space between words in front and behind of comma and fullstop
    sentence = sentence.replace(".", ". ")
    sentence = sentence.replace(",", ", ")
    #remove the punctuation by replacing it with null, except "' ,."
    sentence = "".join(cha for cha in list(sentence) if cha not in exclude)
    return nltk.word_tokenize(sentence)