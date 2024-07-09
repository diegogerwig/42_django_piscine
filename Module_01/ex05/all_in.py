import sys


def normalize_args(arg_str):
    return [item.strip() for item in arg_str.split(',') if item.strip()]


def reverse_dict(initial_dictionary):
    return {v: k for k, v in initial_dictionary.items()}


def all_in(*argv):
    states = {
        "Oregon": "OR",
        "Alabama": "AL",
        "New Jersey": "NJ",
        "Colorado": "CO"
    }
    capital_cities = {
        "OR": "Salem",
        "AL": "Montgomery",
        "NJ": "Trenton",
        "CO": "Denver"
    }

    argument_str = normalize_args(sys.argv[1])

    rev_states = reverse_dict(states)
    rev_cities = reverse_dict(capital_cities)

    for item in argument_str:
        if item.title() in states:
            print("{0} is the capital of {1}".format(capital_cities[states[item.title()]], item.title()))
        elif item.title() in rev_cities:
            print("{0} is the capital of {1}".format(item.title(), rev_states[rev_cities[item.title()]]))
        else:
            print("{0} is neither a capital city nor a state".format(item))


def main():
    if len(sys.argv) == 2:
        all_in(sys.argv)


if __name__ == '__main__':
    main()
