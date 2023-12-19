build:
	docker compose up --build -d

init_migrations:
	docker compose run --user 1000 app sh -c 'alembic init migrations'
	cp migrations_config.py app/migrations/env.py

migration:
	docker compose run --user 1000 app sh -c 'alembic revision --autogenerate -m "$(MESSAGE)"'
	docker compose run --user 1000 app sh -c 'alembic upgrade head'

test:
	pytest app --log-cli-level=INFO --capture=tee-sys