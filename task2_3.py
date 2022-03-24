import os, pymorphy2, string

from bs4 import BeautifulSoup
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

# Функция очистки текста
def prepare_token(token):
    if (token in string.punctuation):
        return ''
    return ''.join([i for i in token if not i.isdigit()])\
    .lower().strip()

uniq_filtered_tokens = set()
stop_words = stopwords.words('russian')
analyzer = pymorphy2.MorphAnalyzer()
lemmas = {}
inverted_index = {}

def write_tokens_and_lemmas_to_file(doc_num, doc_tokens, doc_lemmas):
    doc_tokens_file = open('tokens/{}.txt'.format(doc_num), 'w')
    doc_tokens_file.write(' '.join(doc_tokens))
    doc_tokens_file.close()
    
    doc_lemmas_file = open('lemmas/{}.txt'.format(doc_num), 'w')
    doc_lemmas_file.write(' '.join(doc_lemmas))
    doc_lemmas_file.close()

# Обрабатываем весь текст из страниц
for html_page in os.listdir('pages/'):
    if not html_page.endswith("html"):
        continue
    doc_num = html_page.split('.')[0]
    file = open('pages/' + html_page)
    parser = BeautifulSoup(file.read(), features="html.parser")
    text = parser.get_text()
    tokens = word_tokenize(text)
    # Обрабатываем и фильтруем токены
    
    doc_tokens = set()
    doc_lemmas = set()
    for token in tokens:
        preapared = prepare_token(token) 
        if preapared == '': continue
        if preapared in stop_words: continue
        doc_tokens.add(preapared)
        
        normal_form = analyzer.parse(token)[0].normal_form
        doc_lemmas.add(normal_form)
        if normal_form not in lemmas:
            lemmas[normal_form] = set()
        lemmas[normal_form].add(token)
        # формируем инв. индекс         
        if normal_form not in inverted_index:
            inverted_index[normal_form] = set()
        inverted_index[normal_form].add(doc_num)
        
    write_tokens_and_lemmas_to_file(doc_num, doc_tokens, doc_lemmas)
    uniq_filtered_tokens.update(doc_tokens)

# Записываем токены в файл и извлекаем леммы
tokens_file = open('tokens.txt', 'w')
for token in uniq_filtered_tokens:
    tokens_file.write(token + '\n')
tokens_file.close()

# Записываем леммы с токенами в файл
lemma_tokens_file = open('lemma_tokens.txt', 'w')
for lemma in lemmas:
    lemma_tokens_file.write(lemma + ' ')
    lemma_tokens_file.write(' '.join(lemmas[lemma]) + '\n')
lemma_tokens_file.close()

# Записываем инв. индекс
inverted_index_file = open('inverted_index.txt', 'w')
for lemma in inverted_index:
    inverted_index_file.write(lemma + ' ')
    inverted_index_file.write(' '.join(inverted_index[lemma]) + '\n')
inverted_index_file.close()