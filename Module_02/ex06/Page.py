from elements import (Html, Head, Body, Title, Meta, Img, Table, Th, Tr, Td, Ul, Ol, Li, H1, H2, P, Div, Span, Hr, Br)
from elem import Elem, Text

# ALLOWED_TAGS = (Html, Head, Body, Title, Meta, Img, Table, Th, Tr, Td, Ul, Ol, Li, H1, H2, P, Div, Span, Hr, Br, Elem, Text)
# HTML_CONTENT = (Head, Body)
# HEAD_CONTENT = (Title)
# BODY_CONTENT = DIV_CONTENT = (H1, H2, Div, Table, Ul, Ol, Span, Text)
# TITLE_CONTENT = H1_CONTENT = H2_CONTENT = LI_CONTENT = TH_CONTENT = TD_CONTENT = P_CONTENT = (Text)
# SPAN_CONTENT = (Text, P)
# UL_CONTENT = OL_CONTENT = (Li)
# TR_CONTENT = (Th, Td)
# TABLE_CONTENT = (Tr)


# class Page:

#     def __init__(self, elem: Elem()) -> None:
#         if not isinstance(elem, (Elem, Text)):
#             raise Elem.ValidationError
#         self.elem = elem
#         self._error_msg = None

#     @property
#     def error_msg(self):
#         if self._error_msg:
#             return self._error_msg
#         else:
#             return "No errors"

#     @error_msg.setter
#     def error_msg(self, message):
#         if self._error_msg is None:
#             self._error_msg = message


#     def __str__(self):
#         result = ""
#         if isinstance(self.elem, Html):
#             result += "<!DOCTYPE html>\n"
#         result += str(self.elem)
#         return result

#     def write_to_file(self, path):
#         f = open(path, "w")
#         f.write(self.__str__())

#     def is_valid(self):
#         return self.__recursive_check(self.elem)

#     def subelem_check(self, elem, instance_list=None):
#         if instance_list:
#             #print(instance_list)
#             if (all(isinstance(e, instance_list) for e in elem.content)):
#                 return True
#             else:
#                 return False
#         elif (all(self.__recursive_check(e) for e in elem.content)):
#             return True
#         return False


#     def __recursive_check(self, elem):
#         # Valid tags
#         if not (isinstance(elem, ALLOWED_TAGS)):
#             return False

#         # Html
#         if isinstance(elem, Html):
#             if len(elem.content) == 2 and \
#                 isinstance(elem.content[0], Head) and isinstance(elem.content[1], Body):
#                 if self.subelem_check(elem):
#                     return True
#             else:
#                 self.error_msg = (f"{elem.tag} tag must strictly contain a Head, then a Body.")

#         # Head
#         elif isinstance(elem, Head): 
#             if [isinstance(e, Title) for e in elem.content].count(True) == 1:
#                 if self.subelem_check(elem):
#                     return True
#             else:
#                 self.error_msg = (f"{elem.tag} tag Head must only contain one Title and only one Title.")

#         # Body, Div
#         elif isinstance(elem, (Body, Div)):
#             if self.subelem_check(elem, BODY_CONTENT) and \
#                 self.subelem_check(elem):
#                 return True
#             else:
#                 self.error_msg = (f"{elem.tag} tag must only contain the following type of elements: " \
#                         "H1, H2, Div, Table, Ul, Ol, Span, or Text.")

#         # Title, H1, H2, Li, Th, Td
#         elif isinstance(elem, (Title, H1, H2, Li, Th, Td)):
#                 if len(elem.content) == 1 and isinstance(elem.content[0], Text):
#                     return True
#                 else:
#                     self.error_msg = (f"{elem.tag} tag must contain only one Text.")

#         # P
#         elif isinstance(elem, P):
#             if self.subelem_check(elem, P_CONTENT):
#                 return True
#             else:
#                 self.error_msg = (f"{elem.tag} tag must contain Text.")

#         # Span
#         elif isinstance(elem, Span):
#             if self.subelem_check(elem, SPAN_CONTENT) and \
#                 self.subelem_check(elem):
#                 return True
#             else:
#                 self.error_msg = (f"{elem.tag} tag must only contain Text or some P.")

#         # Ul, Ol
#         elif isinstance(elem, (Ul, Ol)):
#             if len(elem.content) > 0 and \
#                 self.subelem_check(elem, UL_CONTENT) and \
#                 self.subelem_check(elem):
#                     return True
#             else:
#                 self.error_msg = (f"{elem.tag} tag must contain at least one Li and only some Li.")

#         # Tr
#         elif isinstance(elem, Tr):
#             if self.is_valid_tr(elem):
#                 return True

#         # Table
#         elif isinstance(elem, Table):
#             if all(isinstance(e, Tr) for e in elem.content) and \
#                 self.subelem_check(elem):
#                     return True
#             else:
#                 self.error_msg = (f"{elem.tag} tag must only contain Tr and only some Tr.")
#         return False

#     def is_valid_tr(self, elem):
#         if not (len(elem.content) > 0 and \
#                 all(isinstance(e, (Th, Td)) for e in elem.content)):
#             self.error_msg = (f"{elem.tag} tag must contain at least one Th or Td and only some Th or Td. " \
#                     "The Th and the Td must be mutually exclusive.")
#             return False

#         th_elements = [e for e in elem.content if isinstance(e, Th)]
#         td_elements = [e for e in elem.content if isinstance(e, Td)]
        
#         if len(th_elements) > 0 and len(td_elements) > 0:
#             self.error_msg = (f"{elem.tag} tag must contain at least one Th or Td and only some Th or Td. " \
#                     "The Th and the Td must be mutually exclusive.")
#             return False
#         return True

class Page:
    def __init__(self, elem: Elem()) -> None:
        if not isinstance(elem, Elem):
            raise Elem.ValidationError()
        self.elem = elem

    def __str__(self) -> str:
        result = ""
        if isinstance(self.elem, Html):
            result += "<!DOCTYPE html>\n"
        result += str(self.elem)
        return result

    def write_to_file(self, path: str) -> None:
        f = open(path, "w")
        f.write(self.__str__())

    def is_valid(self) -> bool:
        return self.__recursive_check(self.elem)

    def __recursive_check(self, elem: Elem()) -> bool:
        if not (isinstance(elem, (Html, Head, Body, Title, Meta, Img, Table, Th, Tr, Td, Ul, Ol, Li,
                                  H1, H2, P, Div, Span, Hr, Br)) or type(elem) == Text):
            return False
        if type(elem) == Text or isinstance(elem, Meta):
            return True
        if isinstance(elem, Html) and len(elem.content) == 2 \
                and type(elem.content[0]) == Head and type(elem.content[1]) == Body:
            if (all(self.__recursive_check(el) for el in elem.content)):
                return True
        elif isinstance(elem, Head) and [isinstance(el, Title) for el in elem.content].count(True) == 1:
            if (all(self.__recursive_check(el) for el in elem.content)):
                return True
        elif isinstance(elem, (Body, Div)) and \
                all([isinstance(el, (H1, H2, Div, Table, Ul, Ol, Span)) or
                    type(el) == Text for el in elem.content]):
            if (all(self.__recursive_check(el) for el in elem.content)):
                return True
        elif isinstance(elem, (Title, H1, H2, Li, Th, Td)) and \
                len(elem.content) == 1 and type(elem.content[0]) == Text:
            return True
        elif isinstance(elem, P) and \
                all([isinstance(el, Text) for el in elem.content]):
            return True
        elif isinstance(elem, Span) and \
                all([isinstance(el, (Text, P)) for el in elem.content]):
            if (all(self.__recursive_check(el) for el in elem.content)):
                return True
        elif isinstance(elem, (Ul, Ol)) and len(elem.content) > 0 and \
                all([isinstance(el, Li) for el in elem.content]):
            if (all(self.__recursive_check(el) for el in elem.content)):
                return True
        elif isinstance(elem, Tr) and len(elem.content) > 0 and\
                all([isinstance(el, (Th, Td)) for el in elem.content]) and \
                all([type(el) == type(elem.content[0]) for el in elem.content]):
            return True
        elif isinstance(elem, Table) and \
                all([isinstance(el, Tr) for el in elem.content]):
            return True
        return False
