# -*- coding: utf-8 -*-
import word2vec
import pandas
import numpy
import re
#lemma = word2vec.read_model('description_lemmatized.word2vec')
porter = word2vec.read_model('description_porterStem.word2vec')
#nostem = word2vec.read_model('description_nostem.word2vec')
keywords_map = {
       'pool': [],
       'secure': [],
       'furnished': [],
       'yard': ['yard','garden','courtyard','backyard'],
       'ac': [],
        }

def get_most_weight(word, target):
    return porter.similarity(word, target)

def get_weight_arr(docum):
    words = 
        


    
dic = {'id': ,
       'pool': ,
       'secure': ,
       'furnished': ,
       'yard': ,
       }
