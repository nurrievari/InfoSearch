import os, pymorphy2

from bs4 import BeautifulSoup
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

# Функция очистки текста
def prepare_token(token):
    return ''.join([i for i in token if not i.isdigit()])\
    .replace('.', '').replace('_', '')\
    .lower().strip()

# Собираем весь текст из страниц
text = ''
for html_page in os.listdir('pages/'):
    file = open('pages/' + html_page)
    parser = BeautifulSoup(file.read(), features="html.parser")
    text += parser.get_text()

# Извлекаем токены
tokens = word_tokenize(text)

uniq_filtered_tokens = set()
stop_words = stopwords.words('russian')

# Обрабатываем и фильтруем токены
for token in tokens:
    preapared = prepare_token(token) 
    if preapared == '': continue
    if preapared in stop_words: continue
    uniq_filtered_tokens.add(preapared)
    
analyzer = pymorphy2.MorphAnalyzer()
lemmas = {}

# Записываем токены в файл и извлекаем леммы
tokens_file = open('tokens.txt', 'w')
for token in uniq_filtered_tokens:
    tokens_file.write(token + '\n')
    
    normal_form = analyzer.parse(token)[0].normal_form
    if normal_form not in lemmas:
        lemmas[normal_form] = []
    lemmas[normal_form].append(token)
tokens_file.close()

# Записываем леммы с токенами в файл
lemma_tokens_file = open('lemma_tokens.txt', 'w')
for lemma in lemmas:
    lemma_tokens_file.write(lemma + ' ')
    lemma_tokens_file.write(' '.join(lemmas[lemma]) + '\n')

lemma_tokens_file.close()