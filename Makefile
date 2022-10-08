include .env
export

CODE = app

prepare:
	poetry install

shell:
	poetry shell

run:
	docker compose up -d api

run-local:
	uvicorn service.__main__:app  --host 0.0.0.0 --port=${FASTAPI_PORT} --log-level=warning --reload

down:
	docker compose down

logs:
	docker compose logs

format:
	isort ${CODE}
	black ${CODE}

lint:
	pylint ${CODE}

