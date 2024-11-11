DC = docker compose
EXEC = docker exec -it
ENV = --env-file .env

.PHONY: app
app:
	${DC} up --build -d

.PHONY: down
down:
	${DC} down

.PHONY: logs
logs:
	${DC} logs

.PHONY:
create_migraton:
	@read -p "Enter your message: " MESSAGE; \
	${DC} exec api sh -c "alembic revision --autogenerate -m '$$MESSAGE'"

.PHONY:
migrate:
	${DC} exec api sh -c "alembic upgrade head"

.PHONY:
test:
	${DC} exec api sh -c "pytest"

.PHONY:
certs:
	mkdir -p ./app/certs; \
	openssl genrsa -out ./app/certs/private.pem 2048; \
	openssl rsa -in ./app/certs/private.pem -outform PEM -pubout -out ./app/certs/public.pem;
