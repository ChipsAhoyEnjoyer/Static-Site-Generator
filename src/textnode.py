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
    