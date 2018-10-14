import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)
import numpy as np
import json
import nltk

from nltk.tokenize import TweetTokenizer #split review to tokens
from nltk.sentiment.vader import SentimentIntensityAnalyzer as SIA
from nltk.stem import WordNetLemmatizer #reduce words to same form
nltk.download('punkt')
nltk.download('vader_lexicon')

#read and store data
data_json = []
print('reading json file')
file_json = open('CellPhoneReview.json','r')
for each_data in file_json:
    data_json.append(json.loads(each_data))
file_json.close()

#no. of row
print('no. of rows %d'%len(data_json))

#split into positive & negative sentiment review
#pos -> rating >= 4
#neg -> rating <=2
print('splitting data into pos and neg review dataset')
pos_reviews = list(filter(lambda x: x["overall"]>=4,data_json))
neg_reviews = list(filter(lambda x: x["overall"]<=2,data_json))
print('no. of pos reviews %d'%len(pos_reviews))
print('no. of neg reviews %d'%len(neg_reviews))

#get freq of the word
def get_word_freq(wordlist):
    #remove words less than len 3
    wordlist = list(filter(lambda x: len(x)>=3, wordlist))

    #convert all to lower case
    wordlist = [x.lower() for x in wordlist]

    #lemmatize
    lemma = WordNetLemmatizer()
    wordlist = list(map(lambda x: lemma.lemmatize(x,'a'), wordlist))

    wordlist = nltk.FreqDist(wordlist)
    #print words
    rank = 1
    for i in wordlist.most_common(20):
        print('rank {}, {}'.format(rank, i[0]))
        rank += 1

def get_pos_word(tokenize_reviews):
    jj_word = []
    sid = SIA()
    for review in tokenize_reviews:
        words = nltk.pos_tag(review)
        for word in words:
            if word[1] == 'JJ':  #adj tag
                ss = sid.polarity_scores(word[0])
                if ss["pos"] >= 0.5 and ss["compound"] >= 0.5:
                    jj_word.append(word[0])

    #print(jj_word)
    print('Freq positive words:')
    get_word_freq(jj_word)

def get_neg_word(tokenize_reviews):
    jj_word = []
    sid = SIA()
    for review in tokenize_reviews:
        words = nltk.pos_tag(review)
        for word in words:
            if word[1] == 'JJ': #adj tag
                ss = sid.polarity_scores(word[0])
                if ss["neg"] >= 0.5 and ss["compound"] <= -0.5:
                    jj_word.append(word[0])

    #print(jj_word)
    print('Freq negative words:')
    get_word_freq(jj_word)


def main():

    tt = TweetTokenizer()

    #get positive review
    tokenize_reviews = []
    for review in pos_reviews:
        tokenize_reviews.append(tt.tokenize(review["reviewText"]))
    get_pos_word(tokenize_reviews)

    print('')
    #get negative review
    tokenize_reviews = []
    for review in neg_reviews:
        tokenize_reviews.append(tt.tokenize(review["reviewText"]))
    get_neg_word(tokenize_reviews)

if __name__ == '__main__':
    main()
