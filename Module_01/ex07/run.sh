#!/bin/bash

# Path to the Python script you want to execute
python_script="./periodic_table.py"

# Run the Python script
python3 "$python_script"

# Path to the HTML file you want to move to the Downloads folder
html_file="./periodic_table.html"
css_file="./styles.css"

# Move the HTML and CSS files to the Downloads folder
cp "$html_file" ~/Downloads/
cp "$css_file" ~/Downloads/

# Get the base name of the HTML file after moving to Downloads
html_filename=$(basename "$html_file")

# Open the HTML file in Google Chrome
xdg-open ~/Downloads/"$html_filename" &