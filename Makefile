build:
	docker-compose build

run:
	docker-compose up

test:
	./bin/runtests.sh

coverage:
	docker-compose run api pytest --cov=tests

format:
	black .