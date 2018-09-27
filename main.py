import nltk
from nltk.corpus import stopwords
import json
import en_core_web_sm
from tqdm import tqdm
import multiprocessing
from collections import Counter
import os

noun_phrase_dict = {}

def load_json_file():
    data = []
    noun_phrase_no_stop = {}
    stops = set(stopwords.words("english"))
    nlp = en_core_web_sm.load()
    filename_noun_phrase = 'noun_phrase_text.txt'
    #nltk.download('punkt')
    #python -m nltk.downloader stopwords
    #to use cell phone review for deployment, use sample review for testing
    filename = 'CellPhoneReview.json'
    #filename = 'SampleReview.json'
    with open(filename) as file:
        for line in file:
            data.append(json.loads(line))


    find_top_3_popular_product(data)

    exists = os.path.isfile(filename_noun_phrase)
    if not exists:
        #using multiprocessor to increase the speed of parsing
        #parsing of large corpus could take up to 2 hours!!
        pool = multiprocessing.Pool(processes=multiprocessing.cpu_count()-1)
        for data_item in tqdm(data):
            pool.apply_async(extract_noun_phrases(data_item['reviewText'].lower(), noun_phrase_dict, nlp), args=[data_item])
        pool.close()
        pool.join()

        sorted_by_value = sorted(noun_phrase_dict.items(), reverse=True, key=lambda kv: kv[1])

        #write all the extracted noun phrase into this file, only store meaningful noun phrase (not stop words)
        #check if this file exist in the beginning, if exist do not do parsing
        with open(filename_noun_phrase, 'w+') as file:
            for k in tqdm(sorted_by_value):
                if k[0] not in stops:
                    noun_phrase_no_stop[k[0]] = k[1]
            json.dump(noun_phrase_no_stop, file)
            file.close()

    print('hello')


def extract_noun_phrases(sentence, noun_phrase_dict, nlp):
    list_of_noun_phrases = nlp(sentence).noun_chunks
    for noun_phrase in list_of_noun_phrases:
        # remove stopwords and punctuations
        #if all(token.is_stop != True and token.is_punct != True and '-PRON-' not in token.lemma_ for token in noun_phrase) == True:
        if len(noun_phrase.text) > 1:
            if noun_phrase.text in noun_phrase_dict:
                noun_phrase_dict[noun_phrase.text] = noun_phrase_dict[noun_phrase.text] + 1
            else:
                noun_phrase_dict[noun_phrase.text] = 1


def find_top_3_popular_product(data):
    count = Counter(data_item['asin'] for data_item in data)
    print(count)


def find_top_20_noun_phrase():
    print("hi")



if __name__ == '__main__':
    load_json_file()
