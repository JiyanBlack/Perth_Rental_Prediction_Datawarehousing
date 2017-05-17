# -*- coding: utf-8 -*-
import word2vec
import pandas

import re
#lemma = word2vec.read_model('description_lemmatized.word2vec')
dic = word2vec.read_pickle('description_porterStem.dict')
#print(description_dic_porter)
#nostem = word2vec.read_model('description_nostem.word2vec')
keywords_map = {
       'pool': ['pool', 'poolspa'],
       'furnished': ['furnish', 'refurbish','refurbish','renov'],
       'yard': ['yard','garden','courtyard','backyard'],
       'ac': ['ac', 'aricon','aircondit','aircond','aircondition','acon','acond','acondit'],
        }

re_map = None
CSV_PATH = "../../data/csv/"

def convert_keywords_map(keywords_map):
    result = {}
    for key in keywords_map:
        str_arr = keywords_map[key]
        re_result = r'|'.join(str_arr)
        re_result = r'\b(' + re_result + r')\b'
        result[key] = re.compile(re_result)
    return result

def is_exsit(docstr, attribute):
    global re_map
    if re_map[attribute].search(docstr):
        return 1
    return 0

def get_result_for_one_doc_weight(doc,docid,finaldic):
    sents = [' '.join(sent) for sent in doc]
    docstr = ' '.join(sents)
    finaldic['id'].append(docid)
    finaldic['pool'].append(is_exsit(docstr, 'pool'))
    finaldic['furnished'].append(is_exsit(docstr, 'furnished'))
    finaldic['yard'].append(is_exsit(docstr, 'yard'))
    finaldic['ac'].append(is_exsit(docstr, 'ac'))
#    print(finaldic)

    
def extract_info_from_text():
#    extract house detail information from description
    global re_map
    finaldic = {
            'id':[],
            'pool':[],
            'furnished':[],
            'yard':[],
            'ac':[],
            }
    re_map = convert_keywords_map(keywords_map)
    for docid in dic:
        get_result_for_one_doc_weight(dic[docid],docid,finaldic)
    df = pandas.DataFrame(finaldic, columns = ['id','pool','furnished','yard','ac'])
    df.to_csv('../result/house_attr.csv', index = False)
    return df


def combine_house_info():
    df_jsoninfo = pandas.read_csv(CSV_PATH + 'ksou_parsed_from_json.csv')
    df_desciptioninfo = pandas.read_csv(CSV_PATH + 'house_attr.csv')
    df_combined = df_jsoninfo.merge(df_desciptioninfo, on='id')
    df_combined.sort_values('id', inplace = True)
    df_combined.to_csv(CSV_PATH + 'ksou_47146x25.csv', index=False)

def split_lastSold_info():
    df = pandas.read_csv(CSV_PATH + 'ksou_47146x25.csv')
    print(df.shape)
    df_result = df.drop(['lastSoldPrice','lastSoldTimeYear','lastSoldTimeMonth'], axis = 1)
    print(df_result.shape)
    df = df[~pandas.isnull(df['lastSoldPrice'])]
    df = df[~pandas.isnull(df['lastSoldTimeYear'])]
    df = df[~pandas.isnull(df['lastSoldTimeMonth'])]
    df = df.drop(['soldPrice', 'soldTimeMonth', 'soldTimeYear'],axis = 1)
    df = df.rename(columns={'lastSoldPrice': 'soldPrice', 'lastSoldTimeMonth': 'soldTimeMonth', 'lastSoldTimeYear': 'soldTimeYear'})
    print(df.shape)
    df_result = df_result.append(df, ignore_index=True)
    print(df_result.shape)
    df_result.sort_values('id', inplace = True)
    df_result.to_csv(CSV_PATH + 'ksou_50095x22.csv', index = False)

def remove_rental_info():
    CSV_PATH = "../../data/csv/"
    DF_NAME = "ksou_50095x22.csv"
    df = pandas.read_csv(CSV_PATH + DF_NAME)
    df = df.drop(['rentPrice', 'rentTimeYear', 'rentTimeMonth'] , axis = 1)
    print(df.shape)
    df.to_csv(CSV_PATH + 'ksou_50095x19.csv', index = False)

if __name__ == "__main__":
    remove_rental_info()

    
#dic = {'id': ,
#       'pool': ,
#       'secure': ,
#       'furnished': ,
#       'yard': ,
#       }
