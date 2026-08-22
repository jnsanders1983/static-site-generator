import os
from markdown_blocks import markdown_to_html_node

def extract_title(markdown: str) -> str:
    """
    Finds the first H1 header line (starting with a single #) 
    in a markdown file, strips it, and returns the title string.
    Raises a ValueError if no H1 header exists.
    """
    lines = markdown.split("\n")
    for line in lines:
        stripped = line.strip()
        if stripped.startswith("# "):
            return stripped[2:].strip()
        if stripped.startswith("#") and not stripped.startswith("##"):
            return stripped[1:].strip()
            
    raise ValueError("Invalid Markdown Document: No H1 (#) header found.")

def generate_page(from_path: str, template_path: str, dest_path: str, basepath: str) -> None:
    """
    Reads a markdown file, converts it to HTML, injects template variables,
    and updates root-relative path links dynamically to support custom subdirectories.
    """
    # 1. Read files safely into variables
    with open(from_path, "r", encoding="utf-8") as f:
        markdown_content = f.read()
        
    with open(template_path, "r", encoding="utf-8") as f:
        template_content = f.read()
        
    # 2. Extract context metadata and convert markdown to HTML text
    title = extract_title(markdown_content)
    html_string = markdown_to_html_node(markdown_content).to_html()
    
    # 3. Replace token injection placeholders
    full_html = template_content.replace("{{ Title }}", title).replace("{{ Content }}", html_string)
    
    # 4. Replace root-relative paths to match the configured basepath variable
    full_html = full_html.replace('href="/', f'href="{basepath}')
    full_html = full_html.replace('src="/', f'src="{basepath}')
    
    print(f"Generating page: {from_path} -> {dest_path}")
    
    # 5. Enforce parent folder creation before writing target assets
    dest_dir = os.path.dirname(dest_path)
    if dest_dir:
        os.makedirs(dest_dir, exist_ok=True)
        
    with open(dest_path, "w", encoding="utf-8") as f:
        f.write(full_html)

def generate_pages_recursive(dir_path_content: str, template_path: str, dest_dir_path: str, basepath: str) -> None:
    """
    Recursively crawls a markdown directory tree, translating all found .md files 
    into standard web production .html targets using a consistent template layout.
    """
    if not os.path.exists(dir_path_content):
        raise ValueError(f"Content source directory does not exist: {dir_path_content}")

    items = os.listdir(dir_path_content)
    
    for item in items:
        src_item_path = os.path.join(dir_path_content, item)
        dst_item_path = os.path.join(dest_dir_path, item)
        
        if os.path.isfile(src_item_path):
            if item.endswith(".md"):
                html_filename = item.replace(".md", ".html")
                target_html_path = os.path.join(dest_dir_path, html_filename)
                
                # Forward basepath to the child file processor
                generate_page(src_item_path, template_path, target_html_path, basepath)
        else:
            # Recursively pass down tracking contexts for nested subdirectories
            generate_pages_recursive(src_item_path, template_path, dst_item_path, basepath)
