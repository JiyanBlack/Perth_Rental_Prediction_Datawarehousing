# -*- coding: utf-8 -*-
import nltk
import string
import re
from nltk.stem.porter import PorterStemmer


path = '../crawler/ksou/data/description/'
stemmer = PorterStemmer()
translator = str.maketrans('', '', string.punctuation)
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
    return stems
