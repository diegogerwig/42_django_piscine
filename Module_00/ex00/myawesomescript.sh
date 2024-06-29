#!/bin/bash

# Function to process a URL and fetch its final redirect URL
process_url() {
  local url=$1

  # Prepend "https://" if the URL does not start with "https://"
  if [[ $url != https://* ]]; then
    url="https://$url"
  fi

  # Fetch headers of the URL and extract the value of the "Location" header if it exists
  # 	curl options:
  #   		-s: Silent mode
  #   		-I: Fetch headers only
  #   		-L: Follow redirects
  #   	grep -i "location:": Case-insensitive search for the "Location" header
  #   	tail -1: Get the last occurrence of the "Location" header
  #   	awk '{print $2}': Print the second column of the "Location" header
  redirect_url=$(curl -s -I -L $url | grep -i "location:" | tail -1 | awk '{print $2}')

  # Check if a redirect URL was found and print it
  if [ -n "$redirect_url" ]; then
    echo "🎯 Original URL: $url"
    echo "✅ Redirect URL: $redirect_url"
  else
    echo "🎯 Original URL: $url"
    echo "❌ No redirect URL found."
  fi
  echo
}

# Check if at least one URL argument is provided
if [ $# -eq 0 ]; then
  echo "❗ Usage: $0 <URL1> [URL2] [URL3] ..."
  echo
  exit 1
fi

# Loop through each URL provided as an argument
for url in "$@"; do
  process_url "$url"
done
