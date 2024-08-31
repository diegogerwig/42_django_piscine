from elements import (Html, Head, Body, Title, Meta, Img, Table, Th, Tr, Td, Ul, Ol, Li, H1, H2, P, Div, Span, Hr, Br)
from elem import Elem, Text

class Page:
    def __init__(self, elem: Elem) -> None:
        if not isinstance(elem, Elem):
            raise Elem.ValidationError()
        self.elem = elem

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
            return False

        if isinstance(elem, (Text, Meta)):
            return True

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

        return False

    def __is_valid_element_type(self, elem: Elem) -> bool:
        return isinstance(elem, (Html, Head, Body, Title, Meta, Img, Table, Th, Tr, Td,
                                 Ul, Ol, Li, H1, H2, P, Div, Span, Hr, Br, Text))

    def __check_html(self, elem: Html) -> bool:
        return len(elem.content) == 2 and \
               isinstance(elem.content[0], Head) and isinstance(elem.content[1], Body) and \
               all(self.__check(el) for el in elem.content)

    def __check_head(self, elem: Head) -> bool:
        return [isinstance(el, Title) for el in elem.content].count(True) == 1 and \
               all(self.__check(el) for el in elem.content)

    def __check_body_div(self, elem: Elem) -> bool:
        return self.__all_children_of_type(elem, (H1, H2, Div, Table, Ul, Ol, Span, Text))

    def __check_single_text_child(self, elem: Elem) -> bool:
        return len(elem.content) == 1 and isinstance(elem.content[0], Text)

    def __check_span(self, elem: Span) -> bool:
        return self.__all_children_of_type(elem, (Text, P)) and \
               all(self.__check(el) for el in elem.content)

    def __check_list(self, elem: Elem) -> bool:
        return len(elem.content) > 0 and \
               self.__all_children_of_type(elem, Li) and \
               all(self.__check(el) for el in elem.content)

    def __check_table_row(self, elem: Tr) -> bool:
        return len(elem.content) > 0 and \
               self.__all_children_of_type(elem, (Th, Td)) and \
               self.__all_same_type(elem.content)

    def __all_children_of_type(self, elem: Elem, types: tuple) -> bool:
        return all(isinstance(child, types) for child in elem.content)

    def __all_same_type(self, elements: list) -> bool:
        first_type = type(elements[0])
        return all(isinstance(el, first_type) for el in elements)

    def write_to_file(self, path: str) -> None:
        with open(path, "w") as f:
            f.write(self.__str__())
