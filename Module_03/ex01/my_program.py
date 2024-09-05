#!/usr/bin/python3

from path import Path


def generate_loading_bar(steps, length=20):
    loading_lines = []
    for i in range(steps + 1):
        # Calculate the number of '#' to display as progress and '-' for the remaining bar
        progress = int((i / steps) * length)
        bar = f"[{'#' * progress}{'-' * (length - progress)}] {int((i / steps) * 100)}%"
        loading_lines.append(bar)
    
    return loading_lines


def main():
    
    # Create directory if it doesn't exist
    try:
        Path.makedirs('test_dir')
    except FileExistsError as e:
        print(f"Directory already exists: {e}")
    except Exception as e:
        print(f"An error occurred: {e}")
    
    # Create or update the file
    try:
        Path.touch('test_dir/test_file')
        f = Path('test_dir/test_file')
    except Exception as e:
        print(f"An error occurred: {e}")
    
    # Generate a loading bar with 10 steps and write it to the file
    loading_bar = generate_loading_bar(10)
    f.write_lines(loading_bar)
    
    # Read and print the content of the file
    print(f.read_text())


if __name__ == '__main__':
    main()
