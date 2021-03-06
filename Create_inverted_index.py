from __future__ import unicode_literals
import pandas as pd
from bs4 import BeautifulSoup as bs
from hazm import *
import time
from Generate_stop_words import *

stop_words = collect_stop_words()
which_csv = {}
docs = ['ir-news-0-2.csv']


def merge_docs():
    # docs = ['ir-news-0-2.csv']
    all_content = []
    all_title = []
    counter = 0
    for doc in docs:
        df = pd.read_csv(doc, delimiter=',')
        which_csv[doc] = {'start': counter, 'end': counter + len(df['content']) - 1}
        for i in range(len(df['content'])):
            all_content.append(df['content'][i])
            all_title.append(df['title'][i])
        counter = len(df['content'])
    dict = {'which_csv': which_csv, 'all_docs': all_content, 'all_title': all_title}
    return dict


inverted_index = {}
contents = merge_docs()['all_docs']

all_content = []


def extract_inverted_index():
    start_time = time.time()
    lemmatizer = Lemmatizer()
    print(merge_docs()['which_csv'])
    for i in range(len(contents)):
        each_content = []
        soup = bs(contents[i])
        text = soup.get_text()
        # parsing the text
        lines = text.splitlines()
        parag = []
        parag.append([i])
        for line in lines:
            # check if line has ':', if it doesn't, move to the next line
            if line.find(':') == -1:
                continue
            # Normalize each line
            normalizer = Normalizer()
            line = normalizer.normalize(line)
            for j in range(len(stop_words)):
                if stop_words[j] in line:
                    line = line.replace(stop_words[j], ' ')
                if '  ' in line:
                    line = line.replace('  ', ' ')
            for term in line.split(' '):
                flag = 0
                if '#' in lemmatizer.lemmatize(term) and lemmatizer.lemmatize(term).split('#')[
                    1] in inverted_index and i not in inverted_index[lemmatizer.lemmatize(term).split('#')[1]][
                    'doc']:
                    inverted_index[lemmatizer.lemmatize(term).split('#')[1]]['freq'] += 1
                    inverted_index[lemmatizer.lemmatize(term).split('#')[1]]['doc'].append(i)
                    each_content.append(lemmatizer.lemmatize(term).split('#')[1])
                    flag = 1
                    # print('iterative verb : ' + str(lemmatizer.lemmatize(term).split('#')[1]) + str(inverted_index[lemmatizer.lemmatize(term).split('#')[1]]))
                # elif '#' in lemmatizer.lemmatize(term) and lemmatizer.lemmatize(term).split('#')[
                #     1] in inverted_index and i in inverted_index[lemmatizer.lemmatize(term).split('#')[1]][
                #     'doc']:
                #     each_content.append(lemmatizer.lemmatize(term).split('#')[1])
                #     # inverted_index[lemmatizer.lemmatize(term).split('#')[1]]['freq'] += 1
                #     # inverted_index[lemmatizer.lemmatize(term).split('#')[1]]['doc'].append(i)
                #     # for k in range(len(inverted_index[lemmatizer.lemmatize(term).split('#')[1]]['repetition'])):
                #     # if inverted_index[lemmatizer.lemmatize(term).split('#')[1]]['repetition'][-1][0] == i:
                #     #     print('it is ! ')
                #     # inverted_index[lemmatizer.lemmatize(term).split('#')[1]]['repetition'][-1][1] += 1
                #     # each_content.append(lemmatizer.lemmatize(term).split('#')[1])
                #     flag = 1
                #     # print('iterative verb : ' + str(lemmatizer.lemmatize(term).split('#')[1]) + str(inverted_index[lemmatizer.lemmatize(term).split('#')[1]]))
                elif term in inverted_index and i not in inverted_index[term]['doc']:
                    inverted_index[term]['freq'] += 1
                    inverted_index[term]['doc'].append(i)
                    each_content.append(term)
                    flag = 1
                # elif term in inverted_index and i in inverted_index[term]['doc']:
                #     # inverted_index[term]['freq'] += 1
                #     # inverted_index[term]['doc'].append(i)
                #     # inverted_index[term]['repetition'] = [[i, 1]]
                #
                #     # for k in range(len(inverted_index[term]['repetition'])):
                #     # if inverted_index[term]['repetition'][-1][0] == i:
                #     #     print('oops yes ! ')
                #     # inverted_index[term]['repetition'][-1][1] += 1
                #     # each_content.append(term)
                #     flag = 1
                    # print('iterative noun : ' + str(term) + str(inverted_index[lemmatizer.lemmatize(term).split('#')[1]]))
                    # print('iterative noun : ' + str(term) + str(inverted_index[lemmatizer.lemmatize(term).split('#')[1]]))
                if flag == 0:
                    if '#' in lemmatizer.lemmatize(term) and lemmatizer.lemmatize(term) not in inverted_index:
                        inverted_index[lemmatizer.lemmatize(term).split('#')[1]] = {'freq': 1, 'doc': [i]}
                        # print('new verb : ' + str(lemmatizer.lemmatize(term).split('#')[1]) + str(inverted_index[lemmatizer.lemmatize(term).split('#')[1]]))
                        each_content.append(lemmatizer.lemmatize(term).split('#')[1])
                    elif term != '' and term not in inverted_index:
                        inverted_index[term] = {'freq': 1, 'doc': [i]}
                        each_content.append(term)
                        # print('new noun : ' + str(term) + str(inverted_index[term]))
        all_content.append(each_content)
        # print(inverted_index)
    print("--- %s seconds ---" % (time.time() - start_time))
    return all_content, inverted_index
