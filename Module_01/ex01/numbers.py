def print_numbers(filename):
    try:
        with open(filename, "r") as file:
            content = file.read()
            numbers = content.replace(",", "\n").split()
            for number in numbers:
                print(number)
    except FileNotFoundError:
        print(f"❌ Error: The file '{filename}' was not found.")
    except Exception as e:
        print(f"❌ Error: {e}")


def main():
    print_numbers("numbers.txt")


if __name__ == "__main__":
    main()
