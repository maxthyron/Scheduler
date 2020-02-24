#!/bin/sh
if [[ -z "${CONF_DIR}" ]]; then
  CONF_DIR=""
fi

if [[ -z "${DEPLOY_ENV}" ]]; then
  read -rp "Enter the name of database: " DB
  read -rp "Enter username: " USER
  read -rsp "Enter password: " PASS

  psql -d postgres -ec "CREATE USER $USER WITH PASSWORD '$PASS';"
  psql -d postgres -ec "CREATE DATABASE $DB OWNER $USER;"
  psql -d postgres -ec "ALTER ROLE $USER SET client_encoding TO 'utf8';"
  psql -d postgres -ec "ALTER ROLE $USER SET default_transaction_isolation TO 'read committed';"
  psql -d postgres -ec "ALTER ROLE $USER SET timezone TO 'UTC';"
  psql -d postgres -ec "GRANT ALL PRIVILEGES ON DATABASE $DB TO $USER;"

  echo "DATABASE_URL=\"postgres://$USER:$PASS@localhost:5432/$DB\"" > "${CONF_DIR}.env"
  echo "SECRET_KEY=""$(python -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())')" >> "${CONF_DIR}.env"
  echo "DEBUG=True" >> "${CONF_DIR}.env"

else

  if [[ -z "${POSTGRES_DB}" ]]; then
    echo "DB_ENV variable is not set."
    exit 1
  else
    read -rp "Enter the name of database: " POSTGRES_DB
  fi

  if [[ -z "${POSTGRES_USER}" ]]; then
    echo "USER_ENV variable is not set."
    exit 1
  else
    read -rp "Enter username: " POSTGRES_USER
  fi

  if [[ -z "${POSTGRES_PASSWORD}" ]]; then
    echo "PASS_ENV variable is not set."
    exit 1
  else
    read -rsp "Enter password: " POSTGRES_PASSWORD
  fi

  echo "POSTGRES_USER=${POSTGRES_USER}" > "${CONF_DIR}postgres.env"
  echo "POSTGRES_PASSWORD=${POSTGRES_PASSWORD}" >> "${CONF_DIR}postgres.env"
  echo "POSTGRES_DB=${POSTGRES_DB}" >> "${CONF_DIR}postgres.env"

  echo "DATABASE_URL=\"postgres://$POSTGRES_USER:$POSTGRES_PASSWORD@scheduler-db:5432/$POSTGRES_DB\"" > "${CONF_DIR}.env"
  echo "SECRET_KEY=""$(python3 -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())')" >> "${CONF_DIR}.env"
  echo "DEBUG=False" >> "${CONF_DIR}.env"
fi