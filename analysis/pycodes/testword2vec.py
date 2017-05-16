# -*- coding: utf-8 -*-
"""
Created on Mon May 15 20:48:38 2017

@author: anshi
"""

import word2vec

from nltk.stem import WordNetLemmatizer
from nltk.stem.porter import PorterStemmer
porterstemmer = PorterStemmer()
lemmmatizer = WordNetLemmatizer()



lemma = word2vec.read_model('description_lemmatized.word2vec')
porter = word2vec.read_model('description_porterStem.word2vec')
nostem = word2vec.read_model('description_nostem.word2vec')


keyword = 'ac'
top_number = 15

print('Words relating to:', keyword)
print('lemmatized model:')
positive = ['ac','airconditioning', 'aircond', 'acon', 'airconditioner', 'aircondioning', 'cooling' ]
negative = ['vacuuming','vac','vacuum']
print(lemma.most_similar(positive= positive, negative = negative, topn=top_number))
print('stemmed model:')
print(porter.most_similar(porterstemmer.stem(keyword), topn=top_number))
print('original model:')
print(nostem.most_similar(keyword, topn=top_number))
