import nltk
import json

#create arrays
data = []
reviewID = []
productID = []
top10Reviewer = []
top10Product = []

#load json file into data array
for line in open('CellPhoneReview.json', 'r'):
    data.append(json.loads(line))

#load all reviewer id into reviewID array
for a in data:
	reviewID.append(a['reviewerID'])

#load all product id into productID array
for b in data:
	productID.append(b['asin'])

#Calculate frequency distribution
reviewerFreq = nltk.FreqDist(reviewID)
print("Top 10 Reviewer: ")
print(reviewerFreq.most_common(10))

#Calculate frequency distribution
productFreq = nltk.FreqDist(productID)
print("Top 10 Products: ")
print(productFreq.most_common(10))