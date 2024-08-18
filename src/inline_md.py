import re

from textnode import TextNode, text_type_bold, text_type_text, text_type_italic, text_type_link, text_type_image, text_type_code

def to_html_helper_func(children: list):
    lst_of_children =  children.copy()
    html_str_repr = ""
    if lst_of_children == []:
        return ""
    else:
        html_str_repr += lst_of_children[0].to_html() + to_html_helper_func(lst_of_children[1:])
    return html_str_repr
        
def split_nodes_delimiter(old_nodes: list, delimiter: str, text_type: str):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != text_type_text:
            new_nodes.append(node)
        else:
            value = node.text
            counter = 2
            split_nodes = value.split(delimiter)
            if len(split_nodes) % 2 == 0:
                raise SyntaxError(f"Missing '{delimiter}' delimiter in '{node.text}' node")
            for text in split_nodes:
                if counter % 2 == 0 and text != "":
                    new_nodes.append(TextNode(text_type_text, text))
                elif counter % 2 != 0:
                    new_nodes.append(TextNode(text_type, text))
                counter += 1
    return new_nodes

def extract_markdown_images(text: str):
    return re.findall(r"!\[(.*?)\]\((.*?)\)", text)

def extract_markdown_links(text: str):
    return re.findall(r"\[(.*?)\]\((.*?)\)", text)

def split_nodes_image(old_nodes: list) -> list:
    new_nodes = []
    for node in old_nodes:
        if node.text_type != text_type_text:
            new_nodes.append(node)
            continue
        value = node.text
        split_text = re.split(r"!\[(.*?)\]\((.*?)\)", value)
        future_text_nodes = [split_text[i] for i in range(len(split_text)) if i % 3 == 0]
        future_image_nodes = extract_markdown_images(node.text)
        img_counter = 0
        txt_counter = 0
        for i in range(len(future_text_nodes) + len(future_image_nodes)):
            if i % 2 == 0 and future_text_nodes[img_counter] != "":
                new_nodes.append(TextNode(text_type_text, future_text_nodes[txt_counter]))
                txt_counter += 1
            elif i % 2 != 0:
                new_nodes.append(TextNode(text_type_image, future_image_nodes[img_counter][0], future_image_nodes[img_counter][1]))
                img_counter += 1
    return new_nodes

def split_nodes_link(old_nodes):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != text_type_text:
            new_nodes.append(node)
            continue
        value = node.text
        split_text = re.split(r"\[(.*?)\]\((.*?)\)", value)
        future_text_nodes = [split_text[i] for i in range(len(split_text)) if i % 3 == 0]
        future_link_nodes = extract_markdown_links(node.text)
        link_counter = 0
        txt_counter = 0
        for i in range(len(future_text_nodes) + len(future_link_nodes)):
            if i % 2 == 0 and future_text_nodes[link_counter] != "":
                new_nodes.append(TextNode(text_type_text, future_text_nodes[txt_counter]))
                txt_counter += 1
            elif i % 2 != 0:
                new_nodes.append(TextNode(text_type_link, future_link_nodes[link_counter][0], future_link_nodes[link_counter][1]))
                link_counter += 1
    return new_nodes

def text_to_textnodes(text):
    delimiters = [
        (text_type_bold, "**"), 
        (text_type_italic, "*"), 
        (text_type_code, "`"), 
        ]
    new_nodes = [TextNode(text_type_text, text)]
    for text_type, delimiter in delimiters:
        new_nodes = split_nodes_delimiter(new_nodes, delimiter, text_type)
    new_nodes = split_nodes_image(new_nodes)
    new_nodes = split_nodes_link(new_nodes)
    return new_nodes