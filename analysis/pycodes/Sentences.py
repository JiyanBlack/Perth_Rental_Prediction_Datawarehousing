# -*- coding: utf-8 -*-
import os
from nltk.stem.wordnet import WordNetLemmatizer
from nltk.stem.porter import PorterStemmer
import re
import string


class Normalizer():
    def __init__(self, useLemmatizer):
        if useLemmatizer:
            self.stem = WordNetLemmatizer().lemmatize
        else:
            self.stem = PorterStemmer().stem


class MySentences():
    counter = 0
    limit = None
    re_number = re.compile(r'\d')
    re_splitter = re.compile(r'\n')
    translator = str.maketrans('', '', string.punctuation)

    def __init__(self, dirname, useLemmatizer, limit = None):
        self.dirname = dirname
        self.norm = Normalizer(useLemmatizer)
        self.limit = limit

    def has_number(self, string):
        return self.re_number.search(string) != None
        
    def __iter__(self):
        for file in os.listdir(self.dirname):
            with open(os.path.join(self.dirname, file), 'rb') as f:
                text = f.read().decode('utf-8').translate(self.translator)
                texts = self.re_splitter.split(text)
                if len(texts) < 3:
                    continue
                self.counter += 1
                if self.limit and self.counter >= self.limit:
                    return
                for sent in texts:
                    result = [self.norm.stem(word) for word in sent.split() if not self.has_number(word)]
                    yield result

