import os, math

doc_tokens = {}
doc_lemmas = {}

# Чтение токенов вместе с номером документа
for file_name in os.listdir('tokens/'):
    doc = open('tokens/' + file_name)
    doc_number = int(file_name.split('.')[0])
    doc_tokens[doc_number] = doc.read().split(' ')
    
# Чтение лемм вместе с номером документа
for file_name in os.listdir('lemmas/'):
    doc = open('lemmas/' + file_name)
    doc_number = int(file_name.split('.')[0])
    doc_lemmas[doc_number] = doc.read().split(' ')
    

    
# Запись tf_idf токенов документа в файл
def write_token_tf_idf(doc_number, tf_idf_list):
    file = open('tokens_tf_idf/{}.txt'.format(doc_number), 'w')
    file.write('\n'.join(tf_idf_list))
    file.close()

# Запись tf_idf токенов документа в файл
def write_lemma_tf_idf(doc_number, tf_idf_list):
    file = open('lemmas_tf_idf/{}.txt'.format(doc_number), 'w')
    file.write('\n'.join(tf_idf_list))
    file.close()
    
# Считывание инвертированного индекса    
def read_inverted_index():
    inverted_index = dict()
    with open('inverted_index.txt', 'r') as file:
        for line_number, line in enumerate(file):
            entry = line.split(' ')
            inverted_index[entry[0]] = entry[1:]
    return inverted_index

# Считаем tf-idf для токенов
def calc_tokens():
    docs_number = len(doc_tokens)
    files_count_by_token = dict()
    for tokens in doc_tokens.values():
        for unit in tokens:
            if unit in files_count_by_token.keys():
                files_count_by_token[unit] += 1
            else:
                files_count_by_token[unit] = 1
    for item in doc_tokens.items():
        tokens = item[1]
        doc_number = item[0]
        tf_idf_list = []
        counts = dict()
        units_number = len(tokens)
        for unit in tokens:
            if unit in counts.keys():
                counts[unit] += 1
            else:
                counts[unit] = 1
        for unit, count in counts.items():
            if unit in files_count_by_token.keys():
                tf = count / units_number
                idf = math.log10(docs_number / files_count_by_token[unit])
                tf_idf = tf * idf
                tf_idf_list.append("{} {} {}".format(unit, idf, tf_idf))
        
        write_token_tf_idf(doc_number, tf_idf_list)
        
# Считаем tf-idf для лемм
def calc_lemmas():
    docs_number = len(doc_tokens)
    
    inverted_index = read_inverted_index()
    idfs = {unit: math.log10(docs_number / len(doc_ids)) for unit, doc_ids in inverted_index.items()}
    
    for item in doc_lemmas.items():
        doc_number = item[0]
        tf_idf_list = []
        counts = dict()
        units = item[1]
        units_number = len(units)
        for unit in units:
            if unit in counts.keys():
                counts[unit] += 1
            else:
                counts[unit] = 1
        for unit, count in counts.items():
            if unit in idfs.keys():
                tf = count / units_number
                idf = idfs[unit]
                tf_idf = tf * idf
                tf_idf_list.append("{} {} {}".format(unit, idf, tf_idf))

        write_lemma_tf_idf(doc_number, tf_idf_list)
        
def write_all_lemmas_idf():
    total_lemmas = set()
    for lemmas in doc_lemmas:
        total_lemmas.update(doc_lemmas[lemmas])
    lemmas_docs_arr = [i[1] for i in doc_lemmas.items()]
    
    file = open('lemmas_idf.txt', 'w')
    for word in total_lemmas:
        idf = math.log10(len(lemmas_docs_arr) / sum([1.0 for i in lemmas_docs_arr if word in i]))
        file.write('{} {}\n'.format(word, idf))
    
        
# calc_tokens()
# calc_lemmas()
write_all_lemmas_idf()