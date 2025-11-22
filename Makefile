
DC = docker compose
EXEC = docker exec -it
LOGS = docker logs
ENV = --env-file .env

APP_FILE = docker/app.yaml
DB_FILE = docker/postgresql.yaml

APP_CONTAINER = main-app
DB_CONTAINER = postgres_db

.PHONY: db db-down db-logs db-shell db-reset

db:
	${DC} -f ${DB_FILE} ${ENV} up -d postgres

db-down:
	@echo "Stopping PostgreSQL..."
	${DC} -f ${DB_FILE} down

db-reset: db-down db
	@echo "Database recreated and migrations applied!"

db-logs:
	${LOGS} ${DB_CONTAINER} -f

db-shell:
	${EXEC} ${DB_CONTAINER} psql -U ${POSTGRES_USER:-postgres} -d ${POSTGRES_DB:-products_db}

app:
	${DC} -f ${DB_FILE} -f ${APP_FILE} ${ENV} up --build -d

app-down:
	${DC} -f ${APP_FILE} -f ${DB_FILE} down

app-logs:
	${LOGS} ${APP_CONTAINER} -f

app-shell:
	${EXEC} ${APP_CONTAINER} bash

migrations:
	${DC} -f ${DB_FILE} -f ${APP_FILE} ${ENV} run --rm ${APP_CONTAINER} alembic upgrade head

all: app
.DEFAULT_GOAL := all
