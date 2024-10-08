import sys


def normalize_args(arg_str):
    # Split the input string by commas to create a list of items
    # Strip leading and trailing whitespace from each item
    # Only include items in the resulting list if they are not empty after stripping

    # Split the string by commas
    items = arg_str.split(',')
    
    # Strip whitespace from each item
    stripped_items = [item.strip() for item in items]
    
    # Filter out empty items
    non_empty_items = [item for item in stripped_items if item]
    
    # Return the resulting list
    return non_empty_items


def all_in(arg_str):
    states = {
        'Oregon': 'OR',
        'Alabama': 'AL',
        'New Jersey': 'NJ',
        'Colorado': 'CO'
    }
    capital_cities = {
        'OR': 'Salem',
        'AL': 'Montgomery',
        'NJ': 'Trenton',
        'CO': 'Denver'
    }

    argument_str = normalize_args(arg_str)

    for item in argument_str:
        # Convert the current item to title case to match the case of the dictionary keys
        item_title = item.title()

        if item_title in states:
            state_abbr = states[item_title]
            capital = capital_cities[state_abbr]
            print(f'{capital} is the capital of {item_title}')
        elif item_title in capital_cities.values():
            # Find the state abbreviation corresponding to the capital
            state_abbr = None
            for key, value in capital_cities.items():
                if value == item_title:
                    state_abbr = key
                    break
            # Find the state name corresponding to the state abbreviation
            state_name = None
            for key, value in states.items():
                if value == state_abbr:
                    state_name = key
                    break
            print(f'{item_title} is the capital of {state_name}')
        else:
            print(f'{item} is neither a capital city nor a state')


if __name__ == '__main__':
    if len(sys.argv) == 2:
        all_in(sys.argv[1])
