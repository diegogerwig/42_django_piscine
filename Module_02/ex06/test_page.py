import sys

from elements import (Html, Head, Body, Title, Meta, Img, Table, Th, Tr, Td, Ul, Ol, Li, H1, H2, P, Div, Span, Hr, Br)
from elem import Elem, Text
from Page import Page


GREEN = "\033[92m"
RED = "\033[91m"
CYAN = "\033[96m"
YELLOW = "\033[93m"
MAGENTA = "\033[95m"
BOLD = "\033[1m"
BLINK = "\033[5m"
RESET = "\033[0m"

success_count = 0
failure_count = 0

failed_tests = []

try:
    TARGET = Page(
        Html([
            Head([
                Title(Text("💫 Testing html_file")),
                Meta(attr={"charset": "UTF-8"}),
                Meta(attr={"name": "description", "content": "This is a test page for hello world."}),
                Meta(attr={"name": "author", "content": "dgerwig"})
            ]),
            Body([  # Body and Div must only contain the following type of elements: H1, H2, Div, Table, Ul, Ol, Span, Text
                H1(Text("🌍 Hello World!")),
                H2(Text("🌎 Goodbye World!")),
                Div([Text("This is a div with "), H2(Text("a header inside."))]),
                Table([
                    Tr([
                        Th(Text("Header 1")),
                        Th(Text("Header 2")),
                        Th(Text("Header 3")),
                    ]),
                    Tr([
                        Td(Text("Data 1")),
                        Td(Text("Data 2")),
                        Td(Text("Data 3"))
                    ]),
                    Tr([
                        Td(Text("Data 4")),
                        Td(Text("Data 5")),
                        Td(Text("Data 6"))
                    ])
                ]),
                Ul([
                    Li(Text("First item")),
                    Li(Text("Second item")),
                    Li(Text("Third item"))
                ]),
                Ol([
                    Li(Text("First item")),
                    Li(Text("Second item")),
                    Li(Text("Third item"))
                ]),
                Span([
                    Text("This is a span ")
                ]),
            ])
        ])
    )
except Exception as e:
    print(f"❌ An unexpected error occurred: {e}")
    sys.exit(1)

def print_simple_header(title: str):
    print(f"\n{CYAN}{'='*34}{RESET}")
    print(f"{CYAN}{title}{RESET}")
    print(f"{CYAN}{'='*34}{RESET}")

def print_test_result(test_name: str, target: Page, expected: bool):
    global success_count, failure_count, failed_tests
    is_valid = target.is_valid()

    print(f"\nTags to test: {YELLOW} \n{target} {RESET}")

    # validation_result = "True" if is_valid else "False"
    print(f"HTML Rules -> \t{MAGENTA}{expected}{RESET}")

    print(f"Page Class -> \t{MAGENTA}{is_valid}{RESET}")

    result = GREEN + "\t\tSUCCESS" if is_valid == expected else RED + "\t\tFAILURE"
    print(f"{result}{RESET}")

    if is_valid == expected:
        success_count += 1
    else:
        failure_count += 1
        print(f"{RED}{BOLD}Test '{test_name}' Failed{RESET}")
        failed_tests.append(test_name)

def test_table():
    print_simple_header("table")
    test_cases = [
        (Page(Table()), True),
        (Page(Table([Tr()])), False),
        (Page(Table([Tr(Th())])), False),
        (Page(Table([Tr(Th(Text()))])), False),
        (Page(Table([Tr(Th(Text("planet")))])), True),
        (Page(Table([H1(Text("Hello World!"))])), False),
        (TARGET, True)
    ]
    for target, expected in test_cases:
        print_test_result('test_table', target, expected)

def test_tr():
    print_simple_header("tr")
    test_cases = [
        (Page(Tr()), False),
        (Page(Tr([Th(Text("title"))]*5)), True),
        (Page(Tr([Td(Text("content"))]*6)), True),
        (Page(Tr([Th(Text("title")), Td(Text("content"))])), False),
        (TARGET, True)
    ]
    for target, expected in test_cases:
        print_test_result('test_tr', target, expected)

def test_list():
    print_simple_header("ul & ol")
    test_cases = [
        (Page(Ul()), False),
        (Page(Ol()), False),
        (Page(Ul([Li(Text('test'))])), True),
        (Page(Ol([Li(Text('test'))])), True),
        (Page(Ul([Li(Text('test'))]*2)), True),
        (Page(Ol([Li(Text('test'))]*2)), True),
        (Page(Ul([Li(Text('test')), H1(Text('test'))])), False),
        (Page(Ol([Li(Text('test')), H1(Text('test'))])), False),
        (TARGET, True)
    ]
    for target, expected in test_cases:
        print_test_result('test_list', target, expected)

def test_span():
    print_simple_header("span")
    test_cases = [
        (Page(Span()), True),  # Span with no children should be valid
        (Page(Span([Text("Hello"), P(Text("World"))])), True),  # Span with Text and P is valid
        (Page(Span([H1(Text("World"))])), False),  # Span should not contain H1
        (TARGET, True)  # Replace TARGET with your actual Page instance to test
    ]
    
    for idx, (target, expected) in enumerate(test_cases):
        test_name = f"test_span"
        print_test_result(test_name, target, expected)

def test_p():
    print_simple_header("p")
    test_cases = [
        (Page(P()), True),
        (Page(P([Text("Hello?")])), True),
        (Page(P([H1(Text("World!"))])), False),
        (TARGET, True)
    ]
    for target, expected in test_cases:
        print_test_result('test_p', target, expected)

def test_text():
    print_simple_header("title & h1 & h2 & li & th & td")
    for element in [H1, H2, Li, Th, Td]:
        test_cases = [
            (Page(element()), False),
            (Page(element([Text("Hello?")])), True),
            (Page(element([H1(Text("World!"))])), False),
            (Page(element([Text("Hello?")] * 2)), False),
            (TARGET, True)
        ]
        for target, expected in test_cases:
            print_test_result('test_text', target, expected)

def test_body():
    print_simple_header("body & div")
    for element in [Body, Div]:
        test_cases = [
            (Page(element()), True),
            (Page(element([Text("Hello?")])), True),
            (Page(element([H1(Text("World!"))])), True),
            (Page(element([Text("Hello?"), Span()])), True),
            (Page(Html([element()])), False),
            (TARGET, True)
        ]
        for target, expected in test_cases:
            print_test_result('test_body', target, expected)

def test_title():
    print_simple_header("title")
    test_cases = [
        (Page(Title()), False),      
        (Page(Title(Text("Hello"))), True),      
        (Page(Title([Title(Text("Hello?"))])), False),
        (Page(Title([Title(Text("Hello?")), Title(Text("Hello?"))])), False),
        (TARGET, True)
    ]
    for target, expected in test_cases:
        print_test_result('test_title', target, expected)

def test_html():
    print_simple_header("html")
    test_cases = [
        (Page(Html()), False),
        (Page(Html([Head([Title(Text("Hello?"))]), Body([H1(Text("Hello!"))])])), True),
        (Page(Html(Div())), False),
        (TARGET, True)
    ]
    for target, expected in test_cases:
        print_test_result('test_html', target, expected)

def test_elem():
    print_test_result('test_elem', Page(Elem()), False)

def write_to_file():
    print_simple_header("write_to_file")

    target = TARGET

    path = "test_file.html"
    
    print_test_result('write_to_file', target, True)
    
    if target.is_valid():
        target.write_to_file(path)
        print(f"File written to: {GREEN}{path}{RESET}")
    else:
        print(f"{RED}File not written due to validation failure{RESET}")

def print_global_summary():
    print_simple_header("GLOBAL TEST SUMMARY")
    print(f"Total SUCCESS: {GREEN}{success_count}{RESET}")
    print(f"Total FAILURE: {RED}{failure_count}{RESET}")

    if failure_count > 0:
        print(f"{RED}Failed Tests:{RESET}")
        for test_name in failed_tests:
            print(f"- {RED}{test_name}{RESET}")
    else:
        print(f"\n{GREEN}{BOLD}{BLINK}⭐ ⭐ ⭐ ⭐ ⭐   All tests passed!  ⭐ ⭐ ⭐ ⭐ ⭐{RESET}\n")


def test():
    global success_count, failure_count

    test_table()
    test_tr()
    test_list()
    test_span()
    test_p()
    test_text()
    test_body()
    test_title()
    test_html()
    test_elem()

    write_to_file()

    print_global_summary()

if __name__ == '__main__':
    test()
