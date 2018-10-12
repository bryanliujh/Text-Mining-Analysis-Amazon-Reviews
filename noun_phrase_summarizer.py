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


    find_top_3_popular_product(data)
    find_top_20_noun_phrase(filename_noun_phrase)
    random_sample_5reviews(data)
    reviews_chosen()


def extract_noun_phrases(sentence, noun_dict):
    list_of_noun_phrases = nlp(sentence).noun_chunks
    for noun_phrase in list_of_noun_phrases:
        # remove stopwords and punctuations
        if len(noun_phrase.text) > 1:
            if noun_phrase.text in noun_dict:
                noun_dict[noun_phrase.text] = noun_dict[noun_phrase.text] + 1
            else:
                noun_dict[noun_phrase.text] = 1

    return noun_dict



def find_top_3_popular_product(data):
    count = Counter(data_item['asin'] for data_item in data)
    outputStr = ""
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
        outputStr = outputStr + "\n" + json.dumps(top10pairs)
    outputStr = "===========================Summarise 3 popular product reviews by its representative noun phrase==========================================" +  outputStr
    print(outputStr)


def find_top_20_noun_phrase(filename_noun_phrase):
    with open(filename_noun_phrase, 'r') as file:
        data = json.load(file)
        first20pairs = {k: data[k] for k in list(data)[:20]}
        print("\n============================Top 20 most frequent noun phrases used by reviewers=====================================")
        print("Top 20 noun phrase: " + json.dumps(first20pairs))

        file.close()


def random_sample_5reviews(data):
    print("\n==============================Randomly sample 5 reviews and evaluate the effectiveness of the noun phrase detector in terms of Precision and Recall================================")

    for i in range(0,5):
        rand_item = random.choice(data)
        sentence_raw = rand_item['reviewText'].lower()
        noun_phrase_arr = []

        print("\nReview: ")
        print(sentence_raw)

        doc = nlp(sentence_raw)

        print("Noun Phrase: ")
        for noun_phrase in doc.noun_chunks:
            if noun_phrase.text not in stops:
                noun_phrase_arr.append(noun_phrase.text)
        print(noun_phrase_arr)


def reviews_chosen():
    print("\n==============================Reviews chosen for evaluation of effectiveness of the noun phrase detector in terms of Precision and Recall================================\n")

    myTestArr = ["I had my doubts, but the product lived up to the description. It's matte and no more oily fingerprints! I will definitely buy more.",
                 "I bought it as a gift and im really enjoying it not much for big drop protection but its done a good job so far.",
                 "this case is a great case.  my husband drops his phone all the time, this case protects the phone very well.",
                 "i like this case very much. covers my phone and keeps the front from being scratched when placed down. great protection!",
                 "the motorola duel port charger works as advertised. very pleased with charger for multiple uses, smart phone razor maxx, kindle and other smart phones. does a excellent job of charging all items quickly."]
    for sent in myTestArr:

        noun_phrase_arr = []

        print("\nReview: ")
        print(sent.lower())

        doc = nlp(sent.lower())
        print("Noun Phrase: ")
        for noun_phrase in doc.noun_chunks:
            if noun_phrase.text not in stops:
                noun_phrase_arr.append(noun_phrase.text)
        print(noun_phrase_arr)


def check_file_exist(filename):
    is_exists = os.path.isfile(filename)
    return is_exists


if __name__ == '__main__':
    load_json_file()

