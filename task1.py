from bs4 import BeautifulSoup
import requests as r

wiki_url = 'https://ru.wikipedia.org'
writers_url = wiki_url + '/wiki/Категория:Композиторы_XX_века'

index = open('index.txt', 'w')

page = r.get(writers_url)

soup = BeautifulSoup(page.content, 'html.parser')

table = soup.find(id='mw-pages')

count = 1

for a in table.find_all('a', href=True):
    page_url = wiki_url + a['href']
    page = r.get(page_url)
    with open('pages/' + str(count) + '.html', 'w') as out:
        out.write(page.text)
        out.close()
        print(str(count), end='\r')
        index.write(str(count) + '\t' + page_url + '\n')
    count += 1
    
index.close()