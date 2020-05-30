## parser
1. Предлоги взяты отсюда: https://bit.ly/2AjvZai  
2. Настройки хранятся в `settings.py`  

`DEPTH = 2` - глубина вхождения для скрипта, если установить `DEPTH = 1`,
то сохраним только первую страницу и все слова из нее.  
`PAGES_TO_VISIT = 5` - ограничение по количеству сохраненных страниц  
`URL = 'https://habr.com/ru/'` - домен по умолчанию    
`BASE_DIR = os.getcwd()` - текущая директория скрипта  
`PAGES_FOLDER = os.path.join(BASE_DIR, 'saved_pages')` - в `saved_pages` будем сохранять страницы  
`WORDS_FILE = 'words.txt'` - в этом файле будем хранить слова, которые потом будем считать  
`DELAY_BETWEEN_REQUEST = 0.3` - задержка перед следующим запросом  
`POPULAR_WORDS_LIMIT = 10` - ограничение, сколько наиболее часто используемых слов находить  
`PREPOSITIONS` - предлоги, которые исключаем из подсчета
```
RETRY_CODES = [413, 429, 500, 502, 503, 504] - коды ответов, от сервера при которых делаем повторный запрос
RETRY_COUNT = 4     - количество повторных запросов, если запрос не удачный
RETRY_TIMEOUT = 2   - сколько ждать ответа от сервера
RETRY = True        - делать ли повторные запросы
REPEAT_TIMEOUT = 2  - через сколько времени делать повторный запрос
```
  
``
``
``
``
``
``
``
``
``
``
``
``


    
