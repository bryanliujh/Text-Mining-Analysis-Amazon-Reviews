import nltk
import json
import en_core_web_sm
from tqdm import tqdm
import multiprocessing
from collections import Counter

noun_phrase_dict = {}

def load_json_file():
    data = []
    nlp = en_core_web_sm.load()
    #nltk.download('punkt')
    #python -m nltk.downloader stopwords
    #to use cell phone review for deployment, use sample review for testing
    filename = 'CellPhoneReview.json'
    #filename = 'SampleReview.json'
    with open(filename) as file:
        for line in file:
            data.append(json.loads(line))


    find_top_3_popular_product(data)

    print(multiprocessing.cpu_count())
    #using multiprocessor to increase the speed of parsing
    #parsing of large corpus could take up to 2 hours!!
    pool = multiprocessing.Pool(processes=multiprocessing.cpu_count()-1)
    for data_item in tqdm(data):
        pool.apply_async(extract_noun_phrases(data_item['reviewText'].lower(), noun_phrase_dict, nlp), args=[data_item])
    pool.close()
    pool.join()

    #write all the extracted noun phrase into this file
    #check if this file exist in the beginning, if exist do not do parsing
    with open('noun_phrase_text.txt', 'w+') as file:
        for np in noun_phrase_dict:
            file.write(np)
        file.close()

    print('hello')


def extract_noun_phrases(sentence, noun_phrase_dict, nlp):
    list_of_noun_phrases = nlp(sentence).noun_chunks
    for noun_phrase in list_of_noun_phrases:
        # remove stopwords and punctuations
        if len(noun_phrase.text) > 1:
            if noun_phrase.text in noun_phrase_dict:
                noun_phrase_dict[noun_phrase.text] = noun_phrase_dict[noun_phrase.text] + 1
            else:
                noun_phrase_dict[noun_phrase.text] = 1


def find_top_3_popular_product(data):
    count = Counter(data_item['asin'] for data_item in data)
    print(count)



if __name__ == '__main__':
    load_json_file()
