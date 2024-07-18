import os
import sys

EXTENSION = ".template"
SETTINGS_FILENAME = "settings.py"


def read_file(file_path):
    try:
        with open(file_path) as file:
            file_str = file.read()
    except FileNotFoundError as e:
        print(f'{file_path} nout found.')
        sys.exit(1)
    except PermissionError as e:
        print(f'No permission for reading file {file_path}')
        sys.exit(1)
    except IsADirectoryError as e:
        print(f'{file_path} is a directory')
        sys.exit(1)
    except Exception as e:
        print(e)
        sys.exit(1)
    return file_str

def settings(file_path):
    param_dict = {}
    file_str = read_file(file_path)
    lines = file_str.split('\n')
    lines = [line for line in lines if line]
    for line in lines:
        key, value = line.split('=')
        param_dict[(key.strip(' '))] = value.strip("\" \n")
    return param_dict


def render(file_name, param_dict):
    file_str = read_file(file_name + EXTENSION)
    file_str = file_str.split('\n')

    with open(file_name + '.html', 'w') as f:
        for line in file_str:
            for key in param_dict:
                line = line.replace("{" + key + "}", param_dict[key])
            f.write("".join((line, "\n")))


def main():
    if (len(sys.argv)) == 2:
        file_path = sys.argv[1]
        file_name, file_extension = os.path.splitext(file_path)
        if file_extension == EXTENSION:
            param_dict = settings(SETTINGS_FILENAME)
            render(file_name, param_dict)
        else:
            print(f"File extension error: it should be {EXTENSION}")
    else:
        print(f"Usage: python {sys.argv[0]} file.template")


if __name__ == "__main__":
    main()
