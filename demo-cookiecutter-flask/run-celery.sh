#!/usr/bin/env bash

set -euo pipefail

redis-server & 

celery -A my_flask_app.tasks.app worker -B --loglevel=DEBUG -c 1
#celery -A tasks beat --loglevel=INFO