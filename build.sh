#!/bin/bash
docker rmi $(docker images -f "dangling=true" -q)
docker-compose -f cadastro-contas.yml build --force-rm --no-cache