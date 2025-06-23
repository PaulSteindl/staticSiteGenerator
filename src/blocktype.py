import re
from enum import Enum

class BlockType(Enum):
    PARAGRAPH = "paragraph_block"
    HEADING = "heading_block"
    CODE = "code_block"
    QUOTE = "quote_block"
    UNORDERED_LIST = "unordered_list_block"
    ORDERED_LIST = "ordered_list_block"


def is_number_increment(ordered_nrs):
    if not ordered_nrs:
        return False

    for i in range(len(ordered_nrs)):
        if int(ordered_nrs[i]) != i + 1:
            return False

    return True

def block_to_block_type(markdown_text):
    if re.search(r"^#{1,6} .+", markdown_text):
        return BlockType.HEADING
    
    if re.search(r"^```[\s\S]+```$", markdown_text):
        return BlockType.CODE
    
    if markdown_text.startswith(">"):
        return BlockType.QUOTE
    
    if markdown_text.startswith("- "):
        return BlockType.UNORDERED_LIST

    if is_number_increment(re.findall(r'^(\d+)\.', markdown_text, flags=re.MULTILINE)):
        return BlockType.ORDERED_LIST
    
    return BlockType.PARAGRAPH