from elements import (Html, Head, Body, Title, Meta, Img, Table, Th, Tr, Td, Ul, Ol, Li, H1, H2, P, Div, Span, Hr, Br)
from elem import Elem, Text


VALID_TAGS = {
    'Html', 'Head', 'Body', 'Title', 'Meta', 'Img', 'Table', 'Th', 'Tr', 'Td', 'Ul', 'Ol', 'Li', 'H1', 'H2', 'P', 'Div', 'Span', 'Hr', 'Br'
}


class Page:
    def __init__(self, elem):
        try:
            if elem not in VALID_TAGS:
                print("Warning: 'tag' is not a valid tag. Setting to default value.")
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
            content += "<!DOCTYPE html>\n"  # add doctype to html
        content += str(self.elem)
        return content

    def is_valid(self) -> bool:
        return self.__check(self.elem)

    def __check(self, elem: Elem) -> bool:
        if not self.__is_valid_element_type(elem):
            return False

        if isinstance(elem, Html):
            return self.__check_html(elem)

        if isinstance(elem, Head):  
            return self.__check_head(elem)

        if isinstance(elem, (Body, Div)):
            return self.__check_body_div(elem)

        if isinstance(elem, (Title, H1, H2, Li, Th, Td)):
            return self.__check_single_text_child(elem)

        if isinstance(elem, P):
            return self.__all_children_of_type(elem, Text)

        if isinstance(elem, Span):
            return self.__check_span(elem)

        if isinstance(elem, (Ul, Ol)):
            return self.__check_list(elem)

        if isinstance(elem, Tr):
            return self.__check_table_row(elem)

        if isinstance(elem, Table):
            return self.__all_children_of_type(elem, Tr)

        if isinstance(elem, (Text, Meta, Img, Hr, Br)):
            return True

        return False

    def __is_valid_element_type(self, elem: Elem) -> bool:  # check if elem is a valid element
        return isinstance(elem, (Html, Head, Body, Title, Meta, Img, Table, Th, Tr, Td,
                                 Ul, Ol, Li, H1, H2, P, Div, Span, Hr, Br, Text))  

    def __check_html(self, elem: Html) -> bool:  # html must have head and body
        return len(elem.content) == 2 and \
               isinstance(elem.content[0], Head) and isinstance(elem.content[1], Body) and \
               all(self.__check(el) for el in elem.content)

    def __check_head(self, elem: Head) -> bool:  # head must have only one title
        return [isinstance(el, Title) for el in elem.content].count(True) == 1 and \
               all(self.__check(el) for el in elem.content)

    def __check_body_div(self, elem: Elem) -> bool:  # body and div must only contain h1, h2, div, table, ul, ol, span, text
        return self.__all_children_of_type(elem, (H1, H2, Div, Table, Ul, Ol, Span, Text))

    def __check_single_text_child(self, elem: Elem) -> bool:  # title, h1, h2, li, th, td must have only one text child
        return len(elem.content) == 1 and isinstance(elem.content[0], Text)

    def __check_span(self, elem: Span) -> bool:  # span must only contain text and p
        return self.__all_children_of_type(elem, (Text, P)) and \
               all(self.__check(el) for el in elem.content)

    def __check_list(self, elem: Elem) -> bool:  # ul and ol must only contain li
        return len(elem.content) > 0 and \
               self.__all_children_of_type(elem, Li) and \
               all(self.__check(el) for el in elem.content)

    def __check_table_row(self, elem: Tr) -> bool:  # tr must only contain th and td, must be of the same type and must have content
        return len(elem.content) > 0 and \
               self.__all_children_of_type(elem, (Th, Td)) and \
               self.__all_same_type(elem.content)
    
    def __all_children_of_type(self, elem: Elem, types: tuple) -> bool:  # check if all children of elem are of type types
        return all(isinstance(child, types) for child in elem.content)

    def __all_same_type(self, elements: list) -> bool:  # check if all elements in a list are of the same type
        first_type = type(elements[0])
        return all(isinstance(el, first_type) for el in elements)

    def write_to_file(self, path: str) -> None:  # write the page to a file
        with open(path, "w") as f:
            f.write(self.__str__())
