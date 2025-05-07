#!/bin/bash

# Aplicar Migrações
echo "Applying database migrations..."
python3 manage.py migrate

# Seed da DB
#echo "Seeding the database..."
#python3 seed.py
# Agora vai passar a ser opcional !

# Start Django server
echo "Starting the server..."
python3 manage.py runserver 0.0.0.0:8000
