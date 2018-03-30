#!/usr/bin/env bash

echo "---------------------------------------------------------------------------------------------------------------"
echo "Install python 3.6 and pip3"
echo "---------------------------------------------------------------------------------------------------------------"
sudo apt-get install software-properties-common
sudo add-apt-repository ppa:deadsnakes/ppa
sudo apt-get update
sudo apt-get install python3.6 -y
sudo apt-get install python3.6-dev -y
sudo apt-get install python3-pip -y

echo "---------------------------------------------------------------------------------------------------------------"
echo "Create virtualenv"
echo "---------------------------------------------------------------------------------------------------------------"
mkdir virtualenv
cd virtualenv/
pip3 install virtualenv
virtualenv env36 -p python3.6

echo "---------------------------------------------------------------------------------------------------------------"
echo "Install and configure PostgreSQL"
echo "---------------------------------------------------------------------------------------------------------------"
APP_DB_USER=warehouse_user
APP_DB_PASS=super_secret
APP_DB_NAME=warehouse
PG_VERSION=9.5

sudo apt-get -y install "postgresql-$PG_VERSION" "postgresql-contrib-$PG_VERSION"

PG_CONF="/etc/postgresql/${PG_VERSION}/main/postgresql.conf"
PG_HBA="/etc/postgresql/$PG_VERSION/main/pg_hba.conf"
PG_DIR="/var/lib/postgresql/$PG_VERSION/main"

# Edit postgresql.conf to change listen address to '*'
sudo sed -i "s/#listen_addresses = 'localhost'/listen_addresses = '*'/" "$PG_CONF"

# Append to pg_hba.conf to add password auth
# Accept all IPv4 connections - FOR DEVELOPMENT ONLY!!!
echo "host    all             all             all                     md5" | sudo tee -a "$PG_HBA"

# Explicitly set default client_encoding
echo "client_encoding = utf8" | sudo tee -a "$PG_CONF"

# Restart so that all new config is loaded
sudo service postgresql restart

# Create and configure DB
sudo su postgres -c "psql -c \"CREATE DATABASE ${APP_DB_NAME}\" "
sudo su postgres -c "psql -c \"CREATE USER ${APP_DB_USER} WITH PASSWORD '${APP_DB_PASS}'\" "
sudo su postgres -c "psql -c \"ALTER ROLE ${APP_DB_USER} SET client_encoding TO 'utf8'\" "
sudo su postgres -c "psql -c \"ALTER ROLE ${APP_DB_USER} SET default_transaction_isolation TO 'read committed'\" "
sudo su postgres -c "psql -c \"ALTER ROLE ${APP_DB_USER} SET timezone TO 'UTC'\" "
sudo su postgres -c "psql -c \"GRANT ALL PRIVILEGES ON DATABASE ${APP_DB_NAME} TO ${APP_DB_USER}\" "
