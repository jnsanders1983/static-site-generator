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

def split_nodes_image(old_nodes: list[TextNode]) -> list[TextNode]:
    new_nodes = []
    
    for node in old_nodes:
        # Only split plain text nodes
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue
            
        current_text = node.text
        images = extract_markdown_images(current_text)
        
        # Tip: If there are no images, return the original node intact
        if not images:
            new_nodes.append(node)
            continue
            
        for alt_text, url in images:
            image_markdown = f"![{alt_text}]({url})"
            # Tip: Split exactly once at the first occurrence of this image
            sections = current_text.split(image_markdown, 1)
            
            # Tip: Only append if the preceding text is not empty
            if sections[0] != "":
                new_nodes.append(TextNode(sections[0], TextType.TEXT))
                
            new_nodes.append(TextNode(alt_text, TextType.IMAGE, url))
            
            # Move our cursor text to the remaining portion after the split
            current_text = sections[1]
            
        # Tip: Append any trailing text left over at the end of the loops
        if current_text != "":
            new_nodes.append(TextNode(current_text, TextType.TEXT))
            
    return new_nodes


def split_nodes_link(old_nodes: list[TextNode]) -> list[TextNode]:
    new_nodes = []
    
    for node in old_nodes:
        # Only split plain text nodes
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue
            
        current_text = node.text
        links = extract_markdown_links(current_text)
        
        # Tip: If there are no links, return the original node intact
        if not links:
            new_nodes.append(node)
            continue
            
        for anchor_text, url in links:
            link_markdown = f"[{anchor_text}]({url})"
            # Tip: Split exactly once at the first occurrence of this link
            sections = current_text.split(link_markdown, 1)
            
            # Tip: Only append if the preceding text is not empty
            if sections[0] != "":
                new_nodes.append(TextNode(sections[0], TextType.TEXT))
                
            new_nodes.append(TextNode(anchor_text, TextType.LINK, url))
            
            # Move our cursor text to the remaining portion after the split
            current_text = sections[1]
            
        # Tip: Append any trailing text left over at the end of the loops
        if current_text != "":
            new_nodes.append(TextNode(current_text, TextType.TEXT))
            
    return new_nodes

def text_to_textnodes(text: str) -> list[TextNode]:
    # Start with a single plain text node containing the whole string
    nodes = [TextNode(text, TextType.TEXT)]
    
    # Process images and regular links first
    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)
    
    # Process inline formatting markdown styles sequentially
    nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)
    nodes = split_nodes_delimiter(nodes, "_", TextType.ITALIC)
    nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)
    
    return nodes

def markdown_to_blocks(markdown: str) -> list[str]:
    # Split the document by single newlines first to inspect lines
    lines = markdown.split("\n")
    
    blocks = []
    current_block_lines = []
    
    for line in lines:
        # If a line is completely empty or just whitespace
        if line.strip() == "":
            if current_block_lines:
                # Join the accumulated lines into a block and save it
                blocks.append("\n".join(current_block_lines).strip())
                current_block_lines = []
        else:
            current_block_lines.append(line)
            
    # Don't forget to append the final block if text didn't end with a newline
    if current_block_lines:
        blocks.append("\n".join(current_block_lines).strip())
        
    # Final pass to filter out any stray empty strings
    return [b for b in blocks if b != ""]

