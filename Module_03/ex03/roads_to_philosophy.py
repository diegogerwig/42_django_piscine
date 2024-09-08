#!/usr/bin/env python3

import sys
import requests
from bs4 import BeautifulSoup as bs

has_written = False


def write_output(soup):
    global has_written
    if not has_written:
        html_lines = str(soup).splitlines()
        with open('output.txt', 'w', encoding='utf-8') as file:
            for line in html_lines:
                file.write(line + '\n')
        has_written = True


def export_links_to_file(all_links):
    with open('links.txt', 'a', encoding='utf-8') as file:
        file.write('\n' + '-' * 40 + '\n')
        for link in all_links:
            href = link.get('href')
            if href:
                file.write(href + '\n')


def is_valid_link(href):
    if not href:  # If the link is None
        return False

    if not href.startswith('/wiki/'):  # If the link is not a Wikipedia link
        return False

    if href.startswith('/wiki/Wikipedia:') or href.startswith('/wiki/Help:'):  # If the link is a Wikipedia help page
        return False

    return True


def process_links(all_links, visited):
    for link in all_links:
        href = link.get('href')
        if is_valid_link(href):
            wiki_road(href, visited)
            sys.exit(0)


def wiki_road(path: str, visited=None) -> None:
    if visited is None:
        visited = []

    title = path.split('/')[-1]

    URL = f'https://en.wikipedia.org{path}'

    try:
        response = requests.get(URL)
        response.raise_for_status()
    except requests.HTTPError as e:
        if response.status_code == 404:
            print(f'💀 It leads to a dead end! -> {title}')
        else:
            print(f'❌ HTTP Error: {e}')
        sys.exit(1)

    soup = bs(response.text, 'html.parser')
    title = soup.find(id='firstHeading').text  # Get the title from the page

    write_output(soup)

    if title in visited:
        print(f'🎆 It leads to an infinite loop! -> {title}')
        sys.exit(0)

    visited.append(title)
    print(f'{len(visited)} -> {title}')

    if title == 'Philosophy':
        print(f'✅ {len(visited)} roads from {visited[0]} to Philosophy')
        sys.exit(0)

    content = soup.find(id='mw-content-text')  # Get the content of the page
    all_links = content.select('p > a')  # Select all a tags that are direct children of p tags. Not including cites.
    export_links_to_file(all_links)

    process_links(all_links, visited)

    print(f'💀 It leads to a dead end! -> {title}')


def main():
    if len(sys.argv) != 2:
        print('❗ Usage: python script.py <title>')
        return

    title = sys.argv[1]
    wiki_path = f'/wiki/{title}'
    wiki_road(wiki_path)


if __name__ == '__main__':
    main()
