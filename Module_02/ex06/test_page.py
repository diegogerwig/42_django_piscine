from elements import (Html, Head, Body, Title, Meta, Img, Table, Th, Tr, Td, Ul, Ol, Li, H1, H2, P, Div, Span, Hr, Br)
from elem import Elem, Text
from Page import Page

# ANSI escape codes for colors
GREEN = "\033[92m"
RED = "\033[91m"
CYAN = "\033[96m"
YELLOW = "\033[93m"
BOLD = "\033[1m"
BLINK = "\033[5m"
RESET = "\033[0m"

# Global counters for test results
success_count = 0
failure_count = 0

def print_simple_header(title: str):
    print(f"\n{CYAN}{'='*34}{RESET}")
    print(f"{CYAN}{title}{RESET}")
    print(f"{CYAN}{'='*34}{RESET}")

def print_test_result(target: Page, expected: bool):
    global success_count, failure_count
    is_valid = target.is_valid()

    print(f"\nTags to test: {YELLOW} \n{target} {RESET}")

    validation_result = "VALID" if is_valid else "INVALID"
    print(f"Is valid or not: {YELLOW}{validation_result}{RESET}")
    
    result = GREEN + "SUCCESS" if is_valid == expected else RED + "FAILURE"
    print(f"{result}{RESET}")

    # Update global counters
    if is_valid == expected:
        success_count += 1
    else:
        failure_count += 1

def test_table():
    print_simple_header("table")
    test_cases = [
        (Page(Table()), True),
        (Page(Table([Tr()])), True),
        (Page(Table([H1(Text("Hello World!"))])), False)
    ]
    for target, expected in test_cases:
        print_test_result(target, expected)

def test_tr():
    print_simple_header("tr")
    test_cases = [
        (Page(Tr()), False),
        (Page(Tr([Th(Text("title"))]*5)), True),
        (Page(Tr([Td(Text("content"))]*6)), True),
        (Page(Tr([Th(Text("title")), Td(Text("content"))])), False)
    ]
    for target, expected in test_cases:
        print_test_result(target, expected)

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
        (Page(Ol([Li(Text('test')), H1(Text('test'))])), False)
    ]
    for target, expected in test_cases:
        print_test_result(target, expected)

def test_span():
    print_simple_header("span")
    test_cases = [
        (Page(Span()), True),
        (Page(Span([Text("Hello?"), P(Text("World!"))])), True),
        (Page(Span([H1(Text("World!"))])), False)
    ]
    for target, expected in test_cases:
        print_test_result(target, expected)

def test_p():
    print_simple_header("p")
    test_cases = [
        (Page(P()), True),
        (Page(P([Text("Hello?")])), True),
        (Page(P([H1(Text("World!"))])), False)
    ]
    for target, expected in test_cases:
        print_test_result(target, expected)

def test_text():
    print_simple_header("title & h1 & h2 & li & th & td")
    for element in [H1, H2, Li, Th, Td]:
        test_cases = [
            (Page(element()), False),
            (Page(element([Text("Hello?")])), True),
            (Page(element([H1(Text("World!"))])), False),
            (Page(element([Text("Hello?")] * 2)), False)
        ]
        for target, expected in test_cases:
            print_test_result(target, expected)

def test_body():
    print_simple_header("body & div")
    for element in [Body, Div]:
        test_cases = [
            (Page(element()), True),
            (Page(element([Text("Hello?")])), True),
            (Page(element([H1(Text("World!"))])), True),
            (Page(element([Text("Hello?"), Span()])), True),
            (Page(Html([element()])), False)
        ]
        for target, expected in test_cases:
            print_test_result(target, expected)

def test_title():
    print_simple_header("title")
    test_cases = [
        (Page(Title()), False),      
        (Page(Title(Text("Hello"))), True),      
        (Page(Title([Title(Text("Hello?"))])), False),
        (Page(Title([Title(Text("Hello?")), Title(Text("Hello?"))])), False)
    ]
    for target, expected in test_cases:
        print_test_result(target, expected)

def test_html():
    print_simple_header("html")
    test_cases = [
        (Page(Html()), False),
        (Page(Html([Head([Title(Text("Hello?"))]), Body([H1(Text("Hello!"))])])), True),
        (Page(Html(Div())), False)
    ]
    for target, expected in test_cases:
        print_test_result(target, expected)

def test_elem():
    print_test_result(Page(Elem()), False)

def test_write_to_file():
    print_simple_header("write_to_file")
    target = Page(
        Html([
            Head([
                Meta(attr={"charset": "UTF-8"}),
                Meta(attr={"name": "description", "content": "This is a test page for hello world."}),
                Meta(attr={"name": "author", "content": "dgerwig"}),
                Title(Text("💫 Testing html_file"))
            ]),
            Body([
                H1(Text("🌍 Hello World!")),
                Hr(),
                Br(),
                Hr(),
                P(Text("Welcome to this test page.")),
                Ul([
                    Li(Text("First item")),
                    Li(Text("Second item")),
                    Li(Text("Third item"))
                ]),
                Img(attr={"src": "https://picsum.photos/200", "alt": "Random Image"})
            ])
        ])
    )
    path = "test_file.html"
    target.write_to_file(path)
    print(f"{YELLOW}{target}{RESET}")
    print(f"File written to: {GREEN}{path}{RESET}")

def print_global_summary():
    print_simple_header("GLOBAL TEST SUMMARY")
    print(f"Total SUCCESS: {GREEN}{success_count}{RESET}")
    print(f"Total FAILURE: {RED}{failure_count}{RESET}")
    if failure_count == 0:
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
    test_write_to_file()

    print_global_summary()

if __name__ == '__main__':
    test()
