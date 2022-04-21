# Репозиторий
[https://github.com/mbr55aa/graduate_work](https://github.com/mbr55aa/graduate_work)

# Техническое Задание
[ссылка](https://docs.google.com/document/d/1TBbOgtxxFOSANF7Od0uXKds1nT56b6RrfJuaCQw-IpU)

# Настройка
1. Создать .env файл на основе .env.example:
```console
$ make env
```
2. Сбилдить и запустить:
```console
$ make up
```
3. Остановить приложение:
```console
$ make down
```

## Настройка Postgres
- Добавление файлов БД. Создайте в корне проекта папку pgdata, и поместите туда файлы БД (можно использовать вот [эти](https://drive.google.com/file/d/134lPr53ckFRPhupPFg7QB71fIVpv5PKz/view?usp=sharing))

- Восстановление БД из дампа:
  1. Скачайте файл [db.dump](https://drive.google.com/file/d/1m7xdEP368F4tEaXireX7QOVUMbtzkFvc/view?usp=sharing)
  2. Переместите файл в папку `postgres` в корне проекта
  3. Запустите проект и внутри контейнера postgres и выполните следующие команды:
     ```console
     $ su postgres
     ```
     ```console
     $ dropdb movies
     ```
     ```console
     $ pg_restore -C -d postgres /var/lib/postgresql/backup/db.dump
     ```

## Настройка Bob
- Может потребоваться установка portaudio
  - На MAC
    ```console
    $ brew install portaudio
    ```
  - На Ubuntu
    ```console
    $ sudo apt-get install portaudio19-dev
    ```
  
- Для поддержки работы оффлайн, необходимо:
  - в папку `bob/models` поместить [модель](https://drive.google.com/file/d/1INh4uMXfcJfNXhisvVBWrJ_kDNxFoziT/view?usp=sharing)
  - название папки с моделью добавить в .env файл проекта в переменную `VOSK_MODEL`

- Описание возможностей ассистента находится в отдельном [readme](bob/README.md)

## Настройка Алисы

- Инструкция по настройке Алисы и описание возможностей ассистента в отдельном [readme](alice/README.md)

# Взаимодействие
## Облачный инстанс
- Документация Assistant: http://51.250.26.192:8001/apidocs/
- Assistant API: http://51.250.26.192:8001/api/v1/bob/
- Документация FastAPI: http://51.250.26.192:8000/api/openapi
- Админка Django: http://51.250.26.192/admin/ (user admin, password 123456)

## Локальный инстанс
- Документация Assistant: http://localhost:8001/apidocs/
- Assistant API: http://localhost:8001/api/v1/bob/
- Документация FastAPI: http://localhost:8000/api/openapi
- Админка Django: http://localhost/admin/ (user admin, password 123456)

# Известные проблемы
- **Assistant API и FastAPI ничего не находят:**<br/>
Если в момент первого запуска проекта не было папки postgres\pgdata\ или в процессе работы был перезалит дамп то 
необходимо сбросить состояние ETL, для этого удалите файл postgres_to_es\state.json и перезапустите сервисы.
