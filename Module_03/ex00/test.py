#!/usr/bin/python3

import subprocess


def run_script(args):
    try:
        result = subprocess.run(['python3', 'geohashing.py'] + args, check=True, text=True)
        print(f"Command {' '.join(args)} executed successfully.")
    except subprocess.CalledProcessError as e:
        print(f"Command {' '.join(args)} failed with error code {e.returncode}.")
    except Exception as e:
        print(f"Command {' '.join(args)} failed with exception: {e}")


def main():
    # Test 1: Valid input
    print("\nTest 1: Valid input")
    run_script(['43.1496', '-2.7207', '2024-09-01-2041'])

    # Test 2: Invalid latitude
    print("\nTest 2: Invalid latitude")
    run_script(['invalid_latitude', '-2.7207', '2024-09-01-2041'])

    # Test 3: Invalid longitude
    print("\nTest 3: Invalid longitude")
    run_script(['43.1496', 'invalid_longitude', '2024-09-01-2041'])

    # Test 4: Invalid date format
    print("\nTest 4: Invalid date format")
    run_script(['43.1496', '-2.7207', '2024-09-01'])

    # Test 5: Missing arguments
    print("\nTest 5: Missing arguments")
    run_script(['43.1496', '-2.7207'])

    # Test 6: Extra arguments
    print("\nTest 6: Extra arguments")
    run_script(['43.1496', '-2.7207', '2024-09-01-2041', 'extra_arg'])


if __name__ == '__main__':
    main()
