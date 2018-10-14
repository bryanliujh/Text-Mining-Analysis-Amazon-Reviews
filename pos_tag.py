import json
import random
import nltk
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk import ne_chunk, pos_tag

#create arrays
data = []
review = []
sentences = []
posTag = []

#load json file into data array
for line in open('CellPhoneReview.json', 'r'):
    data.append(json.loads(line))

#load all review into review array
for a in data:
	review.append(a['reviewText'])

#load all sentences into sentences array
for b in review:
	for c in sent_tokenize(b):
		sentences.append(c)

#Perfrom POS Tagging on one sentence
def tagging(text):
	return nltk.chunk.ne_chunk(
		nltk.pos_tag(
			nltk.word_tokenize(text)))

#number of total sentences
size = len(sentences)-1

#print POS Tagging and draw tree for random 5 sentences
for x in range(5):
	sentence = sentences[random.randint(0,size)]
	print("\nSentence " + str(x+1) + ": " + sentence + "\n POS Tagging: ")
	tag = tagging(sentence)
	tag.pprint()
	tag.draw()
	posTag.append(tag)
