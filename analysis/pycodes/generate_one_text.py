# -*- coding: utf-8 -*-
import os
import re
import string
import pickle
from nltk.stem import WordNetLemmatizer
from nltk.stem.porter import PorterStemmer
porter_stemmer = PorterStemmer()
articles = {}

Description_path = r'../../crawler/ksou/data/description/'
translator = str.maketrans('', '', string.punctuation)
re_number = re.compile(r'\d')
re_splitter = re.compile(r'\.|\n')
counter = 0
lemmar = WordNetLemmatizer()
def has_number(string):
    return re_number.search(string) != None

for file in os.listdir(Description_path):
    with open(Description_path+file, 'rb') as f:
        cur_desc = []
        text = f.read().decode('utf-8').lower()
        if len(text) < 10:
            continue
        sents = re_splitter.split(text)
        for sent in sents:
            result_sent = sent.translate(translator)
            words = [porter_stemmer.stem(word) for word in result_sent.split() if not has_number(word)]
            if len(words) > 0:
                cur_desc.append(words)
        file_id = file.split('.')[0]
        counter += 1
#        print(counter)
        articles.append(cur_desc)
#        print(articles[file_id])

with open('../result/description_data_arr_porterStem', 'wb') as f:
    pickle.dump(articles, f)