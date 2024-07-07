import subprocess


def print_header(title):
    border = "*" * (len(title) + 10)
    print('\n')
    print(border)
    print(f"   🔨  {title}")
    print(border)


def test_print_capital():
    print_header("Testing with valid state 'Oregon'")
    subprocess.run(["python3", "capital_city.py", "Oregon"], check=True)

    print_header("Testing with valid state 'Alabama'")
    subprocess.run(["python3", "capital_city.py", "Alabama"], check=True)

    print_header("Testing with unknown state 'Bizkaia'")
    subprocess.run(["python3", "capital_city.py", "Bizkaia"], check=True)

    print_header("Testing with empty string")
    subprocess.run(["python3", "capital_city.py", ""], check=True)

    print_header("Testing without any arguments")
    subprocess.run(["python3", "capital_city.py"], check=True)

    print_header("Testing multiple arguments: 'Oregon', 'Alabama'")
    subprocess.run(["python3", "capital_city.py",
                    "Oregon", "Alabama"], check=True)


def main():
    test_print_capital()


if __name__ == '__main__':
    main()
