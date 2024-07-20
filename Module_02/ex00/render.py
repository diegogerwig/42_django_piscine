import os
import sys

EXTENSION = ".template"
SETTINGS_FILENAME = "settings.py"


def read_file(file_path):
    try:
        with open(file_path, 'r') as file:
            return file.read()
    except FileNotFoundError:
        print(f'❌ {file_path} not found.')
    except PermissionError:
        print(f'❌ No permission to read file {file_path}')
    except Exception as e:
        print(f'❌ Error reading file {file_path}: {e}')
    sys.exit(1)


def parse_settings(file_path):
    settings_dict = {}
    file_str = read_file(file_path)
    lines = file_str.splitlines()

    for line in lines:
        if '=' in line:
            key, value = line.split('=', 1)
            settings_dict[key.strip()] = value.strip().strip('"')

    return settings_dict


def render_template(file_name, params):
    template_str = read_file(file_name + EXTENSION)
    for key, value in params.items():
        template_str = template_str.replace(f"{{{key}}}", value)

    output_path = file_name + '.html'
    with open(output_path, 'w') as f:
        f.write(template_str)

    return output_path


def main():
    if len(sys.argv) != 2:
        print(f"💥 Usage: python {os.path.basename(sys.argv[0])} file{EXTENSION}")
        sys.exit(1)

    file_path = sys.argv[1]
    file_name, file_extension = os.path.splitext(file_path)

    if file_extension != EXTENSION:
        print(f"❌ File extension error: it should be {EXTENSION}")
        sys.exit(1)

    params = parse_settings(SETTINGS_FILENAME)
    output_path = render_template(file_name, params)
    print(f"✅ File <{output_path}> has been created.")


if __name__ == "__main__":
    main()
