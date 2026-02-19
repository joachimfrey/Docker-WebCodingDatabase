.PHONY: help build up down logs shell migrate createsuperuser clean restart

help:
	@echo "JF Datenbank - Docker Befehle"
	@echo ""
	@echo "Verfügbare Befehle:"
	@echo "  make build              - Docker Images bauen"
	@echo "  make up                 - Container starten"
	@echo "  make down               - Container stoppen"
	@echo "  make logs               - Logs anschauen"
	@echo "  make shell              - Django Shell öffnen"
	@echo "  make migrate            - Migrationen durchführen"
	@echo "  make makemigrations     - Migrationen erstellen"
	@echo "  make createsuperuser    - Admin-Benutzer erstellen"
	@echo "  make bash               - Bash im Container"
	@echo "  make clean              - Container & Volumes löschen"
	@echo "  make restart            - Container neu starten"
	@echo "  make check-deploy       - Production Check"

build:
	docker-compose build

up:
	docker-compose up -d
	@echo "Containers started. Access at http://localhost"

down:
	docker-compose down

logs:
	docker-compose logs -f app

logs-db:
	docker-compose logs -f postgres

logs-nginx:
	docker-compose logs -f nginx

shell:
	docker-compose exec app python manage.py shell

migrate:
	docker-compose exec app python manage.py migrate

makemigrations:
	docker-compose exec app python manage.py makemigrations

createsuperuser:
	docker-compose exec app python manage.py createsuperuser

bash:
	docker-compose exec app bash

bash-db:
	docker-compose exec postgres bash

check-deploy:
	docker-compose exec app python manage.py check --deploy

clean:
	docker-compose down -v
	@echo "All containers and volumes removed"

restart:
	docker-compose restart

collectstatic:
	docker-compose exec app python manage.py collectstatic --noinput

ps:
	docker-compose ps
