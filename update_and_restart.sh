#!/bin/bash
set -e
docker pull andybaumgar/nycmesh-calendar-bot:latest && docker-compose down && docker-compose up -d && echo "Update Complete!"
