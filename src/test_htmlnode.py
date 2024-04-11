import unittest

from htmlnode import HTMLNode, LeafNode, ParentNode, text_node_to_html_node
from textnode import TextNode

class TestHTMLNode(unittest.TestCase):
    def test_eq(self):
        node1 = HTMLNode("a", "TestValue", None, {"href": "https://www.google.com", "target": "_blank"})
        node2 = HTMLNode("a", "TestValue", None, {"href": "https://www.google.com", "target": "_blank"})
        self.assertEqual(node1.__repr__(), node2.__repr__())

        test_prop_to_html = " href=\"https://www.google.com\" target=\"_blank\""
        self.assertEqual(node1.props_to_html(), test_prop_to_html)

        leaf1 = LeafNode("a", "This is a test value", {"href": "https://www.google.com", "target": "_blank"})
        leaf2 = "<a href=\"https://www.google.com\" target=\"_blank\">This is a test value</a>"
        leaf3 = LeafNode(None, "Testlol", None)
        leaf4 = "Testlol"
        leaf5 = LeafNode("a", "Testing single tag", None)
        leaf6 = "<a>Testing single tag</a>"

        self.assertEqual(leaf1.to_html(), leaf2)
        self.assertEqual(leaf3.to_html(), leaf4)
        self.assertEqual(leaf5.to_html(), leaf6)

        parent1 = ParentNode("p", [LeafNode("a", "This is a test value", {"href": "https://www.google.com", "target": "_blank"}), LeafNode("a", "This is a test value", {"href": "https://www.bootdev.com", "target": "_blank"})])
        parentResult = "<p><a href=\"https://www.google.com\" target=\"_blank\">This is a test value</a><a href=\"https://www.bootdev.com\" target=\"_blank\">This is a test value</a></p>"
        node = ParentNode(
        "p",
            [
                LeafNode("b", "Bold text"),
                LeafNode(None, "Normal text"),
                LeafNode("i", "italic text"),
                LeafNode(None, "Normal text"),
            ],
        )
        nodeResult = "<p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p>"

        node2 = ParentNode(
        "p",
            [
                ParentNode(
                "p",
                    [
                        LeafNode("b", "Bold text"),
                        LeafNode(None, "Normal text"),
                        LeafNode("i", "italic text"),
                        LeafNode(None, "Normal text"),
                    ],
                ),
                LeafNode("b", "Bold text"),
                LeafNode(None, "Normal text"),
                LeafNode("i", "italic text"),
                LeafNode(None, "Normal text"),
            ],
        )

        node2Result = "<p><p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p>"
        self.assertEqual(node.to_html(), nodeResult)
        self.assertEqual(parent1.to_html(), parentResult)
        self.assertEqual(node2.to_html(), node2Result)

        textNode1 = text_node_to_html_node(TextNode("Test", "text"))
        textNode2 = text_node_to_html_node(TextNode("bold testing", "bold"))
        textNode3 = text_node_to_html_node(TextNode("url testing", "link", "http://google.com"))
        textNode4 = text_node_to_html_node(TextNode("image testing", "image", "http://myimages.com"))

        textNodeTest = [
            textNode1.to_html(),
            textNode2.to_html(),
            textNode3.to_html(),
            textNode4.to_html()
        ]

        textNodeResult = [
            LeafNode(None, "Test", None).to_html(),
            LeafNode("b", "bold testing", None).to_html(),
            "<a href=\"http://google.com\">url testing</a>",
            "<img src=\"http://myimages.com\" alt=\"image testing\"></img>"
        ]

        self.assertEqual(textNodeTest, textNodeResult)

# tag, value, children, props
if __name__ == "__main__":
    unittest.main()
