#!/bin/bash
set -e
set -u
function create_databases() {
    user=$1
    database=$2
    password=$3
    psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" <<-EOSQL
      CREATE USER $user with encrypted password '$password';
      CREATE DATABASE $database;
      GRANT ALL PRIVILEGES ON DATABASE $database TO $user;
      ALTER DATABASE $database OWNER TO $user;
EOSQL

    if [ $user == "app" ]
    then
      psql -U $user -d $database -f /tmp/dump.sql
    fi

}

# POSTGRES_MULTIPLE_DATABASES=app:movies_database:123456,admin:auth:12345678
if [ -n "$POSTGRES_MULTIPLE_DATABASES" ]; then
  for db in $(echo $POSTGRES_MULTIPLE_DATABASES | tr ',' ' '); do
    user=$(echo $db | awk -F":" '{print $1}')
    database=$(echo $db | awk -F":" '{print $2}')
    password=$(echo $db | awk -F":" '{print $3}')
    echo "Creating database $database with user $user and password $password"
    create_databases $user $database $password
  done
fi


