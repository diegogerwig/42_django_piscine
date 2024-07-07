import sys


def print_state(city):
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
        "CO": "Denver",
    }
    state_found = False
	
    for city_key, city_value in capital_cities.items():
        if city == city_value:
            for state_key, state_value in states.items():
                if city_key == state_value:
                    print(state_key)
                    state_found = True
                    break
    if state_found == False:
        print("Unknown capital city")


if __name__ == "__main__":
    if len(sys.argv) == 2:
        print_state(sys.argv[1])
