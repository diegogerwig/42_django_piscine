#!/bin/bash

echo -e '\n🧹 Cleaning repository...'

paths_to_remove=(
    # "~/sgoinfre/django_venv"
    "./d05"
)

for path in "${paths_to_remove[@]}"; do
    expanded_path=$(eval echo $path)
    if [ -e "$expanded_path" ]; then
        echo "🟢 Removing: $expanded_path"
        rm -rf "$expanded_path"
    else
        echo "🔴 Path does not exist: $expanded_path"
    fi
done

echo -e '🗑️  Cleaned repository.\n'