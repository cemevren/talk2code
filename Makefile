# Detect the OS
UNAME_S := $(shell uname -s)

load:
	pipenv run python3 -m ./scripts/load

test-integration:
	pipenv run pytest -s --disable-warnings ./test

dev:
	@cd ./backend && pipenv run fastapi dev

open:
ifeq ($(UNAME_S), Darwin)
	@open http://localhost:8080
else ifeq ($(UNAME_S), Linux)
	@xdg-open http://localhost:8080
else ifeq ($(OS), Windows_NT)
	@start http://localhost:8080
else
	@echo "Unsupported OS"
endif

start:
	docker-compose up -d --build && make open
