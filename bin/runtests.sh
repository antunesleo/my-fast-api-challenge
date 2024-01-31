#! /bin/bash
docker-compose run -e IS_TEST=false api pytest "$@"