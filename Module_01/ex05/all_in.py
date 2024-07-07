import sys


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

def print_capital_city(state, states=states, capital_cities=capital_cities):	
    states = {"Oregon": "OR", "Alabama": "AL", "New Jersey": "NJ", "Colorado": "CO"}
    capital_cities = {
        "OR": "Salem",
        "AL": "Montgomery",
        "NJ": "Trenton",
        "CO": "Denver",
    }
    found = False
    for item in states.keys():
        if state.lower() == item.lower():
            print(state, "is a state")
            found = True
            break
    if found == False:
        return False
    return True


def print_state(city):
    states = {"Oregon": "OR", "Alabama": "AL", "New Jersey": "NJ", "Colorado": "CO"}
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
                    print(city, "is the capital of", state_key)
                    state_found = True
                    break
    if state_found == False:
        return False
    return True


if __name__ == "__main__":
    if len(sys.argv) == 2:
        item_list = [item.strip() for item in sys.argv[1].split(",")]
        item_list = [item for item in item_list if item]
        for item in item_list:
            if not (print_state(item) or print_capital_city(item)):
                print(item, "is neither a capital city nor a state")
