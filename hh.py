#!/usr/bin/env python3

from requests import get
from pprint import pprint
import sys

url_vacancies= 'https://api.hh.ru/vacancies'

req_params = dict(
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
    snippet=item['snippet']
    pprint(clean(snippet['requirement']))
    if snippet['responsibility']:
        pprint(clean(snippet['responsibility']))
    print(item['employer']['name'] + ': ' + item['alternate_url'])

def clean(title):
    req = title
    try:
        req = req.replace('<highlighttext>', '')
        req = req.replace('</highlighttext>', '')
    except Exception:
        pass
    return req

def get_vacancy_desc(ident):
    r = get(url_vacancies + '/' + ident)
    r_data = r.json()
    if r.status_code != 200:
        pprint(r_data)
        raise RuntimeError("Wrong request")

def main() -> int:
    """Send requests to hh.ru"""
    if len(sys.argv) > 1:
        input = sys.argv[1:]
        if '-a' in input:
            input.remove('-a')
            input['search_field'] = None
        if '-h' in input:
            input.remove('-h')
            show_help()
            return 0
        req_params['text'] = ' '.join(input)
    else:
        show_help()
        return 1
    page = 0
    vacancies = []
    while True:
        req_params['page'] = page
        r = get(url_vacancies, req_params)
        r_data = r.json()
        if r.status_code != 200:
            pprint(r_data)
            return 1
        if len(r_data['items']) == 0: break
        if page == 0:
            print('Total count: %s' % r_data['found'])
        page += 1
        vacancies.extend(r_data['items'])

    for i, vac_item in enumerate(vacancies):
        show_vacancy_item(vac_item, i)
        print()
    return 0

def show_help():
    print("Usage: [-a] KEY_WORDS")
    print("-a - search in all fields. Default only in title")
    print("KEY_WORDS - words to search in vacancy fields")

if __name__ == '__main__':
    sys.exit(main())