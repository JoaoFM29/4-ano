#!/bin/bash

# Altera as variáveis no arquivo .env
sed -i "s/^DB_HOST=.*/DB_HOST=${DB_HOST}/" .env
sed -i "s/^DB_DATABASE=.*/DB_DATABASE=${DB_DATABASE}/" .env
sed -i "s/^DB_USERNAME=.*/DB_USERNAME=${DB_USER}/" .env
sed -i "s/^DB_PASSWORD=.*/DB_PASSWORD=${DB_PASSWORD}/" .env

# Executa as migrações e o servidor
php artisan migrate:fresh --force
php artisan db:seed --force
php artisan serve --host=0.0.0.0 --port=8000

