from htmlnode import HTMLNode, ParentNode, LeafNode

from inline_md import text_to_textnodes, text_node_to_html_node

def markdown_to_blocks(markdown: str) -> list:
    return [line.strip() for line in markdown.split("\n\n") if line.strip() != ""]

def markdown_to_html_node(markdown):
    block_list = markdown_to_blocks(markdown)
    blocks_parentnode = ParentNode(tag="div", children=[])
    for block in block_list:
        block_type = block_to_block_type(block)
        text = raw_md_to_text(block)
        children = text_to_children(text)
        if block_type == "ol" or block_type == "ul":
            individual_parentnode = ParentNode(tag=block_type, children=[LeafNode(block_type, text)])
        else:
            individual_parentnode = ParentNode(tag=block_type, children=children)
        blocks_parentnode.children.append(individual_parentnode)
    return blocks_parentnode

def text_to_children(text):
    textnodes = text_to_textnodes(text)
    return [text_node_to_html_node(textnode) for textnode in textnodes]


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
                    return "p"
            return f"h{len(heading)}"
        case "`":
            if block[0:3] == block[-1:-4:-1] == "```":
                return "code"
            else:
                return "p"
        case ">":
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
    match block[0]:
        case "#":
            heading = ""
            for i in block:
                if i == "#":
                    heading += i
                elif i == " ":
                    break
                else:
                    return block
            return block[len(heading) + 1:]
        case "`":
            if block[0:3] == block[-1:-4:-1] == "```":
                return block[3:-3]
            else:
                return block
        case ">":
            return block[1:]
        case "*" | "-":
            item_list = []
            for item in block.split("\n"):
                if item[0:2] != f"{block[0]} ":
                    return block
                else:
                    item_list.append(item[2:])
            return "\n".join(item_list)
        case "1":
            counter = 1
            item_list = []
            for item in block.split("\n"):
                if item[0:3] != f"{counter}. ":
                    return block
                else:
                    item_list.append(item[3:])
                counter += 1
            return "\n".join(item_list)
        case _:
            return block

