#!/usr/bin/env python3

from requests import get
from pprint import pprint
import sys

url='https://api.hh.ru/vacancies'

params = dict(
    area=1, # Москва
    text='python', # текст поиска
    search_field='name', # поля для поиска
    schedule='remote', # формат работы
    page=0, # страница
    per_page=100, # строк на каждой странице
)

def show_vacancy_item(item, item_num):
    """ Show vacancy json item"""
    print(str(item_num) + '. ' + item['name'], end=' ')
    if item['salary']:
        print('(', end='')
        if item['salary']['from']:
            print(item['salary']['from'], end='')
        if item['salary']['to']:
            print('-', end='')
            print(item['salary']['to'], end='')
        if item['salary']['currency']:
            print(' ' + item['salary']['currency'], end='')
        print(')')
    else:
        print()
    req = item['snippet']['requirement']
    try:
        req = req.replace('<highlighttext>', '')
        req = req.replace('</highlighttext>', '')
    except Exception:
        pass
    pprint(req)
    print(item['employer']['name'] + ': ' + item['alternate_url'])

def main() -> int:
    """Send requests to hh.ru"""
    st = 1
    if len(sys.argv) > 1:
        if sys.argv[1] == '-a':
            params['search_field'] = None
            st += 1
        if sys.argv[1] == '-h':
            show_help()
            return 0
        if len(sys.argv) > st:
            params['text'] = ' '.join(sys.argv[st:])
    else:
        show_help()
        return 1
    page = 0
    item_num = 1
    while True:
        params['page'] = page
        r = get(url, params)
        r_data = r.json()
        if r.status_code != 200:
            pprint(r_data)
            return 1
        if len(r_data['items']) == 0: break
        if page == 0:
            print('Total count: %s' % r_data['found'])
        page += 1
        for item in r_data['items']:
            show_vacancy_item(item, item_num)
            print()
            item_num += 1
    return 0

def show_help():
    print("Usage: [-a] KEY_WORDS")
    print("-a - search in all fields. Default only in title")
    print("KEY_WORDS - words to search in vacancy fields")

if __name__ == '__main__':
    sys.exit(main())