import unittest

from markdown_blocks import (
        BlockType,
        markdown_to_HTMLNode,
        markdown_to_blocks,
        block_to_blocktype,
        ordered_list_to_HTMLNode,
        quote_to_HTMLNode,
        unordered_list_to_HTMLNode,
        code_to_HTMLNode,
        heading_to_HTMLNode,
        paragraph_to_HTMLNode
)

class Test_Markdown_To_Blocks(unittest.TestCase):
    def test_eq(self):
        test_case = [
            """
            This is a test example

            Of a multiline string in python
            Testing with multiple lines



            too many lines to separate here""",
            """
                This is **bolded** paragraph

                This is another paragraph with *italic* text and `code` here
                This is the same paragraph on a new line

                * This is a list
                * with items
            """
        ]

        result_case = [
            ["This is a test example", "Of a multiline string in python\nTesting with multiple lines", "too many lines to separate here"],
            ["This is **bolded** paragraph", "This is another paragraph with *italic* text and `code` here\nThis is the same paragraph on a new line", "* This is a list\n* with items"]
        ]

        for i in range(len(test_case)):
            self.assertEqual(markdown_to_blocks(test_case[i]), result_case[i])

class Test_Markdown_To_HTMLNode(unittest.TestCase):
    def test_eq(self):
        test_case = [
            """
            This is a test example

            Of a multiline string in python
            Testing with multiple lines



            too many lines to separate here""",
            """
                This is **bolded** paragraph

                This is another paragraph with *italic* text and `code` here
                This is the same paragraph on a new line

                * This is a list
                * with items
            """
        ]

        result_case = [
            "HTMLNode(div, None, [HTMLNode(p, None, [HTMLNode(None, This is a test example, None, None)], None), HTMLNode(p, None, [HTMLNode(None, Of a multiline string in python\nTesting with multiple lines, None, None)], None), HTMLNode(p, None, [HTMLNode(None, too many lines to separate here, None, None)], None)], None)",
            "HTMLNode(div, None, [HTMLNode(p, None, [HTMLNode(None, This is , None, None), HTMLNode(b, bolded, None, None), HTMLNode(None,  paragraph, None, None)], None), HTMLNode(p, None, [HTMLNode(None, This is another paragraph with , None, None), HTMLNode(i, italic, None, None), HTMLNode(None,  text and , None, None), HTMLNode(code, code, None, None), HTMLNode(None,  here\nThis is the same paragraph on a new line, None, None)], None), HTMLNode(ul, None, [HTMLNode(li, None, [HTMLNode(None, This is a list, None, None)], None), HTMLNode(li, None, [HTMLNode(None, with items, None, None)], None)], None)], None)"
        ]

        print(markdown_to_HTMLNode(test_case[0]).to_html())
        for i in range(len(test_case)):
            self.assertEqual(markdown_to_HTMLNode(test_case[i]).__repr__(), result_case[i])

class Test_Block_To_Block_Type(unittest.TestCase):
    def test_eq(self):
        test_case = [
            "##### Hello this is a test with header",
            "> This is a quote",
            "```this is code```",
            "1. This is a test\n2. This is also a test"
            "0. This is not an ordered list",
            "``this is not a quote``",
        ]

        result_case = [
            BlockType.HEADING,
            BlockType.QUOTE,
            BlockType.CODE,
            BlockType.ORDERED_LIST,
            BlockType.PARAGRAPH,
            BlockType.PARAGRAPH
        ]

        for i in range(len(test_case)):
            self.assertEqual(block_to_blocktype(test_case[i]), result_case[i])

class Test_Quote_To_HTMLnode(unittest.TestCase):
    def test_eq(self):
        test_case = [
            "> This is a *quote* I am testing with",
            "> This is also **a quote\nthat I am dealing with",
        ]

        result_case = [
            "HTMLNode(blockquote, None, [HTMLNode(None, This is a , None, None), HTMLNode(i, quote, None, None), HTMLNode(None,  I am testing with, None, None)], None)",
            "HTMLNode(blockquote, None, [HTMLNode(None, This is also **a quote\nthat I am dealing with, None, None)], None)",
        ]

        for i in range(len(test_case)):
            self.assertEqual(quote_to_HTMLNode(test_case[i]).__repr__(), result_case[i])

class Test_Code_To_HTMLNode(unittest.TestCase):
    def test_eq(self):
        test_case = [
            "```this is a test with a code block!```",
            "```this is also test\nwith a code block```"
        ]

        result_case = [
            "HTMLNode(pre, None, [HTMLNode(code, this is a test with a code block!, None, None)], None)",
            "HTMLNode(pre, None, [HTMLNode(code, this is also test\nwith a code block, None, None)], None)"
        ]

        for i in range(len(test_case)):
            self.assertEqual(code_to_HTMLNode(test_case[i]).__repr__(), result_case[i])

class Test_Heading_To_HTMLNode(unittest.TestCase):
    def test_eq(self):
        test_case = [
            "##### this is a heading *with* 5",
            "#### this is a heading *with* 4",
            "### this is a heading *with* 3",
            "## this is a heading *with* 2",
            "# this is a heading *with* 1",
        ]

        result_case = [
            "HTMLNode(h5, None, [HTMLNode(None, this is a heading , None, None), HTMLNode(i, with, None, None), HTMLNode(None,  5, None, None)], None)",
            "HTMLNode(h4, None, [HTMLNode(None, this is a heading , None, None), HTMLNode(i, with, None, None), HTMLNode(None,  4, None, None)], None)",
            "HTMLNode(h3, None, [HTMLNode(None, this is a heading , None, None), HTMLNode(i, with, None, None), HTMLNode(None,  3, None, None)], None)",
            "HTMLNode(h2, None, [HTMLNode(None, this is a heading , None, None), HTMLNode(i, with, None, None), HTMLNode(None,  2, None, None)], None)",
            "HTMLNode(h1, None, [HTMLNode(None, this is a heading , None, None), HTMLNode(i, with, None, None), HTMLNode(None,  1, None, None)], None)"
        ]
        for i in range(len(test_case)):
            self.assertEqual(heading_to_HTMLNode(test_case[i]).__repr__(), result_case[i])

class Test_Paragraph_To_HTMLNode(unittest.TestCase):
    def test_eq(self):
        test_case = [
            "this is normal text in a paragraph",
            "this is also normal text in a paragraph",
            "This is a test **paragraph**"
        ]

        result_case = [
            "HTMLNode(p, None, [HTMLNode(None, this is normal text in a paragraph, None, None)], None)",
            "HTMLNode(p, None, [HTMLNode(None, this is also normal text in a paragraph, None, None)], None)",
            "HTMLNode(p, None, [HTMLNode(None, This is a test , None, None), HTMLNode(b, paragraph, None, None)], None)"
        ]

        for i in range(len(test_case)):
            self.assertEqual(paragraph_to_HTMLNode(test_case[i]).__repr__(), result_case[i])

class Test_unordered_list_To_HTMLNode(unittest.TestCase):
    def test_eq(self):
        test_case = [
            "* This is a test\n* This is also a test\nAnd this is a test!",
        ]

        result_case = [
            "HTMLNode(ul, None, [HTMLNode(li, None, [HTMLNode(None, This is a test, None, None)], None), HTMLNode(li, None, [HTMLNode(None, This is also a test, None, None)], None), HTMLNode(text, None, [HTMLNode(None, And this is a test!, None, None)], None)], None)",
        ]

        for i in range(len(test_case)):
            self.assertEqual(unordered_list_to_HTMLNode(test_case[i]).__repr__(), result_case[i])

class Test_ordered_list_To_HTMLNode(unittest.TestCase):
    def test_eq(self):
        test_case = [
            "1. This is a test\n2. This is also a test"
        ]

        result_case = [
            "HTMLNode(ol, None, [HTMLNode(li, None, [HTMLNode(None, This is a test, None, None)], None), HTMLNode(li, None, [HTMLNode(None, This is also a test, None, None)], None)], None)"
        ]

        for i in range(len(test_case)):
            self.assertEqual(ordered_list_to_HTMLNode(test_case[i]).__repr__(), result_case[i])
