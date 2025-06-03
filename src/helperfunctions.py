import re
from textnode import TextType, TextNode
from leafnode import LeafNode

REGEX_MARKDOWN_IMAGES = r"!\[([^\[\]]*)\]\(([^\(\)]*)\)"
REGEX_MARKDOWN_LINKS = r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)"

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
                new_nodes.append(TextNode(split_text[i], old_node.text_type, old_node.url))
                continue

            new_nodes.append(TextNode(split_text[i], text_type))
    return new_nodes

def extract_markdown_images(text):
    return re.findall(r"\!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)

def extract_markdown_links(text):
    return re.findall(r"(?<!\!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)

def split_nodes_image(old_nodes):
    new_nodes = []
    for old_node in old_nodes:
        images = extract_markdown_images(old_node.text)
        text_without_images = re.split(r"\!\[[^\[\]]*\]\([^\(\)]*\)", old_node.text)

        for i in range(0, len(text_without_images)):
            if text_without_images[i] != '':
                new_nodes.append(TextNode(text_without_images[i], old_node.text_type, old_node.url))

            if i < len(images):
                altText, url = images[i]
                new_nodes.append(TextNode(altText, TextType.IMAGE, url))

    return new_nodes

def split_nodes_link(old_nodes):
    new_nodes = []
    for old_node in old_nodes:
        links = extract_markdown_links(old_node.text)
        text_without_links = re.split(r"(?<!\!)\[[^\[\]]*]\([^\(\)]*\)", old_node.text)

        for i in range(0, len(text_without_links)):
            if text_without_links[i] != '':
                new_nodes.append(TextNode(text_without_links[i], old_node.text_type, old_node.url))

            if i < len(links):
                altText, url = links[i]
                new_nodes.append(TextNode(altText, TextType.LINK, url))

    return new_nodes

def text_to_textnodes(text):
    new_text_node = TextNode(text, TextType.NORMAL)
    tmp_text_nodes = split_nodes_image([new_text_node])
    tmp_text_nodes = split_nodes_link(tmp_text_nodes)
    tmp_text_nodes = split_nodes_delimiter(tmp_text_nodes, "**", TextType.BOLD)
    tmp_text_nodes = split_nodes_delimiter(tmp_text_nodes, "_", TextType.ITALIC)
    return split_nodes_delimiter(tmp_text_nodes, "`", TextType.CODE)

"""
Takes a raw Markdown string (representing a full document) as input and returns a list of "block" strings. 
Spliting Text by \n\n
Striping lines of trailing or leading whitespaces
Filter for non empty Lines
Convert and return List
"""
def markdown_to_blocks(markdown):
    return list(filter(lambda s: s != "", map(lambda s: s.strip(), markdown.split("\n\n"))))