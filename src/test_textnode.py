import unittest

from textnode import (
    TextNode,
    Text_Type
)

class TestTextNode(unittest.TestCase):
    def test_eq(self):
        test_nodes = [
            TextNode("This is a text node", Text_Type.BOLD, "https://boot.dev"),
            TextNode("This is also a text node", Text_Type.ITALIC, "https://boot.dev"),
            TextNode("This is a LINK text node", Text_Type.LINK)
        ]
        result_nodes = [
            "TextNode(This is a text node, bold, https://boot.dev)",
            "TextNode(This is also a text node, italic, https://boot.dev)",
            "TextNode(This is a LINK text node, link, None)"

        ]

        for i in range(len(test_nodes)):
            self.assertEqual(test_nodes[i].repr(), result_nodes[i])

if __name__ == "__main__":
    unittest.main()
