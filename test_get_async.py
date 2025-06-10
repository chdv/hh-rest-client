#!/usr/bin/env python3

import time
import grequests
import hh
import asyncio
import threading

ids=['120236562','120877600', '120776613', '120072589']
ids.extend(ids*2)

def sync_get():
    for _id in ids:
        res = hh.get_vacancy_desc(_id)

def thread_get():
    threads = []
    for _id in ids:
        t=threading.Thread(target=hh.get_vacancy_desc, args=(_id,))
        t.start()
        threads.append(t)
    for t in threads: t.join()

async def async_get():
    for _id in ids:
        res = await asyncio.to_thread(hh.get_vacancy_desc, _id)

def asyncio_get():
    asyncio.run(async_get())

def g_requests():
    rs = (grequests.get(hh.url_vacancies + '/' + _id) for _id in ids)
    result = grequests.map(rs)

def test_time(func):
    start = time.time()
    func()
    print(func.__name__ + ': ' + str(time.time() - start))

if __name__ == '__main__':
    test_time(g_requests)
    test_time(sync_get)
    test_time(asyncio_get)
    test_time(thread_get)
