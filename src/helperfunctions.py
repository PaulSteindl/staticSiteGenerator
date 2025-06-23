import re
from blocktype import BlockType, block_to_block_type
from htmlnode import HTMLNode
from parentnode import ParentNode
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
            return LeafNode("img", "", {"src" : text_node.url, "alt" : text_node.text})
        
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

def get_heading_tag(markdown):
    for i in range(0, 6):
        if markdown[i] != "#":
            return f"h{i}"
    raise Exception("unexpected # count (>6), invalid heading")

def text_to_children(text):
    text = text.strip()
    text = text.replace("\n", " ")
    text_nodes = text_to_textnodes(text)
    html_nodes = [text_node_to_html_node(node) for node in text_nodes]
    return html_nodes

def handle_paragraph(markdown_block):
    child_nodes = text_to_children(markdown_block)
    return ParentNode("p", child_nodes)

def handle_heading(markdown_block):
    tag = get_heading_tag(markdown_block)
    heading_text = markdown_block.lstrip("#").strip()
    child_nodes = text_to_children(heading_text)
    return ParentNode(tag, child_nodes)

def handle_code(markdown_block):
    code_text = markdown_block.strip("`").strip() + "\n"
    code_text_node = TextNode(code_text, TextType.CODE)
    code_html_node = text_node_to_html_node(code_text_node)
    return ParentNode("pre", [code_html_node])

def handle_quote(markdown_block):
    quote_text = markdown_block.lstrip(">").strip()
    child_nodes = text_to_children(quote_text)
    return ParentNode("blockquote", child_nodes)

def handle_unordered_list(markdown_block):
    items = [line.lstrip("-").strip() for line in markdown_block.split("\n") if line.strip()]
    li_nodes = [ParentNode("li", text_to_children(item)) for item in items]
    return ParentNode("ul", li_nodes)

def handle_ordered_list(markdown_block):
    items = [re.sub(r"^\d+\.\s*", "", line).strip() for line in markdown_block.split("\n") if line.strip()]
    li_nodes = [ParentNode("li", text_to_children(item)) for item in items]
    return ParentNode("ol", li_nodes)

def markdown_to_html_node(markdown):
    if not markdown:
        return LeafNode("div", "")

    markdown_blocks = markdown_to_blocks(markdown)
    children = []

    for markdown_block in markdown_blocks:
        blocktype = block_to_block_type(markdown_block)

        match(blocktype):
            case BlockType.PARAGRAPH:
                children.append(handle_paragraph(markdown_block))
            
            case BlockType.HEADING:
                children.append(handle_heading(markdown_block))
            
            case BlockType.CODE:
                children.append(handle_code(markdown_block))

            case BlockType.QUOTE:
                children.append(handle_quote(markdown_block))

            case BlockType.UNORDERED_LIST:
                children.append(handle_unordered_list(markdown_block))
            
            case BlockType.ORDERED_LIST:
                children.append(handle_ordered_list(markdown_block))
            
            case _:
                children.append(handle_paragraph(markdown_block))        

    return ParentNode("div", children)

def extract_title(markdown):
    title = re.search(r"^\s*#(?!#)\s*(.+?)\s*$", markdown, re.MULTILINE)
    if not title:
        raise Exception("No h1 found in document")
    return title.group(1)
        