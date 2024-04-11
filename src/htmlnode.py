from textnode import Text_Type

class HTMLNode():
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        pass

    def props_to_html(self):
        if self.props == None:
            return ""

        result = ""

        for i in self.props:
            result += f" {i}=\"{self.props[i]}\""

        return result

    def __repr__(self):
        return f"HTMLNode({self.tag}, {self.value}, {self.children}, {self.props})"

class LeafNode(HTMLNode):
    def __init__(self, tag=None, value=None, props=None):
        super().__init__(tag, value, None, props)

    def to_html(self):
        if self.value == None:
            raise ValueError("Value is required for leaf node")

        result = self.value
        if self.tag != None:
            result = f"<{self.tag}{self.props_to_html()}>{result}</{self.tag}>"

        return result

class ParentNode(HTMLNode):
    def __init__(self, tag=None, children=None, props=None):
        super().__init__(tag, None, children, props)

    def to_html(self):
        if self.tag == None:
            raise ValueError("No tag provided")

        if self.children == None:
            raise ValueError("No children provided")

        if len(self.children) == 1:
            return f"<{self.tag}>{self.children[0].to_html()}</{self.tag}>"

        tempNode = ParentNode(self.tag, self.children[1:], self.props)
        tempList = list(tempNode.to_html())
        idx = len(self.tag) + 2
        tempList.insert(idx, self.children[0].to_html())

        return ''.join(tempList)

def text_node_to_html_node(text_node):
    valid_types = [
        Text_Type.TEXT,
        Text_Type.BOLD,
        Text_Type.ITALIC,
        Text_Type.CODE,
        Text_Type.LINK,
        Text_Type.IMAGE
    ]

    if text_node.text_type not in valid_types:
        raise ValueError("Provided type not valid")

    result = None
    match text_node.text_type:
        case Text_Type.TEXT: result = LeafNode(None, text_node.text, None)
        case Text_Type.BOLD: result = LeafNode("b", text_node.text, None)
        case Text_Type.ITALIC: result = LeafNode("i", text_node.text, None)
        case Text_Type.CODE: result = LeafNode("code", text_node.text, None)
        case Text_Type.LINK: result = LeafNode("a", text_node.text, {"href": text_node.url})
        case Text_Type.IMAGE: result = LeafNode("img", "", {"src": text_node.url, "alt": text_node.text})

    return result

