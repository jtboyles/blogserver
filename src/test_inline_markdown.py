import unittest

from textnode import (
    TextNode,
    Text_Type,
)

from inline_markdown import (
    split_nodes_delimiter,
    split_nodes_image,
    split_nodes_link,
    extract_markdown_images,
    extract_markdown_links,
    text_to_textnodes
)

class Test_Text_To_Textnodes(unittest.TestCase):
    def test_eq(self):
        testlol = text_to_textnodes("Test lol **what** the *fudge* is going `on` hehe heck ![image](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png) hehe")

        ttn_test = [
            "This is **text** with an *italic* word and a `code block` and an ![image](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png) and a ![link](https://boot.dev)"


        ]
        ttn_result = [
            [
                TextNode("This is ", Text_Type.TEXT),
                TextNode("text", Text_Type.BOLD),
                TextNode(" with an ", Text_Type.TEXT),
                TextNode("italic", Text_Type.ITALIC),
                TextNode(" word and a ", Text_Type.TEXT),
                TextNode("code block", Text_Type.CODE),
                TextNode(" and an ", Text_Type.TEXT),
                TextNode("image", Text_Type.IMAGE, "https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png"),
                TextNode(" and a ", Text_Type.TEXT),
                TextNode("link", Text_Type.LINK, "https://boot.dev"),
            ]

        ]

        for i in range(len(ttn_result)):
            temp_test = text_to_textnodes(ttn_test[i])

            test_one = [x.repr() for x in temp_test]
            test_two = [x.repr() for x in ttn_result[i]]

            self.assertEqual(test_one, test_two)

class Test_Split_Nodes_Delimiter(unittest.TestCase):
    def test_eq(self):
        split_test = [
                split_nodes_delimiter(TextNode("This is *text* with a * in it", "text"), "*", "bold"),
                split_nodes_delimiter(TextNode("This is -text- with -a- - in it", "text"), "-", "italic"),
                split_nodes_delimiter(TextNode("This is text with a `code block` word", "text"), "`", "code")
        ]

        split_result = [
            [
                TextNode("This is ", "text"),
                TextNode("text", "bold"),
                TextNode(" with a * in it", "text")
            ],
            [
                TextNode("This is ", "text"),
                TextNode("text", "italic"),
                TextNode(" with ", "text"),
                TextNode("a", "italic"),
                TextNode(" - in it", "text")
            ],
            [
                TextNode("This is text with a ", Text_Type.TEXT),
                TextNode("code block", Text_Type.CODE),
                TextNode(" word", Text_Type.TEXT),
            ]

        ]

        for j in range(len(split_result)):
            for i in range(j):
                self.assertEqual(split_test[j][i].repr(), split_result[j][i].repr())

class Test_Split_Nodes_Image(unittest.TestCase):
    def test_eq(self):
        test_image_nodes = [
            TextNode(
                "This is text with an ![image](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png) and another ![second image](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/3elNhQu.png)",
                Text_Type.TEXT,
            ),
            TextNode("this is a bunch of other text with ![image test](https://google.com/)![img](https://regexr.com/) hehehehee", Text_Type.TEXT),
            TextNode("this is a textnode without an image", Text_Type.TEXT)
        ]
        result_image_nodes = [
            [
                TextNode("This is text with an ", Text_Type.TEXT),
                TextNode("image", Text_Type.IMAGE, "https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png"),
                TextNode(" and another ", Text_Type.TEXT),
                TextNode("second image", Text_Type.IMAGE, "https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/3elNhQu.png"),
            ],
            [
                TextNode("this is a bunch of other text with ", Text_Type.TEXT),
                TextNode("image test", Text_Type.IMAGE, "https://google.com/"),
                TextNode("img", Text_Type.IMAGE, "https://regexr.com/"),
                TextNode(" hehehehee", Text_Type.TEXT)
            ],
            [
                TextNode("this is a textnode without an image", Text_Type.TEXT)
            ]
        ]

        for i in range(len(test_image_nodes)):
            new_nodes = split_nodes_image(test_image_nodes[i])
            test_result_node = [x.repr() for x in new_nodes]
            result_result_node = [m.repr() for m in result_image_nodes[i]]
            self.assertEqual(test_result_node, result_result_node)

class Test_Extract_Markdown_Images(unittest.TestCase):
    def test_eq(self):
        self.assertEqual(extract_markdown_images("this is a bunch of text with ![img](https://regexr.com/)"), [('img', 'https://regexr.com/')])
        self.assertEqual(extract_markdown_links("this is a bunch of text with ![test_one](https://regexr.com/)![test_two](https://google.com/)"), [('test_one', 'https://regexr.com/'), ('test_two', 'https://google.com/')])

        self.assertEqual(extract_markdown_links("this is a bunch of text with ![img](https://regexr.com/)"), None)

class Test_Extract_Markdown_Links(unittest.TestCase):
    def test_eq(self):
        test_link_nodes = [
            TextNode("This is text with an ![image](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png) and another ![second image](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/3elNhQu.png)", Text_Type.TEXT),
            TextNode("this is a bunch of other text with ![link test](https://google.com/)![link two](https://regexr.com/) hehehehee", Text_Type.TEXT)
        ]

        result_link_nodes = [
            [
                TextNode("This is text with an ![image](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png) and another ![second image](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/3elNhQu.png)", Text_Type.TEXT)
            ],
            [
                TextNode("this is a bunch of other text with ", Text_Type.TEXT),
                TextNode("link test", Text_Type.LINK, "https://google.com/"),
                TextNode("link two", Text_Type.LINK, "https://regexr.com/"),
                TextNode(" hehehehee", Text_Type.TEXT)
            ]
        ]

        for i in range(len(test_link_nodes)):
            new_new_nodes = split_nodes_link(test_link_nodes[i])
            new_test_result_node = [x.repr() for x in new_new_nodes]
            new_result_result_node = [m.repr() for m in result_link_nodes[i]]
            self.assertEqual(new_test_result_node, new_result_result_node)

if __name__ == "__main__":
    unittest.main()
