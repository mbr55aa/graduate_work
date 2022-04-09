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
- Добавление файлов БД. Создайте в корне проекта папку pgdata, и поместите туда файлы БД (можно использовать вот [эти](https://drive.google.com/file/d/1INh4uMXfcJfNXhisvVBWrJ_kDNxFoziT/view?usp=sharing))

- Восстановление БД из дампа:
  1. Скачайте файл [db.dump]()
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

# Взаимодействие
- Доступ к документации FastAPI осуществляется через http://localhost:8000/api/openapi
- Доступ к админке Django осуществляется через http://localhost/admin/ (user admin, password 123456)

