build:
	docker compose up --build

init_migrations:
	docker compose run --user 1000 app sh -c 'alembic init migrations'

make_migration:
	docker compose run --user 1000 app sh -c 'alembic revision --autogenerate -m "$(MESSAGE)"'
	docker compose run --user 1000 app sh -c 'alembic upgrade head'

test:
	docker compose run app sh -c 'pytest'