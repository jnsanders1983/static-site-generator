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
        # Edge case: raw "#Title" without spaces
        if stripped.startswith("#") and not stripped.startswith("##"):
            return stripped[1:].strip()
            
    raise ValueError("Invalid Markdown Document: No H1 (#) header found.")

def generate_page(from_path: str, template_path: str, dest_path: str) -> None:
    """
    Reads a single markdown document and a baseline template file, 
    converts markdown structure to final HTML, injects meta variables,
    and writes the final file out to the destination path.
    """
    # 1. Read files safely into execution memory variables
    with open(from_path, "r", encoding="utf-8") as f:
        markdown_content = f.read()
        
    with open(template_path, "r", encoding="utf-8") as f:
        template_content = f.read()
        
    # 2. Extract context metadata safely with explicit exception fallbacks
    try:
        title = extract_title(markdown_content)
    except ValueError as error:
        print(f"\n[BUILD ERROR]: Skipping compilation for '{from_path}'. Reason: {error}")
        return  # Gracefully drop execution for this specific page, continuing the build loop

    print(f"Generating page: {from_path} -> {dest_path}")
    html_string = markdown_to_html_node(markdown_content).to_html()
    
    # 3. Replace token injection placeholders
    full_html = template_content.replace("{{ Title }}", title).replace("{{ Content }}", html_string)
    
    # 4. Enforce parent folder creation before writing target assets
    dest_dir = os.path.dirname(dest_path)
    if dest_dir:
        os.makedirs(dest_dir, exist_ok=True)
        
    with open(dest_path, "w", encoding="utf-8") as f:
        f.write(full_html)


def generate_pages_recursive(dir_path_content: str, template_path: str, dest_dir_path: str) -> None:
    """
    Recursively crawls a markdown directory tree, translating all found .md files 
    into standard web production .html targets using a consistent template layout.
    """
    if not os.path.exists(dir_path_content):
        raise ValueError(f"Content source directory does not exist: {dir_path_content}")

    # Read item names in the current content path context
    items = os.listdir(dir_path_content)
    
    for item in items:
        # Build paths for evaluation loops
        src_item_path = os.path.join(dir_path_content, item)
        dst_item_path = os.path.join(dest_dir_path, item)
        
        if os.path.isfile(src_item_path):
            # Process markdown content files only
            if item.endswith(".md"):
                # Swap out extensions to map standard webpage structure targets
                html_filename = item.replace(".md", ".html")
                target_html_path = os.path.join(dest_dir_path, html_filename)
                
                # Execute your file compiler routine
                generate_page(src_item_path, template_path, target_html_path)
        else:
            # Recursively pass down tracking contexts for nested subdirectories
            generate_pages_recursive(src_item_path, template_path, dst_item_path)
