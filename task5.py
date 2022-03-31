import numpy as np
import re, string
import pymorphy2  
import webbrowser
import collections
from scipy import spatial
import PySimpleGUI as sg
import os.path
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

russian_pattern = re.compile('[а-я]')
# Функция очистки текста
def prepare_token(token):
    token = token.lower()
    if token in string.punctuation or not russian_pattern.match(token):
        return ''
    return ''.join([i for i in token if not i.isdigit()])\
    .lower().strip()

uniq_filtered_tokens = set()
stop_words = stopwords.words('russian')
analyzer = pymorphy2.MorphAnalyzer()

def to_lemmas(text):
    result = []
    tokens = word_tokenize(text)
    for token in tokens:
        preapared = prepare_token(token) 
        if preapared == '': continue
        if preapared in stop_words: continue
        normal_form = analyzer.parse(preapared)[0].normal_form
        result.append(normal_form)
    return result;

def get_idf():
    lemmas = set()
    file = open('lemmas_idf.txt', 'r')
    idf = dict()
    for line in file.readlines():
        lemma, _idf = line.replace('\n', '').split(' ')
        idf[lemma] = float(_idf)
    return idf

def get_lemmas_and_inverted_index():
    index_file = open('inverted_index.txt', 'r')
    index = dict()
    lemmas = []
    for line in index_file.readlines():
        line = line.replace('\n', '').split(' ')
        lemma_docs = []
        for i in line[1:]:
            lemma_docs.append(int(i))
        index[line[0]] = lemma_docs
        lemmas.append(line[0])
    return lemmas, index

def get_urls():
    urls = dict()
    file = open('index.txt')
    for line in file.readlines():
        split = line.split('\t')
        urls[int(split[0])] = split[1]
    return urls

def load_matrix():
    all_lemmas, index = get_lemmas_and_inverted_index()
    matrix = np.zeros((202, len(index)))
    
    for path in os.listdir('lemmas_tf_idf/'):
        if not path.endswith('txt'): continue
        lemmas, idf, tfidf =[], dict(), dict()
        doc_num = int(path.split('.')[0])
        
        for lemma_line in open('lemmas_tf_idf/' + path).readlines():
            split = lemma_line.replace('\n', '').split(' ')
            lemma = split[0]
            lemmas.append(lemma)
            idf[lemma] = float(split[1])
            tfidf[lemma] = float(split[2])
        
        for lemma in lemmas:
            matrix[doc_num - 1][all_lemmas.index(lemma)] = tfidf[lemma]
    return matrix

def get_search_result(query):
    search_lemmas = to_lemmas(query.lower())
    idf = get_idf()
    tf = collections.Counter(search_lemmas)
    vector = np.zeros(len(index))
    for lemma in index:
        if lemma in search_lemmas:
            vector[lemmas.index(lemma)] = (tf[lemma] / float(len(index[lemma]))) * idf[lemma]
            
    result = dict()
    for idx, row in enumerate(matrix):
        result[idx + 1] = 1 - spatial.distance.cosine(vector, row)

    result_sorted = dict(sorted(result.items(), key=lambda item: item[1], reverse=True))
    return result_sorted

lemmas, index = get_lemmas_and_inverted_index()
doc_num_url = get_urls()    
matrix = load_matrix()


storage = {'data':[]}

def click_search():
    search_input = window['-INPUT-'].get()
    docs = get_search_result(search_input)
    storage['data'] = [[i[0], doc_num_url[i[0]], i[1]] for i in docs.items()]
    window['-TABLE-'].update(storage['data'])
    
def click_open_url(num):
    url = storage['data'][num][1]
    print(url)
    webbrowser.open(url, new=2)
    
layout = [
    [sg.Text("Enter search phrase")], 
    [sg.Input(key='-INPUT-'), sg.Button("Search", key=click_search)],
    [sg.Table(values=[], headings=['Doc number','URL', 'Value'], auto_size_columns=False, col_widths=[10,40,10], key='-TABLE-', enable_events=True)]
]

window = sg.Window("Demo", layout)
while True:
    event, values = window.read()
    print(event)
    if callable(event):
        event()
    if event == '-TABLE-':
        click_open_url(values['-TABLE-'][0])
    if event == sg.WIN_CLOSED:
        break

window.close()