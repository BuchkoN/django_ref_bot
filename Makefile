DC = docker-compose
ENV = --env-file .env
APP_FILE = docker/docker-compose.app.yaml
STORAGE_FILE = docker/docker-compose.storage.yaml
APP_CONTAINER = web_app

.PHONY: app-start
app-start:
	$(DC) -f $(APP_FILE) -f $(STORAGE_FILE) $(ENV) up --build -d

.PHONY: app-down
app-down:
	$(DC) -f $(APP_FILE) -f $(STORAGE_FILE) $(ENV) down

.PHONY: app-logs
app-logs:
	$(DC) -f $(APP_FILE) logs -f

.PHONY: app-shell
app-shell:
	$(DC) -f $(APP_FILE) -f $(STORAGE_FILE) exec $(APP_CONTAINER) ./manage.py shell

.PHONY: app-makemigrations
app-makemigrations:
	$(DC) -f $(APP_FILE) -f $(STORAGE_FILE) exec $(APP_CONTAINER) ./manage.py makemigrations

.PHONY: app-migrate
app-migrate:
	$(DC) -f $(APP_FILE) -f $(STORAGE_FILE) exec $(APP_CONTAINER) ./manage.py migrate