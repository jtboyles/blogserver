from textnode import TextNode

if __name__ == "__main__":
    text_node = TextNode("TEXT1", "TEXT2", "http://boot.dev")

    print(text_node.repr())
