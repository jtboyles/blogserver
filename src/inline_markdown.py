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
        Text_Type.BOLD:     "**",
        Text_Type.ITALIC:   "*",
        Text_Type.CODE:     "`"
    }

    temp_list = split_nodes_link(test_node)
    temp_result = []
    for i in temp_list:
        if i.text_type == "link":
            temp_result += [i]
        else:
            temp_result += split_nodes_image(i)

    temp_list = temp_result

    for i in delim_types:
        temp_result = []
        for j in temp_list:
            temp_result += split_nodes_delimiter(j, delim_types[i], i)

        temp_list = temp_result

    return temp_list

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    if not isinstance(old_nodes, TextNode):
        return old_nodes

    if old_nodes.text_type in [Text_Type.LINK, Text_Type.IMAGE]:
        return [old_nodes]

    new_node = list(old_nodes.text)
    node_len = len(new_node)
    max_end = len(new_node) - 1

    new_delim = list(delimiter)
    delim_len = len(delimiter)
    before_delim = delim_len - 1
    check_delim_len = 0

    idx_start = 0
    idx_end = 0
    closed_delim = 0

    result = []
    add_result = lambda x, y, z: result.append(TextNode(''.join(new_node[x:y]), z))

    for i in range(len(new_node)):
        if new_node[i] == new_delim[check_delim_len]:
            check_delim_len += 1
            if check_delim_len == delim_len:
                closed_delim += 1
                check_delim_len = 0

                if closed_delim % 2 == 0 and i != 0:
                    add_result(idx_end, idx_start, old_nodes.text_type)
                    add_result(idx_start + delim_len, i - before_delim, text_type)
                    idx_end = i + 1
                else:
                    idx_start = i - before_delim
        else:
            check_delim_len = 0

        if i == max_end:
            add_result(idx_end, node_len, old_nodes.text_type)

    return result

def split_nodes_image(old_nodes):
    return split_nodes(old_nodes, Text_Type.IMAGE)

def split_nodes_link(old_nodes):
    return split_nodes(old_nodes, Text_Type.LINK)

def split_nodes(old_nodes, text_type):
    if text_type == Text_Type.IMAGE:
        check_node = re.compile(r"(!\[[^\]]*?(?:image|img)[^\]]*?\]\([^\)]+\))")
    else:
        check_node = re.compile(r"(!\[(?![^\]]*?image|img)[^\]]+\]\([^\)]+\))")
    add_node = lambda text, type, *url: TextNode(text, type, url[0] if url else None) if len(text) > 0 else None

    test_node = old_nodes

    if len(check_node.findall(test_node.text)) == 0:
        return [add_node(test_node.text, Text_Type.TEXT)]

    result = check_node.finditer(test_node.text)

    list_results = [x.span() for x in result]
    start = list_results[0][0]
    end = list_results[0][1]

    extraction = extract_markdown(test_node.text[start:end], text_type)
    if extraction == None:
        extracted_node = add_node(test_node.text[start:end], Text_Type.TEXT)
    else:
        extracted_node = add_node(extraction[0][0], text_type, extraction[0][1])

    new_node = [
        add_node(test_node.text[:start], Text_Type.TEXT),
        extracted_node
    ]

    if len(test_node.text[end:]) > 0:
        new_node.extend(split_nodes(add_node(test_node.text[end:], Text_Type.TEXT), text_type))

    return list(filter(lambda item: item is not None, new_node))

def extract_markdown_images(text):
    return extract_markdown(text, Text_Type.IMAGE)

def extract_markdown_links(text):
    return extract_markdown(text, Text_Type.LINK)

def extract_markdown(text, text_type):
    if text_type == Text_Type.IMAGE:
        result = re.findall(r"!\[([^\]]*(?:image|img)[^\]]*)\]\(([^\)]+)\)", text)
    else:
        result = re.findall(r"!\[((?![^\]]*?image|img)[^\]]+)\]\(([^\)]+)\)", text)
    return result if len(result) > 0 else None
