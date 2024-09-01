import subprocess

def run_script(args):
    """Run the geohashing script with specified arguments."""
    try:
        result = subprocess.run(['python3', 'geohashing.py'] + args, check=True, text=True)
        print(f"Command {' '.join(args)} executed successfully.")
    except subprocess.CalledProcessError as e:
        print(f"Command {' '.join(args)} failed with error code {e.returncode}.")
    except Exception as e:
        print(f"Command {' '.join(args)} failed with exception: {e}")

def main():
    # Test 1: Valid input
    print("\nRunning Test 1: Valid input")
    run_script(['48.8582', '2.2945', '2023-09-01-1254'])

    # Test 2: Invalid latitude
    print("\nRunning Test 2: Invalid latitude")
    run_script(['invalid_latitude', '2.2945', '2023-09-01-1254'])

    # Test 3: Invalid longitude
    print("\nRunning Test 3: Invalid longitude")
    run_script(['48.8582', 'invalid_longitude', '2023-09-01-1254'])

    # Test 4: Invalid date format
    print("\nRunning Test 4: Invalid date format")
    run_script(['48.8582', '2.2945', '2023-09-01'])

    # Test 5: Missing arguments
    print("\nRunning Test 5: Missing arguments")
    run_script(['48.8582', '2.2945'])

    # Test 6: Extra arguments
    print("\nRunning Test 6: Extra arguments")
    run_script(['48.8582', '2.2945', '2023-09-01-1254', 'extra_arg'])

if __name__ == '__main__':
    main()

