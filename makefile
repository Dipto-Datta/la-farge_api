
run:
	docker compose up backend --build --remove-orphans

makemigrations:
	docker compose run backend python manage.py makemigrations

migrate:
	docker compose run backend python manage.py migrate

#superuser:
#	docker compose run backend python manage.py createsuperuser
#init-admin:
#	docker compose run backend python manage.py initadmin

action: ## My action helper -- VAR_NAME="Hello World" make action
	@echo $$VAR_NAME

new-app: ## APP="guide" make new-app
	django-admin startapp $$APP

run-db:
	docker compose up -d db

rm-null-images:
	docker image prune
