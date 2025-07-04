from htmlnode import HTMLNode

class LeafNode(HTMLNode):
    def __init__(self, tag, value, props=None):
        super().__init__(tag, value, None, props)

    def to_html(self):
        if self.value == None:
            print(self.tag)
            raise ValueError("All leaf nodes must have a value")
        
        if not self.tag:
            return self.value
        
        return f"<{self.tag}{super().props_to_html()}>{self.value}</{self.tag}>"