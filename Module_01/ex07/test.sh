#!/bin/bash

# Path to the Python script you want to execute
python_script='./periodic_table.py'

# Run the Python script
python3 "$python_script"

# Paths to the HTML and CSS files you want to move to the Downloads folder
html_file='./periodic_table.html'
css_file='./styles.css'

# Move the HTML and CSS files to the Downloads folder
cp "$html_file" ~/Downloads/
cp "$css_file" ~/Downloads/

# Get the base name of the HTML file after moving to Downloads
html_filename=$(basename "$html_file")

# Open the HTML file in Google Chrome
(xdg-open ~/Downloads/"$html_filename" &>/dev/null &)

# URL of the W3C validator
validator_url='https://validator.w3.org/nu/'

# HTML file you want to check
html_file_path=~/Downloads/"$html_filename"

# Perform the request to the validator using curl and save the response
response=$(curl -s -F "file=@$html_file_path;type=text/html" $validator_url)

# Check if the response contains errors
if echo "$response" | grep -q "class=\"error\"" ; then
    echo "❌ The HTML file <$html_filename> contains errors according to the W3C validator:"
    echo "$response" | grep -oP '(?<=<li class="error">).*?(?=</li>)' | sed 's/\&quot;/"/g'
else
    echo "✅ The HTML file <$html_filename> is valid according to the W3C validator."
fi

# Remove the HTML and CSS files from the current directory
rm -rf "$html_file"
rm -rf "$css_file"
