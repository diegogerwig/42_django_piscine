#!/bin/sh

project_name="d05"

# Change to the project directory.
cd "$project_name"


# Make migrations
echo "✅ Making migrations..."
python manage.py makemigrations


# Migrate the changes
python manage.py migrate
echo "✅ Changes migrated."


# Run the server
echo "✅ Running server..."
python manage.py runserver
