from inline_md import to_html_helper_func

class HTMLNode:
    '''
    Tag: HTML tag
    Value: String/content inside the HTML tag(s)
    Children: List of HTMLNode objects representing the children of this node
    Props: Key/value pairs representing attributes of the HTML tag. e.g. for the 
           <a> tag, {"href": "https://www.boot.dev"}
    '''
    def __init__(self, tag: str=None, value: str=None, children: list=None, props: dict=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props
    
    def to_html(self):
        raise NotImplementedError
    
    def props_to_html(self):
        if self.props == None:
            return ""
        attributes = ""
        for key, value in self.props.items():
            attributes += f" {key}='{value}'"
        return attributes
    
    def __repr__(self):
        return f"HTMLNode({self.tag}, {self.value}, children: {self.children}, {self.props})"

class LeafNode(HTMLNode):
    def __init__(self, tag: str = None, value: str = None, children: list = None, props: dict = None):
        super().__init__(tag, value, None, props)
        
    def __repr__(self):
        return f"LeafNode({self.tag}, {self.value}, {self.props})"

    def to_html(self) -> str:
        if self.value is None and self.tag != "img":
            raise ValueError("Invalid HTML: no value")
        if self.tag is None:
            return self.value
        match self.tag:
            case "a":
                return f"<a{self.props_to_html()}>{self.value}</a>"
            case "img":
                return f"<img{self.props_to_html()}>"
            case "blockquote":
                return f"<blockquote>\n{self.value}\n</blockquote>"
            case "ul":
                li = self.value.splitlines()
                li_items = ""
                for line in li:
                    li_items += f"  <li>{line}</li>\n"
                return f"\n{li_items}"
            case "ol":
                li = self.value.splitlines()
                li_items = ""
                for line in li:
                    li_items += f"  <li>{line}</li>\n"
                return f"\n{li_items}"
            case _:
                return f"<{self.tag}>{self.value}</{self.tag}>"
            
class ParentNode(HTMLNode):
    def __init__(self, tag: str = None, value: str = None, children: list = None, props: dict = None):
        super().__init__(tag, None, children, props)

    def __repr__(self):
        return f"ParentNode({self.tag}, children: {self.children}, {self.props})"
    
    def to_html(self):
        if self.tag is None:
            raise ValueError("Invalid HTML: missing tag")
        if self.children is None:
            raise ValueError("Invalid HTML: ParentNode object requires children argument")
        return f"<{self.tag}{self.props_to_html()}>{to_html_helper_func(self.children)}</{self.tag}>"
    
