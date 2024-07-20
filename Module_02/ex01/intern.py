class Intern:
    def __init__(self, name="My name? I’m nobody, an intern, I have no name."):
        self.name = name

    def __str__(self):
        return self.name

    class Coffee:
        def __str__(self):
            return "This is the worst coffee you ever tasted."

    def work(self):
        raise Exception("I’m just an intern, I can’t do that...")

    def make_coffee(self):
        return self.Coffee()


def main():
    # Create intern instances
    intern1 = Intern()
    intern2 = Intern("Mark")

    # Print intern names
    print(intern1)  # Should print the default intern message
    print(intern2)  # Should print "Mark"

    # Test making coffee
    print(intern1.make_coffee())  # Should print the coffee message
    print(intern2.make_coffee())  # Should print the coffee message

    # Test the work method for intern1, which should raise an exception
    try:
        intern1.work()
    except Exception as e:
        print(e)  # Should print the exception message

    # Test the work method for intern2, which should also raise an exception
    try:
        intern2.work()
    except Exception as e:
        print(e)  # Should print the exception message

    intern3 = Intern("")
    print(intern3)  # Should print an empty string


if __name__ == "__main__":
    main()
