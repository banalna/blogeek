#!/usr/bin/env pwsh

Set-StrictMode -Version latest
$ErrorActionPreference = "Stop"

$settings = Get-Content -Path "settings.json" | ConvertFrom-Json
$image="$($settings.registry)/$($settings.name):$($settings.version)"
$container=$settings.name

# run mysql
docker run --name mysql --rm -d -e MYSQL_DATABASE="$($settings.MYSQL_DATABASE)" -e MYSQL_USER="$($settings.MYSQL_USER)" -e MYSQL_PASSWORD="$($settings.MYSQL_PASSWORD)" mysql/mysql-server:5.7

# run Redis
docker run --name redis -d -p 6379:6379 redis:3-alpine

# run elasticsearch
docker run --name elasticsearch -d -p 9200:9200 -p 9300:9300 --rm -e "discovery.type=single-node" docker.elastic.co/elasticsearch/elasticsearch-oss:7.7.0

# Build app image
docker build -f Dockerfile -t $image .

# Run app
docker run --name $container -d -p 8000:5000 --rm -e SECRET_KEY="$($settings.SECRET_KEY)" -e MS_TRANSLATOR_KEY="$($settings.MS_TRANSLATOR_KEY)" -e MAIL_SERVER="$($settings.MAIL_SERVER)" -e MAIL_PORT="$($settings.MAIL_PORT)" -e MAIL_USE_TLS="$($settings.MAIL_USE_TLS)" -e MAIL_USERNAME="$($settings.MAIL_USERNAME)" -e MAIL_PASSWORD="$($settings.MAIL_PASSWORD)" --link mysql:dbserver -e DATABASE_URL="$($settings.DATABASE_URL)" --link elasticsearch:elasticsearch -e ELASTICSEARCH_URL="$($settings.ELASTICSEARCH_URL)" --link redis:redis-server -e REDIS_URL="$($settings.REDIS_URL)" $image
# rq Worker
docker run --name rq-worker -d --rm -e SECRET_KEY="$($settings.SECRET_KEY)" -e MS_TRANSLATOR_KEY="$($settings.MS_TRANSLATOR_KEY)" -e MAIL_SERVER="$($settings.MAIL_SERVER)" -e MAIL_PORT="$($settings.MAIL_PORT)" -e MAIL_USE_TLS="$($settings.MAIL_USE_TLS)" -e MAIL_USERNAME="$($settings.MAIL_USERNAME)" -e MAIL_PASSWORD="$($settings.MAIL_PASSWORD)" --link mysql:dbserver -e DATABASE_URL="$($settings.DATABASE_URL)" --link elasticsearch:elasticsearch -e ELASTICSEARCH_URL="$($settings.ELASTICSEARCH_URL)" --link redis:redis-server -e REDIS_URL="$($settings.REDIS_URL)"  --entrypoint venv/bin/rq $image worker -u "$($settings.REDIS_URL)" blogeek-tasks

