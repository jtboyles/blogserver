import re

from textnode import Text_Type
from inline_markdown import text_to_htmlnodes
from htmlnode import HTMLNode, ParentNode, LeafNode

class BlockType:
    PARAGRAPH       = "paragraph"
    HEADING         = "heading"
    QUOTE           = "quote"
    CODE            = "code"
    ORDERED_LIST    = "ordered_list"
    UNORDERED_LIST  = "unordered_list"

class BlockTag:
    PARAGRAPH               = "p"
    HEADING                 = "h"
    QUOTE                   = "blockquote"
    CODE_PARENT             = "pre"
    CODE_CHILD              = "code"
    ORDERED_LIST_PARENT     = "ol"
    UNORDERED_LIST_PARENT   = "ul"
    LIST_CHILD              = "li"
    DIV                     = "div"

class REqual(str):
    def __eq__(self, pattern):
        return True if re.fullmatch(pattern, self, re.DOTALL) else False

def markdown_to_blocks(markdown):
    temp_markdown = markdown.split('\n')

    temp_result = []
    result = []
    add_result = lambda x: result.append('\n'.join(x))

    for i in temp_markdown:
        temp_block = i.strip()
        if len(temp_block) > 0:
            temp_result += [temp_block]
            continue

        if len(temp_result) > 0:
            add_result(temp_result)
            temp_result = []

    if len(temp_result) > 0:
        add_result(temp_result)

    return result

def block_to_blocktype(markdown):
    block_type = ""

    def test_ordered_list(text_to_test):
        split_text = text_to_test.split('\n')

        for i in range(len(split_text)):
            if not split_text[i].startswith(f"{i + 1}. "):
                return False

        return True

    match REqual(markdown):
        case r'^#{1,6} .*$':
            block_type = BlockType.HEADING

        case r'^```.*```$':
            block_type = BlockType.CODE

        case r'^> .*$':
            block_type = BlockType.QUOTE

        case r'^[-\*] .*$':
            block_type = BlockType.UNORDERED_LIST

        case r'^[\d]\. .*':
            if test_ordered_list(markdown):
                block_type = BlockType.ORDERED_LIST
            else:
                block_type = BlockType.PARAGRAPH

        case _:
            block_type = BlockType.PARAGRAPH

    return block_type

def quote_to_HTMLNode(block):
    return ParentNode(BlockTag.QUOTE, text_to_htmlnodes(block[2:]))

def code_to_HTMLNode(block):
    remove_markdown = block[3:-3]
    return ParentNode(BlockTag.CODE_PARENT, [LeafNode(BlockTag.CODE_CHILD, remove_markdown)])

def heading_to_HTMLNode(block):
    heading_size = block.find(' ')
    heading_tag = f"{BlockTag.HEADING}{heading_size}"
    idx = heading_size + 1

    return ParentNode(heading_tag, text_to_htmlnodes(block[idx:]))

def paragraph_to_HTMLNode(block):
    return ParentNode(BlockTag.PARAGRAPH, text_to_htmlnodes(block))

def unordered_list_to_HTMLNode(block):
    result = []
    split_block = block.split('\n')

    for i in split_block:
        if i[:2] == "* ":
            result.append(ParentNode(BlockTag.LIST_CHILD, text_to_htmlnodes(i[2:])))
        else:
            result.append(ParentNode(Text_Type.TEXT, text_to_htmlnodes(i)))

    return ParentNode(BlockTag.UNORDERED_LIST_PARENT, result)

def ordered_list_to_HTMLNode(block):
    result = []
    split_block = block.split('\n')

    for i in split_block:
        idx = i.find(' ') + 1
        result.append(ParentNode(BlockTag.LIST_CHILD, text_to_htmlnodes(i[idx:])))

    return ParentNode(BlockTag.ORDERED_LIST_PARENT, result)

def convert_block(block_type):
    match block_type:
        case BlockType.HEADING:
            return heading_to_HTMLNode
        case BlockType.CODE:
            return code_to_HTMLNode
        case BlockType.QUOTE:
            return quote_to_HTMLNode
        case BlockType.ORDERED_LIST:
            return ordered_list_to_HTMLNode
        case BlockType.UNORDERED_LIST:
            return unordered_list_to_HTMLNode
        case _:
            return paragraph_to_HTMLNode

def markdown_to_HTMLNode(markdown):
    blocks = markdown_to_blocks(markdown)
    result = []

    for i in blocks:
        convert_func = convert_block(block_to_blocktype(i))
        result.append(convert_func(i))

    return ParentNode(BlockTag.DIV, result)
