import sys

from elements import (Html, Head, Body, Title, Meta, Img, Table, Th, Tr, Td, Ul, Ol, Li, H1, H2, P, Div, Span, Hr, Br, Elem, Text)

from Page import Page


class TextColors:
    RED = '\033[31m'
    GREEN = '\033[32m'
    YELLOW = '\033[33m'
    BLUE = '\033[34m'
    MAGENTA = '\033[35m'
    CYAN = '\033[36m'
    WHITE = '\033[37m'
    RESET = '\033[0m'

def print_colored_text(text, color_code):
    if color_code.upper() in dir(TextColors):
        color = getattr(TextColors, color_code.upper())
        print(f"{color}{text}{TextColors.RESET}", file=sys.stdout)
    else:
        print(text)


class PageTester():
    def __init__(self, print_error_msg=False, print_code=False, write_path=None):
        self.print_error_msg = print_error_msg
        self.print_code = print_code
        self.write_path = write_path

    def test(self):
        self.__one_Text()
        self.__test_Html()
        self.__test_Head()
        self.__test_Body_Div()
        self.__test_P()
        self.__test_Span()
        self.__test_Ul_Ol()
        self.__test_Tr()
        self.__test_Table()

    def is_valid(self, page):
        print_colored_text(page.is_valid(), 'blue')
        if self.print_error_msg:
            print_colored_text(f" - {page.error_msg}", 'YELLOW')
        if self.print_code:
            print(page, "\n")
        if self.write_path:
            page.write_to_file(self.write_path)

    def __test_Html(self):
        print("\n{:=^42s}\n".format("Html"))
        page = Page(
                    Html([
                        Head()
                    ])
                )
        self.is_valid(page)
    
        page = Page(
                    Html([
                        Body(),
                    ])
                )
        self.is_valid(page)
    
        page = Page(
                    Html([
                        Body(),
                        Head(Title(Text("test"))),
                    ])
                )
        self.is_valid(page)
    
        page = Page(
                    Html([
                        Head(Title(Text("test"))),
                        Body(),
                    ])
                )
        self.is_valid(page)
    
    def __test_Head(self):
        print("\n{:=^42s}\n".format("Head"))
        page = Page(
                    Head(),
                )
        self.is_valid(page)
    
        page = Page(
                    Head(H1(Text("test"))),
                )
        self.is_valid(page)
    
        page = Page(
                    Head(Title(Text("test"))),
                )
        self.is_valid(page)
    
    def __test_Body_Div(self):
        print("\n{:=^42s}\n".format("Body Div"))
        page = Page(
                    Body(Title(Text("test"))),
                )
        self.is_valid(page)
        
    
        page = Page(
                    Body(H1(Text("test"))),
                )
        self.is_valid(page)
    
    def __test_Span(self):
        print("\n{:=^42s}\n".format("Span"))
        page = Page(
                    Span(Title(Text("test"))),
                )
        self.is_valid(page)
        
    
        page = Page(
                    Span(P(Text("test"))),
                )
        self.is_valid(page)
    
    def __test_Ul_Ol(self):
        print("\n{:=^42s}\n".format("Ul Ol"))
        page = Page(
                    Ul(Title(Text("test"))),
                )
        self.is_valid(page)
        
        page = Page(
                    Ol([
                        Li(Text("test")),
                        Ul(Text("test")),
                        ]),
                )
        self.is_valid(page)
    
        page = Page(
                    Ol(Li(Text("test"))),
                )
        self.is_valid(page)
    
    def __test_Tr(self):
        print("\n{:=^42s}\n".format("Tr"))
        page = Page(
                    Tr(Li(Text("test"))),
                )
        self.is_valid(page)
    
        page = Page(
                    Tr([
                        Td(Text("test")),
                        Th(Text("test")),
                        ]),
                )
        self.is_valid(page)
    
        page = Page(
                    Tr([
                        Td(Text("test")),
                        Td(Text("test")),
                        ]),
                )
        self.is_valid(page)
    
    def __test_Table(self):
        print("\n{:=^42s}\n".format("Table"))
        page = Page(
                    Table(Li(Text("test"))),
                )
        self.is_valid(page)
    
        page = Page(
                    Table([
                        Tr(Td(Text("test"))),
                        Td(Td(Text("test"))),
                        ]),
                )
        self.is_valid(page)
    
        page = Page(
                    Table([
                        Tr(Td(Text("test"))),
                        Tr(Td(Text("test"))),
                        ]),
                )
        self.is_valid(page)
    
    # Title_H1_H2_Li_Th_Td
    def __one_Text(self):
        print("\n{:=^42s}\n".format("Title H1 H2 Li Th Td"))
        elem = Html([
            Head(Title(Text('"Hello ground!"'))),
    				    Body([H1(),
                  ])])
        page = Page(elem)
        self.is_valid(page)
    
    def __test_P(self):
        print("\n{:=^42s}\n".format("P"))
        page = Page(
                    P([
                        Text('"again!"'), 
                        Text('"again!"'),
                    ])
                )
        self.is_valid(page)
    
        page = Page(
                    P()
                )
        self.is_valid(page)
    
        page = Page(
                    P(H2())
                )
        self.is_valid(page)


def main():
    tester = PageTester()
    tester.test()


if __name__ == '__main__':
    main()
