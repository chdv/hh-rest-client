#!/usr/bin/env python3

import grequests
from requests import get
from pprint import pprint
import sys
from parsers import collect
import re

url_vacancies = 'https://api.hh.ru/vacancies'

req_params = dict(
    area=1,  # Москва
    text='python',  # текст поиска
    search_field='name',  # поля для поиска
    schedule='remote',  # формат работы
    page=0,  # страница
    per_page=10,  # строк на каждой странице
)

html_tags_re = re.compile('<.*?>')

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
    snippet = item['snippet']
    if snippet['requirement']:
        print(clean(snippet['requirement']))
    if snippet['responsibility']:
        print(clean(snippet['responsibility']))
    print(item['employer']['name'] + ': ' + item['alternate_url'])

def clean(title):
    if title: return re.sub(html_tags_re, ' ', title)
    return None

def get_vacancy_desc(ident):
    r = get(url_vacancies + '/' + ident)
    r_data = r.json()
    if r.status_code != 200:
        pprint(r_data)
        raise RuntimeError("Wrong request")
    return r_data['description']

def get_vacancies_desc(idents):
    rs = (grequests.get(url_vacancies + '/' + _id) for _id in idents)
    resps = grequests.map(rs)
    result=[]
    for resp in resps:
        if resp.status_code != 200:
            pprint(resp)
            raise RuntimeError("Wrong request")
        result.append(resp.json()['description'])
    return result

def main() -> int:
    """Send requests to hh.ru"""
    get_stat = False
    if len(sys.argv) > 1:
        input_pars = sys.argv[1:]
        if '-a' in input_pars:
            input_pars.remove('-a')
            req_params['search_field'] = None
        if '-s' in input_pars:
            input_pars.remove('-s')
            get_stat = True
        if '-h' in input_pars:
            input_pars.remove('-h')
            show_help()
            return 0
        req_params['text'] = ' '.join(input_pars)
    else:
        show_help()
        return 1

    page = 0
    vacancies = []
    item_num = 1
    keys_map = {}
    total=0
    while True:
        req_params['page'] = page
        r = get(url_vacancies, req_params)
        r_data = r.json()
        if r.status_code != 200:
            pprint(r_data)
            return 1
        data_items = r_data['items']
        if len(data_items) == 0: break
        if page == 0:
            total=r_data['found']
            print('Total count: %s' % total)
        page += 1
        if get_stat:
            ids = [item['id'] for item in data_items]
            vac_descs = get_vacancies_desc(ids)
            for desc in vac_descs:
                keys_map = collect(keys_map, desc)
            vacancies.extend(data_items)
        else:
            for item in data_items:
                show_vacancy_item(item, item_num)
                print()
                item_num += 1

    if get_stat:
        print('Key words statistics:')
        print(keys_map)
        print()
        for i, vac_item in enumerate(vacancies):
            show_vacancy_item(vac_item, i+1)
            print()
    return 0

def show_help():
    print("Usage: [-a][-s] WORDS")
    print("-a - search in all fields. Default only in title")
    print("-s - make statistics by key words in vacancies")
    print("WORDS - words to search in vacancy fields")

if __name__ == '__main__':
    sys.exit(main())
