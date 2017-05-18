# -*- coding: utf-8 -*-

import gensim
import pickle

RESULT_PATH = '../../../data/binary/'

class pickle_sentence():
    input_binary = ""
    def __init__(self, input_binary):
        self.input_binary = input_binary
    
    def __iter__(self):
        with open(self.input_binary,'rb') as f:
            arr = pickle.load(f)
            for article in arr:
                for sentence in article:
                    yield sentence

def produce_model(input_binary, output):
    model = gensim.models.Word2Vec(pickle_sentence(RESULT_PATH + input_binary), min_count=5, workers=4)
    model.save(RESULT_PATH + output)

def read_model(file_name):
    return gensim.models.Word2Vec.load(RESULT_PATH + file_name)

if __name__ == "__main__":
    pass
    produce_model('description_lemmatized.arr','description_lemmatized.word2vec')
    produce_model('description_porterStem.arr','description_porterStem.word2vec')