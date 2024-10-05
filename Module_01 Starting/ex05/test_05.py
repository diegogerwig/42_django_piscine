import subprocess


def print_header(title):
    border = '*' * (len(title) + 10)
    print('\n')
    print(border)
    print(f'   🔨  {title}')
    print(border)


def test_script():
    print_header('Testing with subject params: New jersey, Tren ton, NewJersey, Trenton, toto,    ,      sAlem')
    subprocess.run(['python3', 'all_in.py',
                    'New jersey, Tren ton, NewJersey, Trenton, toto,    ,      sAlem'],
                   check=True)

    print_header('Testing with invalid city: denver')
    subprocess.run(['python3', 'all_in.py', 'denver'], check=True)

    print_header('Testing with unknown city: Bilbao')
    subprocess.run(['python3', 'all_in.py', 'Bilbao'], check=True)

    print_header('Testing with empty string')
    subprocess.run(['python3', 'all_in.py', ''], check=True)

    print_header('Testing without any arguments')
    subprocess.run(['python3', 'all_in.py'], check=True)

    print_header('Testing multiple arguments: Salem, salem')
    subprocess.run(['python3', 'all_in.py',
                    'Salem', 'salem'], check=True)

    print_header('Running unit_test.py')
    subprocess.run(['python3', 'unit_test.py'], check=True)


def main():
    test_script()


if __name__ == '__main__':
    main()
