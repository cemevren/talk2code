load:
	pipenv run python3 -m ./scripts/load

test-integration:
	pipenv run pytest -s --disable-warnings ./test

dev:
	pipenv run uvicorn app.main:app --reload

build:
	sh ./docker/build.sh