#!/usr/bin/python3

import sys
import antigravity  # This module is a joke and	opens a web browser to a comic


def geo():
    if len(sys.argv) != 4:
        print('❗ Error: Exactly 3 arguments are required (latitude, longitude, datedow).')
        sys.exit(1)

    try:
        latitude = float(sys.argv[1])
    except ValueError:
        print('❗ Error: Latitude must be a float.')
        print('💥 Usage: python3 geohashing.py 43.1496 -2.7207 2024-09-01-2041')
        sys.exit(1)

    try:
        longitude = float(sys.argv[2])
    except ValueError:
        print('❗ Error: Longitude must be a float.')
        print('💥 Usage: python3 geohashing.py 43.1496 -2.7207 2024-09-01-2041')
        sys.exit(1)

    try:
        datedow = sys.argv[3]
    except ValueError:
        print('❗ Error: date must be a string.')
        print('💥 Usage: python3 geohashing.py 43.1496 -2.7207 2024-09-01-2041')
        sys.exit(1)

    # Validate datedow format
    if len(datedow.split('-')) != 4:
        print('❗ Error: datedow must be in the format YYYY-MM-DD-xxxx')
        sys.exit(1)

    # Encode the string before passing to antigravity.geohash
    encoded_datedow = datedow.encode('utf-8')

    # Call the geohash function from antigravity
    try:
        antigravity.geohash(latitude=latitude, longitude=longitude, datedow=encoded_datedow)
    except Exception as e:
        print(f'Error: {e}')
        sys.exit(1)




if __name__ == '__main__':
    geo()
