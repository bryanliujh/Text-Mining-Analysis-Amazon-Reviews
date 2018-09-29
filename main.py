from nltk import Tree
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
    process_filename_noun_phrase = 'process_noun_phrase_text.txt'

    #nltk.download('punkt')
    #python -m nltk.downloader stopwords
    #to use cell phone review for deployment, use sample review for testing
    filename = 'CellPhoneReview.json'
    #filename = 'SampleReview.json'
    with open(filename) as file:
        for line in file:
            data.append(json.loads(line))


    if not check_file_exist(filename_noun_phrase):
        #using multiprocessor to increase the speed of parsing
        #parsing of large corpus could take up to 2 hours!!
        pool = multiprocessing.Pool(processes=multiprocessing.cpu_count()-1)
        for data_item in tqdm(data):
            #sentence_arr = clean_sentence(data_item['reviewText'])
            #for sentence in sentence_arr:
            pool.apply_async(extract_noun_phrases(data_item['reviewText'].lower(), noun_phrase_dict), args=[data_item])
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

    #check if processed noun phrase file exist
    #if not check_file_exist(process_filename_noun_phrase):
    #   clean_sentence(filename_noun_phrase, process_filename_noun_phrase)

    find_top_3_popular_product(data)
    find_top_20_noun_phrase(filename_noun_phrase)
    random_sample_5reviews(data)


def extract_noun_phrases(sentence, noun_dict):
    list_of_noun_phrases = nlp(sentence).noun_chunks
    for noun_phrase in list_of_noun_phrases:
        # remove stopwords and punctuations
        #if all(token.is_stop != True and token.is_punct != True and '-PRON-' not in token.lemma_ for token in noun_phrase) == True:
        if len(noun_phrase.text) > 1:
            if noun_phrase.text in noun_dict:
                noun_dict[noun_phrase.text] = noun_dict[noun_phrase.text] + 1
            else:
                noun_dict[noun_phrase.text] = 1

    return noun_dict

'''
def clean_sentence(filename_noun_phrase, process_filename_noun_phrase):
    process_dict = {}
    #set to break sentences into sentence, break sentence into words, remove stopwords
    with open(filename_noun_phrase, 'r') as file:
        data = json.load(file)
        for i in tqdm(data):
            if i in process_dict:
                process_dict[i] = process_dict[i] + data[i]
            else:
                words = nltk.word_tokenize(i)
                w_list = []
                for w in words:
                    if w not in stops:
                        w_list.append(w)
                process_word = ' '.join(w_list)
                if process_word in process_dict:
                    process_dict[process_word] = process_dict[process_word] + data[i]
                else:
                    process_dict[process_word] = data[i]
        file.close()

    with open(process_filename_noun_phrase, 'w+') as file:
        process_list = sorted(process_dict.items(), reverse=True, key=lambda kv: kv[1])
        process_dict = {}
        for k in tqdm(process_list):
            process_dict[k[0]] = k[1]
        json.dump(process_dict, file)
        file.close()
'''

def find_top_3_popular_product(data):
    count = Counter(data_item['asin'] for data_item in data)
    for letter, count in count.most_common(3):
        pd_dict = {}
        top_pd_dict = {}
        for data_item in tqdm(data):
            if letter == data_item['asin']:
                pd_dict = extract_noun_phrases(data_item['reviewText'].lower(),pd_dict)
        top_pd_list = sorted(pd_dict.items(), reverse=True, key=lambda kv: kv[1])
        for item in top_pd_list:
            if item[0] not in stops:
                top_pd_dict[item[0]] = item[1]
        top10pairs = {letter: {k: top_pd_dict[k] for k in list(top_pd_dict)[:10]}}
        print(json.dumps(top10pairs))


def find_top_20_noun_phrase(filename_noun_phrase):
    with open(filename_noun_phrase, 'r') as file:
        data = json.load(file)
        first20pairs = {k: data[k] for k in list(data)[:20]}
        print("Top 20 noun phrase: " + json.dumps(first20pairs))

        file.close()


def random_sample_5reviews(data):
    for i in range(0,5):
        rand_item = random.choice(data)
        doc = nlp(rand_item['reviewText'])
        print(rand_item['reviewText'])
        print("Noun Phrase: ")
        print([noun_phrase.text for noun_phrase in doc.noun_chunks])
        #[to_nltk_tree(sent.root).pretty_print() for sent in doc.sents]



def check_file_exist(filename):
    is_exists = os.path.isfile(filename)
    return is_exists


def tok_format(tok):
    return "_".join([tok.orth_, tok.tag_])


def to_nltk_tree(node):
    if node.n_lefts + node.n_rights > 0:
        return Tree(tok_format(node), [to_nltk_tree(child) for child in node.children])
    else:
        return tok_format(node)

if __name__ == '__main__':
    load_json_file()
