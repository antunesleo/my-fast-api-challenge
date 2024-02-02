build:
	docker-compose build

run:
	docker-compose up

test:
	./bin/runtests.sh

format:
	black .