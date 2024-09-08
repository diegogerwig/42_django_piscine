#!/usr/bin/env python3

import sys
import requests
from bs4 import BeautifulSoup as bs


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
        return

    soup = bs(response.text, 'html.parser')
    title = soup.find(id='firstHeading').text

    if title in visited:
        print(f'🎆 It leads to an infinite loop! -> {title}')
        return

    visited.append(title)
    print(f'{len(visited)} -> {title}')

    if title == 'Philosophy':
        print(f'✅ {len(visited)} roads from {visited[0]} to Philosophy')
        return

    content = soup.find(id='mw-content-text')
    all_links = content.select('p > a')
    for link in all_links:
        href = link.get('href')
        if href and href.startswith('/wiki/') and not href.startswith('/wiki/Wikipedia:') and not href.startswith('/wiki/Help:'):
            wiki_road(href, visited)
            return

    print(f'💀 It leads to a dead end! -> {title}')


def main():
    if len(sys.argv) != 2:
        print('❗ Usage: python script.py <title>')
        return

    title = sys.argv[1]  
    wiki_road(f'/wiki/{title}')  


if __name__ == '__main__':
    main()
