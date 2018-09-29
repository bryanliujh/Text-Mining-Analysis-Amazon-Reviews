import nltk
from nltk.corpus import stopwords
import json, os, random, string
import en_core_web_sm
from tqdm import tqdm
import multiprocessing
from collections import Counter
from nltk.stem import PorterStemmer

noun_phrase_dict = {}
nlp = en_core_web_sm.load()
ps = PorterStemmer()
stops = set(stopwords.words("english") + list(string.punctuation))

def load_json_file():
    data = []
    noun_phrase_no_stop = {}
    filename_noun_phrase = 'noun_phrase_text.txt'


    #nltk.download('punkt')
    #python -m nltk.downloader stopwords
    #to use cell phone review for deployment, use sample review for testing
    #filename = 'CellPhoneReview.json'
    filename = 'SampleReview.json'
    with open(filename) as file:
        for line in file:
            data.append(json.loads(line))

    exists = os.path.isfile(filename_noun_phrase)
    if not exists:
        #using multiprocessor to increase the speed of parsing
        #parsing of large corpus could take up to 2 hours!!
        pool = multiprocessing.Pool(processes=multiprocessing.cpu_count()-1)
        for data_item in tqdm(data):
            sentence_arr = clean_sentence(data_item['reviewText'])
            for sentence in sentence_arr:
                pool.apply_async(extract_noun_phrases(sentence, noun_phrase_dict, nlp), args=[data_item])
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

    find_top_3_popular_product(data)
    find_top_20_noun_phrase(filename_noun_phrase)


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


def clean_sentence(sentences):
    #set to lowercase, break sentences into sentence, break sentence into words, remove stopwords and stem words
    sentences = nltk.sent_tokenize(sentences.lower())
    sentence_arr = []

    for sentence in sentences:
        words = nltk.word_tokenize(sentence)
        w_list = []
        s = ''
        for w in words:
            if w not in stops:
                #w = ps.stem(w)
                w_list.append(w)
        s = ' '.join(w_list)
        sentence_arr.append(s)

    return sentence_arr



def find_top_3_popular_product(data):
    count = Counter(data_item['asin'] for data_item in data)
    print(count)


def find_top_20_noun_phrase(filename_noun_phrase):
    with open(filename_noun_phrase, 'r') as file:
        data = json.load(file)
        first20pairs = {k: data[k] for k in list(data)[:20]}
        print("Top 20 noun phrase: " + json.dumps(first20pairs))

        file.close()


def random_sample_5reviews(filename_noun_phrase):
    random_review_dict = {}
    with open(filename_noun_phrase, 'r') as file:
        data = json.load(file)
        for i in range(0,5):
            rand_key = random.choice(data)
            nlp(data[rand_key]).noun_chunks
        print("Top 20 noun p: " + json.dumps())

        file.close()


if __name__ == '__main__':
    load_json_file()
