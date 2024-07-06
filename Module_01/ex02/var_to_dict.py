def convert_to_dict():
    # List of tuples containing musician names and their birth years
    d = [
        ("Hendrix", "1942"),
        ("Allman", "1946"),
        ("King", "1925"),
        ("Clapton", "1945"),
        ("Johnson", "1911"),
        ("Berry", "1926"),
        ("Vaughan", "1954"),
        ("Cooder", "1947"),
        ("Page", "1944"),
        ("Richards", "1943"),
        ("Hammett", "1962"),
        ("Cobain", "1967"),
        ("Garcia", "1942"),
        ("Beck", "1944"),
        ("Santana", "1947"),
        ("Ramone", "1948"),
        ("White", "1975"),
        ("Frusciante", "1970"),
        ("Thompson", "1949"),
        ("Burton", "1939"),
    ]

    # Create an empty dictionary to store the converted data
    to_dict = {}

    # Populate the dictionary where the key is the birth year
    # and the value is the musician name
    for value, key in d:
        to_dict[key] = value

    # Print the dictionary in the specified format
    # Note: Starting from Python 3.7, dictionaries preserve insertion order,
    # so iterating over to_dict.items() will print items in the order they
    # were inserted. However, this behavior is not guaranteed in earlier
    # versions of Python.
    for key, value in to_dict.items():
        print(f"{key} : {value}")


if __name__ == "__main__":
    convert_to_dict()
