#!/bin/sh

project_name="d07"

# Change to the project directory.
cd "$project_name"


# Make migrations
echo "✅ Making migrations..."
python manage.py makemigrations


# Migrate the changes
python manage.py migrate
echo "✅ Changes migrated."


# Populate the database
python manage.py populate_db
echo "✅ Database populated."


# Run the server
echo "✅ Running server..."
python manage.py runserver
