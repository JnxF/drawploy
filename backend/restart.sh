#!/bin/sh

export PROD_MODE="True"

echo "Checking updates..."
./env/bin/pip install -r requirements.txt
echo "Checking updates... Done!"
echo "Migrating DB..."
./env/bin/python manage.py migrate
echo "Migrating db... Done!"
echo "Collecting static..."
./env/bin/python manage.py collectstatic --no-input
echo "Collecting static... Done!"
echo "Removing all pyc..."
find . -name \*.pyc -delete
echo "Removing all pyc... Done!"
echo "Deploy completed."
