env:
	cp config/.env.example config/.env

pull:
	docker-compose pull

up:
	docker-compose up --build -d

down:
	docker-compose down --remove-orphans
