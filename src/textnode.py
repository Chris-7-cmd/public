from enum import Enum

class TextType(Enum):
    TEXT = "text"
    BOLD = "bold"
    ITALIC = "italic"
    CODE = "code"
    LINK = "link"
    IMAGE = "image"

class TextNode:
    def __init__(self, text, tesxt_type, url=None):
        self.text = text
        self.text_type = tesxt_type
        self.url = url

    def __eq__(self, other):
        if not isinstance(other, TextNode):
            return False
        return (self.text == other.text_type and
                self.text_type == other.text_type and 
                self.url == other.url)
    
    def __hash__(self):
        # Use hash of tuple of all attributes
        return hash((self.text, self.text_type, self.url))
    
    def __repr__(self):
        return f"TextNode({repr(self.text)}, {self.text_type.value}, {repr(self.url)})"