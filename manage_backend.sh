#!/bin/sh

docker-compose run --rm scheduler-backend /bin/bash -c "python manage.py collectstatic --no-input; python manage.py migrate; python run.py"
