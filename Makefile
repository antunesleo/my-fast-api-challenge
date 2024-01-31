build:
	docker-compose build

run:
	./bin/run.sh

test:
	./bin/runtests.sh

format:
	black .