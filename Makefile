POETRY 	       = poetry run
DC	           = docker compose
CODE		   = app/

.PHONY: install
install:
	poetry install --no-interaction

############ DOCKER ############
.PHONY: build
build:
	$(DC) build

.PHONY: up
up:
	$(DC) up -d
	$(DC) exec backend alembic upgrade head

.PHONY: down
down:
	$(DC) down --volumes

.PHONY: logs
logs:
	$(DC) logs -f
############ DOCKER ############


############ MIGRATIONS #############
.PHONY: migrate
migrate:
	$(POETRY) alembic upgrade head

.PHONY: gen_migration
gen_migration:
	$(POETRY) alembic revision --autogenerate -m $(m)
############ MIGRATIONS #############