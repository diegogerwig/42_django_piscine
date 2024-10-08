#!/usr/bin/python3

class Text(str):  # str is a built-in Python class that represents a string of characters. The Text class is a subclass of str.
    """
    A Text class to represent a text you could use with your HTML elements.

    Because directly using str class was too mainstream.
    """

    def __str__(self):
        """
        Do you really need a comment to understand this method?.
        """

        # Convert special characters to HTML entities
        text = super().__str__().replace('<', '&lt;').replace('>', '&gt;')  # super() initializes the parent class.

        # Handle the special case for a single double quote
        if text == '"':
            text = text.replace('"', '&quot;')

        # Replace newline characters with HTML line breaks
        text = text.replace('\n', '\n<br />\n')

        # Return the processed text
        return text


class Elem:
    """
    Elem will permit us to represent our HTML elements.
    """
    class ValidationError(Exception):
        def __init__(self, message="Error: content must be a Text instance or an Elem instance"):
            super().__init__(message)

    def __init__(self, tag='div', attr={}, content=None, tag_type='double'):
        """
        __init__() method.

        Obviously.
        """
        self.tag = tag
        self.attr = attr
        self.content = []
        if content:
            self.add_content(content)
        elif content is not None and not isinstance(content, Text):
            raise self.ValidationError
        self.tag_type = tag_type

    def __str__(self):
        """
        The __str__() method will permit us to make a plain HTML representation
        of our elements.
        Make sure it renders everything (tag, attributes, embedded
        elements...).
        """
        result = ""
        if self.tag_type == 'double':  # The double tag type is the most common tag type. It has an opening tag and a closing tag.
            result = "<{0}{1}>{2}</{0}>".format(self.tag, self.__make_attr(), self.__make_content())
        elif self.tag_type == 'simple':  # The simple tag type is a self-closing tag. It has an opening tag, but no closing tag.
            result = "<{0}{1} />".format(self.tag, self.__make_attr())
        return result

    def __make_attr(self):
        """
        Here is a function to render our elements attributes.
        """
        result = ''
        for pair in sorted(self.attr.items()):
            result += ' ' + str(pair[0]) + '="' + str(pair[1]) + '"'
        return result

    def __make_content(self):
        """
        Here is a method to render the content, including embedded elements.
        """
        if len(self.content) == 0:
            return ''
        result = '\n'
        for elem in self.content:
            result += "  " + str(elem).replace("\n", "\n  ") + "\n"
        return result

    def add_content(self, content):
        if not Elem.check_type(content):
            raise Elem.ValidationError
        if type(content) is list:
            self.content += [elem for elem in content if elem != Text('')]
        elif content != Text(''):
            self.content.append(content)

    @staticmethod  # The @staticmethod decorator is used to define a static method in a class. With a static method, you can call it without an object of the class.
    def check_type(content):
        """
        Is this object a HTML-compatible Text instance or a Elem, or even a
        list of both?
        """
        return (isinstance(content, Elem) or type(content) is Text or
                (type(content) is list and all([type(elem) is Text or
                                                isinstance(elem, Elem)
                                                for elem in content])))


def create_html():
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
