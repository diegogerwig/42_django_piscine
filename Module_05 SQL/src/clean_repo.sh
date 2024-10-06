#!/bin/bash

echo -e '\n🧹 Cleaning repository and localhost cache...'

# Clean Django cache
if [ -d "../d05" ]; then
    echo "🟢 The directory d05 exists. Cleaning Django cache..."
    python3 ./d05/manage.py clearcache
else
    echo "🔴 The directory d05 does not exist. Cannot clean Django cache."
fi

# Paths to remove
paths_to_remove=(
    # "~/sgoinfre/django_venv"
    "./d05"
)

# Clean specified paths
for path in "${paths_to_remove[@]}"; do
    expanded_path=$(eval echo $path)
    if [ -e "$expanded_path" ]; then
        echo "🟢 Removing: $expanded_path"
        rm -rf "$expanded_path"
    else
        echo "🔴 Path does not exist: $expanded_path"
    fi
done

echo -e '🧹 Cleaning complete!\n'
