from textnode import TextType, TextNode
from leafnode import LeafNode

def text_node_to_html_node(text_node):
    match(text_node.text_type):

        case TextType.NORMAL:
            return LeafNode(None, text_node.text)
        
        case TextType.BOLD:
            return LeafNode("b", text_node.text)
        
        case TextType.ITALIC:
            return LeafNode("i", text_node.text)
        
        case TextType.CODE:
            return LeafNode("code", text_node.text)
        
        case TextType.LINK:
            if not text_node.url:
                raise ValueError(f"TextType {TextType.LINK} needs an url")
            return LeafNode("a", text_node.text, {"href" : text_node.url})
        
        case TextType.IMAGE:
            if not text_node.url:
                raise ValueError(f"TextType {TextType.IMAGE} needs an url")
            return LeafNode("img", None, {"src" : text_node.url, "alt" : text_node.text})
        
        case _:
            raise Exception(f"Unknow TextType {text_node.text_type}")
        
def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for old_node in old_nodes:
        split_text = old_node.text.split(delimiter)
        
        for i in range(0, len(split_text)):
            if not split_text[i]:
                continue

            if i % 2 == 0:
                new_nodes.append(TextNode(split_text[i], old_node.text_type))
                continue

            new_nodes.append(TextNode(split_text[i], text_type))
    return new_nodes