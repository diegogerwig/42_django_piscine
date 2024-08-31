from elem import Elem, Text


class Html(Elem):  # 'html' is the root element of an HTML document.
    def __init__(self, content=None, attr={}):
        super().__init__(tag="html", attr=attr, content=content, tag_type="double")


class Head(Elem):  # 'head' is the container for metadata (data about data).
    def __init__(self, content=None, attr={}):
        super().__init__(tag="head", attr=attr, content=content, tag_type="double")


class Body(Elem):  # 'body' is the container for the visible content of the document.
    def __init__(self, content=None, attr={}):
        super().__init__(tag="body", attr=attr, content=content, tag_type="double")


class Title(Elem):  # 'title' is the title of the document.
    def __init__(self, content=None, attr={}):
        super().__init__(tag="title", attr=attr, content=content, tag_type="double")


class Meta(Elem):  # 'meta' is used to specify metadata about the HTML document.
    def __init__(self, content=None, attr={}):
        super().__init__(tag="meta", attr=attr, content=content, tag_type="simple")


class Img(Elem):  # 'img' is used to embed an image in an HTML page.
    def __init__(self, content=None, attr={}):
        super().__init__(tag="img", attr=attr, content=content, tag_type="simple")


class Table(Elem):  # 'table' is used to create a table in an HTML page.
    def __init__(self, content=None, attr={}):
        super().__init__(tag="table", attr=attr, content=content, tag_type="double")


class Th(Elem):  # 'th' is used to create a header cell in a table.
    def __init__(self, content=None, attr={}):
        super().__init__(tag="th", attr=attr, content=content, tag_type="double")


class Tr(Elem):  # 'tr' is used to create a row in a table.
    def __init__(self, content=None, attr={}):
        super().__init__(tag="tr", attr=attr, content=content, tag_type="double")


class Td(Elem):  # 'td' is used to create a cell in a table.
    def __init__(self, content=None, attr={}):
        super().__init__(tag="td", attr=attr, content=content, tag_type="double")


class Ul(Elem):  # 'ul' is used to create an unordered list in an HTML page.
    def __init__(self, content=None, attr={}):
        super().__init__(tag="ul", attr=attr, content=content, tag_type="double")


class Ol(Elem):  # 'ol' is used to create an ordered list in an HTML page.
    def __init__(self, content=None, attr={}):
        super().__init__(tag="ol", attr=attr, content=content, tag_type="double")


class Li(Elem):  # 'li' is used to create a list item in an HTML page.
    def __init__(self, content=None, attr={}):
        super().__init__(tag="li", attr=attr, content=content, tag_type="double")


class H1(Elem):  # 'h1' is used to create a header in an HTML page.
    def __init__(self, content=None, attr={}):
        super().__init__(tag="h1", attr=attr, content=content, tag_type="double")


class H2(Elem):  # 'h2' is used to create a header in an HTML page.
    def __init__(self, content=None, attr={}):
        super().__init__(tag="h2", attr=attr, content=content, tag_type="double")


class P(Elem):  # 'p' is used to create a paragraph in an HTML page.
    def __init__(self, content=None, attr={}):
        super().__init__(tag="p", attr=attr, content=content, tag_type="double")


class Div(Elem):  # 'div' is used to create a division or a section in an HTML page.
    def __init__(self, content=None, attr={}):
        super().__init__(tag="div", attr=attr, content=content, tag_type="double")


class Span(Elem):  # 'span' is used to group inline-elements in a document.
    def __init__(self, content=None, attr={}):
        super().__init__(tag="span", attr=attr, content=content, tag_type="double")


class Hr(Elem):  # 'hr' is Horizontal Rule. It is used to separate content.
    def __init__(self, content=None, attr={}):
        super().__init__(tag="hr", attr=attr, content=content, tag_type="simple")


class Br(Elem):  # 'br' is Line Break. It is used to break lines.
    def __init__(self, content=None, attr={}):
        super().__init__(tag="br", attr=attr, content=content, tag_type="simple")


def create_html():
    print(Html([Head(), Body()]))

    print('\n' + '='*50 + '\n')

    elem = Elem(
        tag='html',
        content=[
            Elem(
                tag='head',
                content=Elem(
                    tag='title',
                    content=Text('"Hello ground!"')
                )
            ),
            Elem(
                tag='body',
                content=[
                    Elem(
                        tag='h1',
                        content=Text('"Oh no, not again!"')
                    ),
                    Elem(
                        tag='img',
                        tag_type='simple',
                        attr={'src': 'http://i.imgur.com/pfp3T.jpg'}
                    )
                ]
            )
        ]
    )
    print(elem)


if __name__ == '__main__':
    create_html()
