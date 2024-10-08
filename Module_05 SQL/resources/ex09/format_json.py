import json

# Open and read the original JSON file in one line
with open('ex09_initial_data.json', 'r') as file:
    json_data = file.read()

# Parse the JSON into a Python dictionary
parsed_json = json.loads(json_data)

# Format the JSON with indentation for better readability
formatted_json = json.dumps(parsed_json, indent=4)

# Save the formatted JSON into a new file
with open('ex09_initial_data_formatted.json', 'w') as outfile:
    outfile.write(formatted_json)

print("Formatted JSON saved to 'ex09_initial_data_formatted.json'")
