#!/bin/sh

project_name="d09"

# Change to the project directory.
cd "$project_name"


# Make migrations
echo "✅ Making migrations..."
python manage.py makemigrations


# Migrate the changes
python manage.py migrate
echo "✅ Changes migrated."


# Management the database
python manage.py create_user_statuses
echo "✅ Management running."


# Run the server
echo "✅ Running server..."
python manage.py runserver
