#!/bin/sh

project_name="d07"
settings_file="$project_name/$project_name/settings.py"


# Create a Django project
django-admin startproject "$project_name" 
echo -e "✅ $project_name PROJECT created."


# Change the timezone to Europe/Madrid in the settings.py file of the project.
sed -i "s/'UTC'/'Europe\/Madrid'/" "$settings_file"
echo "✅ Timezone changed to Europe/Madrid in $settings_file."


echo -e "\n**********************\n"
