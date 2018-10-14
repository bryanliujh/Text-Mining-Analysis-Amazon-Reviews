import sys
import pandas as pd
import negationExpressionDetector
import tokenizer
import nltk
print("nlp")
fileName = "CellPhoneReview.json"
colName = "reviewText"
if len(sys.argv) >1:
    fileName = sys.argv[1]
    if len(sys.argv)>2:
        colName = sys.argv[2]
df = pd.read_json(fileName, lines=True)

#for faster debugging
#df = df.head(1000)

print("read json")
df['tokenized_'+ colName] = df[colName].apply(tokenizer.tokenize)
print("review text tokenized")

#top10product = df.groupby(['asin']).size().to_frame('size').reset_index().sort_values(['size'], ascending=[False]).head(10)
#print(top10product)


#testing purpose
#note: (no. 947) detect not well due to wrong tag (word 'so' is tagged as noun)
#sentence = "I LIKED THE CASE VERY MUCH = BUT I NO LONGER HAVE THE PHONE = SO THE NEW BUYER THAT BOUGHT IT FROM ME AND THE CASE."
#sentence = "I am disappointed that the 1A didn't work with my iPad.  That's what I get for buying a cheap adapter"
#tokens = nltk.word_tokenize(sentence)
#print(nltk.pos_tag(tokens))
#result = negationExpressionDetector.detectNegation(tokens)
#print(result)

df["negation"]=df['tokenized_'+ colName].apply(negationExpressionDetector.detectNegation)
print("negation found")
#check = df[['negation', 'tokenized_'+ colName]]
finalDetectedNegationExpression = df[['negation', colName]]
print(finalDetectedNegationExpression.head(200))
finalDetectedNegationExpression.to_csv("result.csv")
