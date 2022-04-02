env:
	cp config/.env.example config/.env

pull:
	docker-compose pull

up:
	docker-compose up --build -d

down:
	docker-compose down --remove-orphans

fakemigrate:
	docker-compose run --rm movies-admin python manage.py migrate movies --fake && docker-compose run --rm movies-admin python manage.py migrate

createsuperuser:
	docker-compose run --rm movies-admin python manage.py createsuperuser
