upto=head
downto=-1

USE_DOCKER_COMPOSE=docker-compose
RUN_WITH_DEVOPS=$(USE_DOCKER_COMPOSE) run --rm devops
ifeq ("${IN_CI}", "1")
	RUN_TASK := 
else
	RUN_TASK := $(RUN_WITH_DEVOPS)
endif

# DB Migration

.PHONY: upgrade-db
upgrade-db: ensure-db-ready
	$(RUN_TASK) alembic upgrade $(upto)

.PHONY: downgrade-db
downgrade-db: ensure-db-ready
	$(RUN_TASK) alembic downgrade $(downto)

.PHONY: upgrade-testdb
upgrade-testdb: ensure-testdb-ready
	$(RUN_TASK) sh -c "DATABASE_URL=\$$TEST_DATABASE_URL alembic upgrade $(upto)"

.PHONY: downgrade-testdb
downgrade-testdb: ensure-testdb-ready
	$(RUN_TASK) sh -c "DATABASE_URL=\$$TEST_DATABASE_URL alembic downgrade $(downto)"

.PHONY: create-migration
create-migration:
	${RUN_TASK} alembic revision -m "${name}"

define ensure_db_service_ready
	@if [ -z `$(USE_DOCKER_COMPOSE) ps --services --filter "status=running" | grep ^$(1)$$` ]; then \
	  echo "[ ] starting $(1)..."; \
	  $(USE_DOCKER_COMPOSE) up -d $(1); \
	fi \
	&& while ! $(USE_DOCKER_COMPOSE) exec $(1) sh -c "pg_isready > /dev/null"; do sleep 1; done
endef

# Test
.PHONY: test-api
test-api: upgrade-testdb
	$(RUN_TASK) sh -c " \
		pylama rffa tests && \
		mypy rffa tests && \
		python -m pytest tests \
		"

# Utils

.PHONY: ensure-testdb-ready
ensure-testdb-ready:
ifeq ("${IN_CI}", "1")
ifeq ("$(findstring @testdb/,${TEST_DATABASE_URL})", "@testdb/")
	$(call ensure_db_service_ready,testdb)
else
	service postgresql start
endif
else
	$(call ensure_db_service_ready,testdb)
endif

.PHONY: ensure-db-ready
ensure-db-ready:
	$(call ensure_service_ready,db)

# Development environment init

.PHONY: init-db-and-testdb
init-db-and-testdb:
	$(eval DB_INIT_CMD := " \
		psql -d \$$$${POSTGRES_DB} -U \$$$${POSTGRES_USER} -c \" \
		CREATE SCHEMA IF NOT EXISTS \$$$${POSTGRES_DB}; \
		\"")

	@echo "Initializing db and testdb..."
	
	@$(USE_DOCKER_COMPOSE) up -d db
	@$(USE_DOCKER_COMPOSE) up -d testdb
	@$(USE_DOCKER_COMPOSE) down

	@$(USE_DOCKER_COMPOSE) up -d db
	@$(USE_DOCKER_COMPOSE) up -d testdb
	@$(USE_DOCKER_COMPOSE) exec db bash -c $(DB_INIT_CMD)
	@$(USE_DOCKER_COMPOSE) exec testdb bash -c $(DB_INIT_CMD)
	@$(USE_DOCKER_COMPOSE) down

	@echo "Done"

.PHONY: setup
setup: init-db-and-testdb

