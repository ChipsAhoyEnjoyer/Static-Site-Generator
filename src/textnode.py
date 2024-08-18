import htmlnode

text_type_text = "text"
text_type_bold = "bold"
text_type_italic = "italic"
text_type_code = "code"
text_type_link = "link"
text_type_image = "image"

class TextNode:
    def __init__(self, text_type: str, text: str, url: str = None):
        self.text = text
        self.text_type = text_type
        self.url = url
    
    def __eq__(self, obj: object):
        return (self.text == obj.text
            and self.text_type == obj.text_type
            and self.url == obj.url)

    def __repr__(self):
        return f"TextNode({self.text_type}, {self.text}, {self.url})"

def text_node_to_html_node(text_node: object):
    match text_node.text_type:
        case "text":
            return htmlnode.LeafNode(None, text_node.text)
        case "bold":
            return htmlnode.LeafNode("b", text_node.text)
        case "italic":
            return htmlnode.LeafNode("i", text_node.text)
        case "code":
            return htmlnode.LeafNode("code", text_node.text)
        case "link":
            return htmlnode.LeafNode("a", text_node.text, props={"href": text_node.url})
        case "image":
            return htmlnode.LeafNode("img", None, props={"src": text_node.url, "alt": text_node.text})
        case _:
            raise ValueError(f"Invalid text type: {text_node.text_type}")