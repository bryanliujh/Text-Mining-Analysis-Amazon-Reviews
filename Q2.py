import json
import random
import nltk
from nltk.tokenize import sent_tokenize

#create arrays
data = []
reviews = []
sentences = []

#load json file into data array
for line in open('CellPhoneReview.json', 'r'):
    data.append(json.loads(line))

#load all review into reviews array
for a in data:
	reviews.append(a['reviewText'])

#count the number of sentence in one review and load into sentences array
for b in reviews:
	sentences.append(str(len(sent_tokenize(b))))

#Calculate frequency distribution
reviewFreq = nltk.FreqDist(sentences)
 print(reviewFreq)
 print(reviewFreq.most_common(143))
 reviewFreq.plot()

#number of total review
size = len(reviews)-1

#print sentence segmentation for random 5 review
for c in range(5):
	count = 1
	review = reviews[random.randint(0,size)]
	print("\nReview " + str(c+1) + ":")
	sents = sent_tokenize(review)
	for d in sents:
		print("Sentence " + str(count) + ": " + d)
		count+=1

