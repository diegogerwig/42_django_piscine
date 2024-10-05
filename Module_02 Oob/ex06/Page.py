from elements import (Html, Head, Body, Title, Meta, Img, Table, Th, Tr, Td, Ul, Ol, Li, H1, H2, P, Div, Span, Hr, Br)
from elem import Elem, Text

class Page:
    def __init__(self, elem):
        try:
            if not isinstance(elem, Elem):
                print("Warning: 'elem' is not an instance of Elem. Setting to default value.")
                self.elem = Elem()
            else:
                self.elem = elem
        except Exception as e:
            print(f"An unexpected error occurred: {e}")

    def __str__(self) -> str:  
        content = ""
        if isinstance(self.elem, Html):
            content += "<!DOCTYPE html>\n"
        content += str(self.elem)
        return content

    def is_valid(self) -> bool:
        return self.__check(self.elem)

    def __check(self, elem: Elem) -> bool:
        if not self.__is_valid_element_type(elem):
            print(f"Error: Invalid element type '{type(elem).__name__}' encountered.")
            return False

        if isinstance(elem, Html):
            return self.__check_html(elem)
        elif isinstance(elem, Head):
            return self.__check_head(elem)
        elif isinstance(elem, (Body, Div)):
            return self.__check_body_div(elem)
        elif isinstance(elem, (Title, H1, H2, Li, Th, Td)):
            return self.__check_single_text_child(elem)
        elif isinstance(elem, P):
            return self.__all_children_of_type(elem, Text)
        elif isinstance(elem, Span):
            return self.__check_span(elem)
        elif isinstance(elem, (Ul, Ol)):
            return self.__check_list(elem)
        elif isinstance(elem, Tr):
            return self.__check_table_row(elem)
        elif isinstance(elem, Table):
            return self.__check_table(elem)
        elif isinstance(elem, (Meta, Img, Hr, Br, Text)):
            return True

        # Check childrem of elem recursively
        return all(self.__check(child) for child in elem.content)

    def __is_valid_element_type(self, elem: Elem) -> bool:
        """Check if elem is a valid element."""
        return isinstance(elem, (Html, Head, Body, Title, Meta, Img, Table, Th, Tr, Td,
                                 Ul, Ol, Li, H1, H2, P, Div, Span, Hr, Br, Text))

    def __check_html(self, elem: Html) -> bool:
        """Html must have head and body, and their children must be valid."""
        if len(elem.content) != 2:
            print("Error: Html must contain exactly two children (Head and Body).")
            return False
        head, body = elem.content
        if not isinstance(head, Head) or not isinstance(body, Body):
            print("Error: Html's children must be Head and Body.")
            return False
        return self.__check(head) and self.__check(body)

    def __check_head(self, elem: Head) -> bool:
        """Head must have only one title, and its children must be valid."""
        valid_types = (Title)
        if not self.__all_children_of_type(elem, valid_types):
            print("Error: Head contains invalid child elements.")
            return False
        title_count = sum(isinstance(el, Title) for el in elem.content)
        if title_count != 1:
            print(f"Error: Head must contain exactly one Title. Found {title_count}.")
            return False
        return all(self.__check(el) for el in elem.content)

    def __check_body_div(self, elem: Elem) -> bool:
        """Body and Div must only contain h1, h2, div, table, ul, ol, span, text."""
        valid_types = (H1, H2, Div, Table, Ul, Ol, Span, Text)
        if not self.__all_children_of_type(elem, valid_types):
            print(f"Error: Body/Div contains invalid child elements.")
            return False
        return all(self.__check(el) for el in elem.content)

    def __check_single_text_child(self, elem: Elem) -> bool:
        """Title, h1, h2, li, th, td must have only one text child."""
        if len(elem.content) != 1 or not isinstance(elem.content[0], Text):
            print(f"Error: {type(elem).__name__} must contain exactly one Text child.")
            return False
        return True

    def __check_span(self, elem: Span) -> bool:
        """Span must only contain text and p."""
        if not self.__all_children_of_type(elem, (Text, P)):
            print("Error: Span contains invalid child elements.")
            return False
        return all(self.__check(el) for el in elem.content)

    def __check_list(self, elem: Elem) -> bool:
        """Ul and Ol must only contain li, and their children must be valid."""
        if len(elem.content) == 0 or not self.__all_children_of_type(elem, Li):
            print(f"Error: {type(elem).__name__} must contain only Li elements.")
            return False
        return all(self.__check(el) for el in elem.content)

    def __check_table(self, elem: Table) -> bool:
        """Table must only contain tr, and its children must be valid."""
        if not self.__all_children_of_type(elem, Tr):
            print("Error: Table must contain only Tr elements.")
            return False
        return all(self.__check(el) for el in elem.content)

    def __check_table_row(self, elem: Tr) -> bool:
        """Tr must only contain Th and Td, and all children must be of the same type."""
        if len(elem.content) == 0:
            print("Error: Tr element has no children.")
            return False
        if not self.__all_children_of_type(elem, (Th, Td)):
            print(f"Error: Invalid child element found in Tr.")
            return False
        if not self.__all_same_type(elem.content):
            print("Error: Not all children of Tr are of the same type.")
            return False
        return all(self.__check(child) for child in elem.content)

    def __all_children_of_type(self, elem: Elem, types: tuple) -> bool:
        """Check if all children of elem are of type types."""
        return all(isinstance(child, types) for child in elem.content)

    def __all_same_type(self, elements: list) -> bool:
        """Check if all elements in a list are of the same type."""
        if not elements:
            return True
        first_type = type(elements[0])
        return all(isinstance(el, first_type) for el in elements)

    def write_to_file(self, path: str) -> None:
        """Write the page to a file."""
        with open(path, "w") as f:
            f.write(self.__str__())
