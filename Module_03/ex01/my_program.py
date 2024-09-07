#!/usr/bin/python3

import os
from path import Path


def copy_lines(source_file, destination_file):
    try:
        source_file = os.path.expanduser(source_file)
        print(f'✨ Attempting to read from: {source_file}')
        with open(source_file, 'r') as src:
            lines = src.readlines()

        if len(lines) == 0:
            print(f'💥 No content found in {source_file}.')
            return
        else:
            print(f'✅ Read {len(lines)} lines from {source_file}')
    
    except FileNotFoundError:
        print(f'❌ Error: {source_file} not found.')
        return
    except Exception as e:
        print(f'❌ An error occurred while reading {source_file}: {e}')
        return

    try:
        print(f'✨ Writing content to {destination_file}')
        with open(destination_file, 'w') as dest:
            dest.writelines(lines[:])
        print(f'✅ Successfully wrote to {destination_file}')
    
    except Exception as e:
        print(f'❌ An error occurred while writing to {destination_file}: {e}')
        return


def main():
    
    try:
        Path.makedirs('test_dir')
    except FileExistsError as e:
        print(f'❌ Directory already exists: {e}')
    except Exception as e:
        print(f'❌ An error occurred: {e}')
    
    destination_file = 'test_dir/test_file'
    
    try:
        Path.touch(destination_file)
    except Exception as e:
        print(f'❌ An error occurred: {e}')
    
    source_file = '~/sgoinfre/local_lib/lib/python3.12/site-packages/path/classes.py'

    try:
        copy_lines(source_file, destination_file)
        print(f'✅ Copied lines from {source_file} to {destination_file}')
    except Exception as e:
        print(f'❌ An error occurred during file operation: {e}')
    
    try:
        with open(destination_file, 'r') as dest:
            print(f'✨ Reading content from {destination_file}: \n')
            print(dest.read())
    except Exception as e:
        print(f'❌ An error occurred while reading {destination_file}: {e}')


if __name__ == '__main__':
    main()
