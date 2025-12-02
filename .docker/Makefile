.PHONY: create-docker run-docker run-debug-docker stop-docker clean-docker

# subir o projeto
create-clear-docker:
	docker compose build --no-cache

create-docker:
	docker compose build

run-docker:
	docker compose up -d

run-debug-docker:
	docker compose up

# parar o projeto
stop-clear-docker:
	docker compose down -v

stop-docker:
	docker compose down

clean-docker:
	sudo rm -r data/postgres -R

create-network:
	docker network create shared_net