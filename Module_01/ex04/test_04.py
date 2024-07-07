import subprocess


def print_header(title):
    border = "*" * (len(title) + 10)
    print('\n')
    print(border)
    print(f"   🔨  {title}")
    print(border)


def test_script():
    print_header("Testing with valid city 'Salem'")
    subprocess.run(["python3", "state.py", "Salem"], check=True)

    print_header("Testing with invalid city 'denver'")
    subprocess.run(["python3", "state.py", "denver"], check=True)

    print_header("Testing with unknown city 'Bilbao'")
    subprocess.run(["python3", "state.py", "Bilbao"], check=True)

    print_header("Testing with empty string")
    subprocess.run(["python3", "state.py", ""], check=True)

    print_header("Testing without any arguments")
    subprocess.run(["python3", "state.py"], check=True)

    print_header("Testing multiple arguments: 'Salem', 'Denver'")
    subprocess.run(["python3", "state.py",
                    "Salem", "Denver"], check=True)


def main():
    test_script()


if __name__ == '__main__':
    main()
