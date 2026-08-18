from textnode import TextType, TextNode
import re

def split_nodes_delimiter(old_nodes: list[TextNode], delimiter: str, text_type: TextType) -> list[TextNode]:
    new_nodes = []
    
    for node in old_nodes:
        # Only process nodes that are plain text
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue
            
        # Split the text string by the delimiter
        sections = node.text.split(delimiter)
        
        # If the length is even, it means there is an unclosed delimiter
        if len(sections) % 2 == 0:
            raise ValueError(f"Invalid markdown syntax: matching delimiter '{delimiter}' not found.")
            
        # Alternate between plain text and the new text type
        for i, section in enumerate(sections):
            # Skip empty strings (e.g., if a delimiter is at the very start/end)
            if section == "":
                continue
                
            if i % 2 == 0:
                new_nodes.append(TextNode(section, TextType.TEXT))
            else:
                new_nodes.append(TextNode(section, text_type))
                
    return new_nodes

def extract_markdown_images(text: str) -> list[tuple[str, str]]:
    # Finds ![alt text](url)
    pattern = r"!\[([^\[\]]*)\]\(([^\(\)]*)\)"
    return re.findall(pattern, text)

def extract_markdown_links(text: str) -> list[tuple[str, str]]:
    # Finds [anchor text](url) only if NOT preceded by !
    pattern = r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)"
    return re.findall(pattern, text)