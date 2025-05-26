# HH rest client

Консольный клиент к rest-api сайта hh.ru

Предварительно требуется установленный пакеты requests и grequests. В ubuntu устанавливается через пакетный менеджер apt
```
sudo apt install python3-requests
sudo apt install python3-grequests
```
Если ошибка вида 
```
bash: ./hh: Permission denied
```
Требуется выполнить команду 
```
chmod +x hh
```
Получение справки по программе
```
./hh -h
```
Поиск по ключевым полям в заголовке вакансии
```
$ ./hh java python linux
```
Поиск по ключевым полям в заголовке и описании вакансии
```
./hh -a java python linux
```
Вывод статистики встречаемости ключевых слов на английском языке
```
./hh -s java python linux
```
Пример ответа программы. Детальное описание вакансии открывается после перехода по ссылке
```
Total count: 290
1. Python разработчик Middle+ (-200000 RUR)
('Опыт разработки на Python 3.10+ в production-разработке. Опыт работы с LLM, '
 'в частности с langchain. ')
EORA: https://hh.ru/vacancy/120836411

2. Python Backend разработчик ( FastAPI, Django) 
('Опыт работы с FastAPI, Django. Будет плюсом SQLAlchemy. Опыт работы с SQL и '
 'NoSQL БД, брокерами очередей. Будет плюсом опыт...')
Верме: https://hh.ru/vacancy/120490383
```
Скрипт test_get_async.py позволяет сравнить скорость синхронного и асинхронного выполнения запросов
```
$ ./test_get_async.py 
g_requests: 0.6496844291687012
sync_get: 1.710972785949707
asyncio_get: 1.583308458328247
```