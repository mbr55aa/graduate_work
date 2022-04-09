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

## Настройка Боба
- скачать русскую библиотеку [Vosk](https://drive.google.com/file/d/1VxUGfnFsuDOJZjts1bzOdaFazdjl-UKf/view?usp=sharing) 

# Взаимодействие
- Доступ к документации FastAPI осуществляется через http://localhost:8000/api/openapi
- Доступ к админке Django осуществляется через http://localhost/admin/ (user admin, password 123456)
