#!/bin/sh

docker-compose run --rm scheduler-backend /bin/bash -c "cd backend; python manage.py migrate; python run.py"
