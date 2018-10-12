import json
import nltk
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.stem import PorterStemmer
from collections import Counter
from nltk.tokenize import RegexpTokenizer
from nltk.corpus import stopwords

stop_words = stopwords.words('english')
lowerCaseStopWords=[]
for s in stop_words:
	lowerCaseStopWords.append(s.lower())


data = []
wordCountForEachReview =[]

for line in open('CellPhoneReview.json', 'r'):
    data.append(json.loads(line))
	
reviewText = []
	
for d in data:
	reviewText.append(d['reviewText'])

tokenizer = RegexpTokenizer(r'\w+')

stemReview=[]
ps = PorterStemmer()
for r in reviewText:
    stemReview.append(str(ps.stem(r)).lower())


for i in reviewText:
	wordCountForEachReview.append(str(len(word_tokenize(i))))
	
stemFreq = nltk.FreqDist(wordCountForEachReview)
print(stemFreq.most_common(len(wordCountForEachReview)))

reviewFreq = nltk.FreqDist(wordCountForEachReview)
#print(reviewFreq.most_common(len(wordCountForEachReview)))	## without stemming
	
#top 20 words before stemming
top20words=[]
top20wordsRank=[]

for r in reviewText:
	for c in tokenizer.tokenize(r): # for . use word_tokenize
		if str(c).lower() not in lowerCaseStopWords :
			top20words.append(c)

wordFreq = nltk.FreqDist(top20words)

for d in wordFreq.most_common(20):
    top20wordsRank.append(d)
	
#print(top20wordsRank) #top-20 most frequent words without stemming








