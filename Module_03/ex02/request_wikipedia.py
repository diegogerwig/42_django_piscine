#!/usr/bin/python3

import requests
import json
import dewiki
import sys


def request_wiki(page: str) -> str:

    URL = 'https://en.wikipedia.org/w/api.php'

    PARAMS = {
        'action': 'parse',  # Parse the content of a page
        'page': page,  # The title of the page to retrieve
        'format': 'json', # The format of the response
        'prop': 'wikitext',  # The properties to get
        'redirects': 'true',  # Automatically resolve redirects
    }

    try:
        response = requests.get(url=URL, params=PARAMS)
        response.raise_for_status()  # Raises an HTTPError for bad responses
    except requests.HTTPError as e:
        raise Exception(f'❌ HTTP error occurred: {e}')
    except requests.RequestException as e:
        raise Exception(f'❌ Request error occurred: {e}')

    try:
        data = response.json()
    except Exception as e:
        raise Exception(f'❌ Error occurred while decoding the JSON response: {e}')

    if 'error' in data:
        raise Exception(f'❌ API error: {data['error']['info']}')

    return dewiki.from_string(data['parse']['wikitext']['*'])  # Parse the wikitext to plain text


def write_to_file(filename: str, content: str):

    try:
        with open(f'{filename}.wiki', 'w') as f:
            f.write(content)
        print(f'✅ Successfully written to {filename}.wiki')
    except IOError as e:
        raise Exception(f'❌ File writing error: {e}')


def main():
    
    if len(sys.argv) != 2:
        print('❗ Incorrect usage: Provide exactly one argument for the page title.')
        sys.exit(1)

    page = sys.argv[1]

    page_snake_case = page.replace(" ", "_")

    try:
        wiki_data = request_wiki(page)
        write_to_file(page_snake_case, wiki_data)
    except Exception as e:
        print(f'❌ Error: {e}')
        sys.exit(1)

    print(f'✨ Reading from file {page_snake_case}.wiki')
    with open(f'{page_snake_case}.wiki', 'r') as f:
        print(f.read())


if __name__ == '__main__':
    main()
