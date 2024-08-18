from htmlnode import ParentNode

from inline_md import text_to_textnodes

from textnode import text_node_to_html_node

def markdown_to_blocks(markdown: str) -> list:
    return [line.strip() for line in markdown.split("\n\n") if line.strip() != ""]

def markdown_to_html_node(markdown):
    block_list = markdown_to_blocks(markdown)
    children = children=[]
    for block in block_list:
        children.append(block_to_htmlnode(block))
    return ParentNode("div", children=children)

def block_to_htmlnode(block):
    block_type = block_to_block_type(block)
    match block_type:
        case "p":
            return paragraph_to_htmlnode(block)
        case "h1" | "h2" | "h3" | "h4" | "h5" | "h6":
            return heading_to_htmlnode(block)
        case "code":
            return code_to_htmlnode(block)
        case "blockquote":
            return blockquote_to_htmlnode(block)
        case "ul":
            return ul_to_htmlnode(block)
        case "ol":
            return ol_to_htmlnode(block)
        case _:
            raise Exception(f"Invalid block type:\nBlock_type:{block_type}\n\nText = {block}")

def text_to_children(text: str) -> list:
    children = []
    textnodes = text_to_textnodes(text)
    for textnode in textnodes:
        htmlnode = text_node_to_html_node(text_node=textnode)
        children.append(htmlnode)
    return children

def paragraph_to_htmlnode(text: str) -> str:
    paragragh = " ".join(text.split("\n"))
    children = text_to_children(paragragh)
    return ParentNode("p", children=children)

def heading_to_htmlnode(text: str) -> str:
    heading = ""
    for i in text:
        if i == "#":
            heading += i
        else:
            break
    if (len(heading) > 6) or (len(heading) + 1 > len(text)):
        raise Exception(f"Invalid heading: {text}")
    words = raw_md_to_text(text)
    children = text_to_children(words)
    return ParentNode(f"h{len(heading)}", children=children)

def ol_to_htmlnode(text):
    ol_items = [item for item in raw_md_to_text(text).split("\n")]
    children = []
    for item in ol_items:
        children.append(ParentNode("li", children=text_to_children(item)))
    return ParentNode("ol", children=children)


def ul_to_htmlnode(text):
    ol_items = [item for item in raw_md_to_text(text).split("\n")]
    children = []
    for item in ol_items:
        children.append(ParentNode("li", children=text_to_children(item)))
    return ParentNode("ul", children=children)

def blockquote_to_htmlnode(text):
    words = raw_md_to_text(text)
    children = text_to_children(words)
    return ParentNode("blockquote", children=(children))

def code_to_htmlnode(text):
    words = raw_md_to_text(text)
    children = text_to_children(words)
    code = ParentNode("code", children=children)
    return ParentNode("pre", children=[code])

def block_to_block_type(block: str) -> str:
    match block[0]:
        case "#":
            heading = ""
            for i in block:
                if i == "#":
                    heading += i
                elif i == " ":
                    break
                else:
                    raise Exception(f"Invalid heading format: '{block}'")
            if len(heading) > 6:
                raise Exception(f"Invalid heading format: '{block}'")
            return f"h{len(heading)}"
        case "`":
            if block[0:3] == block[-1:-4:-1] == "```":
                return "code"
            else:
                return "p"
        case ">":
            for line in block.split("\n"):
                if line[0] != ">":
                    return "p"
            return "blockquote"
        case "*" | "-":
            for item in block.split("\n"):
                if item[0:2] != f"{block[0]} ":
                    return "p"
            return "ul"
        case "1":
            counter = 1
            for item in block.split("\n"):
                if item[0:3] != f"{counter}. ":
                    return "p"
                counter += 1
            return "ol"
        case _:
            return "p"

def raw_md_to_text(block):
    block_type = block_to_block_type(block)
    match block_type:
        case "h1" | "h2" | "h3" | "h4" | "h5" | "h6":
            heading_num = int(block_type[1])
            return block[heading_num + 1:]
        case "code":
            words = " ".join(block.split("\n"))
            return words[3:-3]
        case "blockquote":
            return " ".join([item[1:].strip() for item in block.split("\n")])
        case "ul":
            item_list = []
            for item in block.split("\n"):
                item_list.append(item[2:])
            return "\n".join(item_list)
        case "ol":
            item_list = []
            for item in block.split("\n"):
                item_list.append(item[3:])
            return "\n".join(item_list)
        case _:
            return block

