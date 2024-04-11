import re

from textnode import (
    TextNode,
    Text_Type
)

def text_to_textnodes(text):
    if not isinstance(text, TextNode):
        test_node = TextNode(text, Text_Type.TEXT)
    else:
        test_node = text

    delim_types = {
        Text_Type.BOLD: "**",
        Text_Type.ITALIC: "*",
        Text_Type.CODE: "`"
    }
    # result = []

    print(split_nodes_delimiter(test_node, delim_types[Text_Type.BOLD], Text_Type.BOLD))



def split_nodes_delimiter(old_nodes, delimiter, text_type):
    if not isinstance(old_nodes, TextNode):
        return old_nodes

    new_node = list(old_nodes.text)
    node_len = len(new_node)
    max_end = len(new_node) - 1

    idx = 0
    idx_start = 0
    idx_end = 0
    closed_delim = 0

    result = []
    add_result = lambda x, y, z: result.append(TextNode(''.join(new_node[x:y]), z))

    for i in new_node:
        if i == delimiter:
            closed_delim += 1

            if closed_delim % 2 == 0 and idx != 0:
                add_result(idx_end, idx_start, Text_Type.TEXT)
                add_result(idx_start + 1, idx, text_type)
                idx_end = idx + 1
            else:
                idx_start = idx

        if idx == max_end:
            add_result(idx_end, node_len, Text_Type.TEXT)

        idx += 1
    return result

def split_nodes_image(old_nodes):
    check_node = re.compile(r"(!\[[^\]]*(?:image|img)[^\]]*\]\((?:(?:https?:\/\/)?(?:[^\)]*\.\w+\/)[^\)]*?\)))")
    add_node = lambda text, type, *url: TextNode(text, type, url[0] if url else None) if len(text) > 0 else None

    test_node = old_nodes

    if len(check_node.findall(test_node.text)) == 0:
        return [add_node(test_node.text, Text_Type.TEXT)]

    result = check_node.finditer(test_node.text)

    list_results = [x.span() for x in result]
    start = list_results[0][0]
    end = list_results[0][1]
    extraction = extract_markdown_images(test_node.text[start:end])

    if extraction == None:
        extracted_node = add_node(test_node.text[start:end], Text_Type.TEXT)
    else:
        extracted_node = add_node(extraction[0][0], Text_Type.IMAGE, extraction[0][1])

    new_node = [
        add_node(test_node.text[:start], Text_Type.TEXT),
        extracted_node
    ]

    if len(test_node.text[end:]) > 0:
        new_node.extend(split_nodes_image(add_node(test_node.text[end:], Text_Type.TEXT)))

    return list(filter(lambda item: item is not None, new_node))

def split_nodes_link(old_nodes):
    check_node = re.compile(r"(!\[(?![^\]]*?image|img)[^\]]+\]\((?:(?:https?:\/\/)?(?:[^\)]*\.\w+\/)[^\)]*?\)))")
    add_node = lambda text, type, *url: TextNode(text, type, url[0] if url else None) if len(text) > 0 else None

    test_node = old_nodes

    if len(check_node.findall(test_node.text)) == 0:
        return [add_node(test_node.text, Text_Type.TEXT)]

    result = check_node.finditer(test_node.text)

    list_results = [x.span() for x in result]
    start = list_results[0][0]
    end = list_results[0][1]
    extraction = extract_markdown_links(test_node.text[start:end])

    if extraction == None:
        extracted_node = add_node(test_node.text[start:end], Text_Type.TEXT)
    else:
        extracted_node = add_node(extraction[0][0], Text_Type.LINK, extraction[0][1])

    new_node = [
        add_node(test_node.text[:start], Text_Type.TEXT),
        extracted_node
    ]

    if len(test_node.text[end:]) > 0:
        new_node.extend(split_nodes_link(add_node(test_node.text[end:], Text_Type.TEXT)))

    return list(filter(lambda item: item is not None, new_node))

def extract_markdown_images(text):
    result = re.findall(r"!\[([^\]]*(?:image|img)[^\]]*)\]\(((?:https?:\/\/)?(?:[^\)]*\.\w+\/)[^\)]*?(?=\)))", text)
    return result if len(result) > 0 else None

def extract_markdown_links(text):
    result = re.findall(r"!\[((?!image|img)[^\]]+)\]\(((?:https?:\/\/)?(?:[^\)]*\.\w+\/)[^\)]*?(?=\)))", text)
    return result if len(result) > 0 else None

