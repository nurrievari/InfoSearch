DOCS_COUNT = 202

# Чтение инв. индекса из файла
inverted_index = {}
for line in open('inverted_index.txt', 'r').read().splitlines():
    data = line.split(' ')
    lemma = data[0] 
    doc_numbers = [int(num) for num in data[1:]]
    inverted_index[lemma] = doc_numbers
    
query = 'поиск & !материал | собака'
input_bool = query.replace(' ', '')

all_nums = set(range(DOCS_COUNT + 1))

        # Объединение сетов | 
result = set.union(* \
            # Пересечение сетов &                    
            [set.intersection(* \
                [set( \
                    # Если отрицание, то вычитаем из всех номеров документов                      
                     all_nums.difference(inverted_index[q[1:]]) \
                     if q.startswith('!') \
                    # Иначе берем только номера документов этого слова                      
                     else inverted_index[q]\
                    ) \
             for q in and_query.split('&')]) \
          for and_query in input_bool.split('|')])

print('Query - \'{}\', result -  {}'.format(query, result))