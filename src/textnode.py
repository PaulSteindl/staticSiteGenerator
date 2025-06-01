from enum import Enum

class TextType(Enum):
    NORMAL = "normal_text"
    BOLD = "bold_text"
    ITALIC = "italic_text"
    CODE = "code_text"
    LINK = "link_text"
    IMAGE = "image_text"

class TextNode():

    """
    text - The text content of the node
    text_type - The type of text this node contains, which is a member of the TextType enum.
    url - The URL of the link or image, if the text is a link. Default to None if nothing is passed in.
    """
    def __init__(self, text, text_type, url = None):
        self.text = text
        self.text_type = text_type
        self.url = url

    def __eq__(self, value):
        return (isinstance(value, TextNode) and
            self.text == value.text and
            self.text_type == value.text_type and
            self.url == value.url)
    
    def __repr__(self):
        return f"{type(self).__name__}({self.text}, {self.text_type.value}, {self.url})"