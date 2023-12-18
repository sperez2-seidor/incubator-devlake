#!/bin/bash

cd "$(dirname "$0")"
source .env
CTX='{"db_url":"sqlite+pysqlite:///:memory:", "connection": {"token":"f9b37f42164f572e14952d58252df","subscriptionCode": "14f48190b2ce42a78a80c2ff9dc27fc5" }}'
poetry run python myplugin/main.py "$@"