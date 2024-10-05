#!/bin/bash

echo -e '\n🧹 Cleaning repository and localhost cache...'

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

# Clean Django cache
echo "🟢 Cleaning Django cache..."
python manage.py clearcache

# Clean Brave localhost cache
echo "🟢 Cleaning Brave localhost cache..."
brave_cache_dir="$HOME/.config/BraveSoftware/Brave-Browser/Default/Cache"
if [ -d "$brave_cache_dir" ]; then
    find "$brave_cache_dir" -type f -name "*localhost*" -delete
    echo "   Brave localhost cache removed."
else
    echo "   Brave cache directory not found."
fi

echo -e '🗑️  Repository and localhost cache cleaned.\n'