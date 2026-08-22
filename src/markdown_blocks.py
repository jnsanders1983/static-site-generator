import re
from enum import Enum

# Import your nodes and types precisely from your project files
from htmlnode import HTMLNode
from parentnode import ParentNode
from leafnode import LeafNode
from textnode import TextNode, TextType, text_node_to_html_node
from inline_markdown import text_to_textnodes


class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"

# --- Shared Text to Children Utility ---

def text_to_children(text: str) -> list[HTMLNode]:
    """
    Transforms raw block text into a list of child nodes using inline rules.
    Ensures an empty string returns at least one text LeafNode so ParentNode doesn't crash.
    """
    if not text:
        return [LeafNode(tag=None, value="")]
    
    text_nodes = text_to_textnodes(text)
    if not text_nodes:
        return [LeafNode(tag=None, value="")]
        
    children = []
    for text_node in text_nodes:
        html_node = text_node_to_html_node(text_node)
        children.append(html_node)
    return children

# --- Structural Block Utilities ---

def block_to_block_type(block: str) -> BlockType:
    if re.match(r"^#{1,6}\s", block):
        return BlockType.HEADING
    if block.startswith("```\n") and block.endswith("```"):
        return BlockType.CODE
    
    lines = block.split("\n")
    if all(line.startswith(">") for line in lines):
        return BlockType.QUOTE
    if all(line.startswith("- ") for line in lines):
        return BlockType.UNORDERED_LIST
        
    is_ordered_list = True
    for i, line in enumerate(lines):
        expected_prefix = f"{i + 1}. "
        if not line.startswith(expected_prefix):
            is_ordered_list = False
            break
    if is_ordered_list:
        return BlockType.ORDERED_LIST
        
    return BlockType.PARAGRAPH

def markdown_to_blocks(markdown: str) -> list[str]:
    blocks = markdown.split("\n\n")
    filtered_blocks = []
    for block in blocks:
        stripped = block.strip()
        if stripped:
            filtered_blocks.append(stripped)
    return filtered_blocks

# --- Block to ParentNode Conversions ---

def _paragraph_to_html(block: str) -> ParentNode:
    clean_text = " ".join(block.split("\n"))
    return ParentNode(tag="p", children=text_to_children(clean_text))

def _heading_to_html(block: str) -> ParentNode:
    match = re.match(r"^(#{1,6})\s", block)
    level = len(match.group(1))
    text = block[level + 1:]
    clean_text = " ".join(text.split("\n"))
    return ParentNode(tag=f"h{level}", children=text_to_children(clean_text))

def _code_to_html(block: str) -> ParentNode:
    """
    Safely extracts multi-line literal block data and structures it inside 
    a clean <pre><code>...</code></pre> tag combination.
    """
    # 1. Strip out the raw leading ```\n and trailing ``` fences
    code_text = block[4:-3] + "\n"
    
    # 2. Create the inner text block as plain TextType.TEXT to prevent double-tagging
    inner_text_node = text_node_to_html_node(TextNode(code_text, TextType.TEXT))
    
    # 3. Wrap it in a single 'code' parent node, then return under 'pre'
    code_parent = ParentNode(tag="code", children=[inner_text_node])
    return ParentNode(tag="pre", children=[code_parent])


def _quote_to_html(block: str) -> ParentNode:
    lines = block.split("\n")
    clean_lines = []
    for line in lines:
        if line.startswith("> "):
            clean_lines.append(line[2:])
        elif line.startswith(">"):
            clean_lines.append(line[1:])
    clean_text = " ".join(clean_lines)
    return ParentNode(tag="blockquote", children=text_to_children(clean_text))

def _unordered_list_to_html(block: str) -> ParentNode:
    lines = block.split("\n")
    items = []
    for line in lines:
        text = line[2:]
        items.append(ParentNode(tag="li", children=text_to_children(text)))
    return ParentNode(tag="ul", children=items)

def _ordered_list_to_html(block: str) -> ParentNode:
    lines = block.split("\n")
    items = []
    for i, line in enumerate(lines):
        prefix_len = len(f"{i + 1}. ")
        text = line[prefix_len:]
        items.append(ParentNode(tag="li", children=text_to_children(text)))
    return ParentNode(tag="ol", children=items)

# --- Primary Entry Point ---

def markdown_to_html_node(markdown: str) -> ParentNode:
    blocks = markdown_to_blocks(markdown)
    block_nodes = []
    
    for block in blocks:
        block_type = block_to_block_type(block)
        
        if block_type == BlockType.PARAGRAPH:
            node = _paragraph_to_html(block)
        elif block_type == BlockType.HEADING:
            node = _heading_to_html(block)
        elif block_type == BlockType.CODE:
            node = _code_to_html(block)
        elif block_type == BlockType.QUOTE:
            node = _quote_to_html(block)
        elif block_type == BlockType.UNORDERED_LIST:
            node = _unordered_list_to_html(block)
        elif block_type == BlockType.ORDERED_LIST:
            node = _ordered_list_to_html(block)
        else:
            raise ValueError(f"Invalid block type: {block_type}")
            
        block_nodes.append(node)
        
    # Return the entire document wrapped in a single ParentNode container
    return ParentNode(tag="div", children=block_nodes)
