#! /bin/bash
docker-compose run -e IS_TEST=true api pytest "$@"