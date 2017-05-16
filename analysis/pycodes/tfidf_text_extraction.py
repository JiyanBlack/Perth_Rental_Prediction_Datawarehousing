# -*- coding: utf-8 -*-
import nltk
import string
import os
import re
from sklearn.feature_extraction.text import TfidfVectorizer
from nltk.stem.porter import PorterStemmer


path = '../crawler/ksou/data/description/'
token_dict = {}
stemmer = PorterStemmer()
translator = str.maketrans('', '', string.punctuation)
count = 0
LIMIT = 100
re_number = re.compile(r'\d')

def has_number(string):
    return re_number.search(string) != None

def stem_tokens(tokens, stemmer):
    stemmed = []
    for item in tokens:
        stemmed.append(stemmer.stem(item))
    return stemmed

def tokenize(text):
    tokens = nltk.word_tokenize(text)
    stems = stem_tokens(tokens, stemmer)
    stems = [s for s in stems if not has_number(s)]
#    print(stems)
    return stems

def main():
    global count
    for file in os.listdir(path):
        with open(path+file, 'rb') as f:
            text = f.read().decode('utf-8')
    #        print(text)
            if len(text) > 10:
                token_dict[file] = text.translate(translator)
                count += 1
                if count >= LIMIT:
                    break
    
    #this can take some time
    print('Finish collecting the doc... training using tfidf')
    tfidf = TfidfVectorizer(tokenizer=tokenize, stop_words='english', lowercase=True)
    tfs = tfidf.fit_transform(token_dict.values())
    dense = tfs.todense()
    feature_names = tfidf.get_feature_names()
    print(feature_names)

main()
