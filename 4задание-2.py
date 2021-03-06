# -*- coding: utf-8 -*-
"""4задание.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1a7zju4EQx0UjdFJifpkjbHziWiKPjhWO
"""

from google.colab import drive
drive.mount('gdrive')

input_path = 'gdrive/My Drive/4курс/Инфопоиск/result/'
input_tokens_path = 'gdrive/My Drive/4курс/Инфопоиск/result/tokens.txt'
output_tokens_path = 'gdrive/My Drive/4курс/Инфопоиск/result/tokens_td-idf.txt'
input_lemmas_path = 'gdrive/My Drive/4курс/Инфопоиск/result/lemmas.txt'
output_lemmas_path = 'gdrive/My Drive/4курс/Инфопоиск/result/lemmas_td-idf.txt'

from enum import unique
from itertools import chain
import re
import nltk
from nltk.corpus import stopwords

nltk.download('stopwords')
sw_nltk = stopwords.words('english')
import numpy as np

N = 142

def get_words_from_file(input):

    # with open(input) as source, open(output, 'w') as destination:
    with open(input) as source:
        #get the text from file
        text = source.read()
        #lower the text
        text = text.lower()
        #split words in text
        words = text.split()
        #get words without number
        words = [re.sub(r'\d', '', word) for word in words]
        words = [re.sub(r'amott/', '', word) for word in words]
        words = [re.sub(r'\b\w{1,2}\b', '', word) for word in words]
        words = [word.replace("'", '') for word in words]
        #reduce stopwords .,!;()[]-:"/\|$@^''&*%?
        words = [word.strip('.,!;()[]-:"/\|$@^''&*%?') for word in words]
        #reduce stopwords
        words = [word for word in words if word not in sw_nltk]
    return words

def get_tokens_from_multiple_files(input1, input2):

    with open(input2) as source2:
        #get the text from file
        text = source2.read()
        #lower the text
        text = text.lower()
        #split words in text
        tokens = text.split()

    count_tokens_tf_all_files = []

    for i in range(N):

        words = get_words_from_file(input_path + 'выкачка' + str(i + 1) + '.txt')


        count_tokens_tf = []

        #count the number of i token in every document
        for token in tokens:
            count = 0
            for word in words:
                if word == token:
                    count += 1
            count_tokens_tf.append(count/len(words))

        count_tokens_tf_all_files.append(count_tokens_tf)

    #create array for df value and sum all i array values to find occurence of word in N documents
    count_word_df_all_files = []

    for i in range(len(tokens)):
        count_loc = 0

        for j in range(len(count_tokens_tf_all_files)):
            if count_tokens_tf_all_files[j][i] != 0:
                count_loc += 1

        count_word_df_all_files.append(count_loc)
    
    #find idf(t) as log(N/(df + 1))
    count_tokens_idf_all_files = [np.log(N / (count_word_df_all_files[i] + 1)) for i in range(len(count_word_df_all_files))]

    #transpose cause tf matrix is 2326 x 142, but idf is 142 x 1
    new_tf_np = np.transpose(np.array(count_tokens_tf_all_files))

    #find td-idf(t,d) as tf(d,t) * log(N/(df + 1))
    count_tokens_tf_idf_all_files = [new_tf_np[i] * count_tokens_idf_all_files[i] for i in range(len(count_tokens_idf_all_files))]

    return count_tokens_tf_all_files, count_word_df_all_files, count_tokens_idf_all_files, count_tokens_tf_idf_all_files, tokens  


def write_tokens_to_file(output, tokens, idf, tf_idf):
    for i in range(N):
        with open(output + 'td-idf' + str(i + 1) + '.txt', 'w') as destination:
            for j in range(len(tokens)):
                destination.write(tokens[j] + ' ' + str(idf[j]) + ' ' + str(tf_idf[j][i]) + '\n')

res = get_tokens_from_multiple_files(input_path, input_tokens_path)
tf = res[0]
df = res[1]
idf = res[2]
tf_idf = res[3]
tokens = res[4]

write_tokens_to_file(input_path, tokens, idf, tf_idf)