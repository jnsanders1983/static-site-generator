import sys
import os
from copystatic import clear_directory, copy_directory_recursive
from gencontent import generate_pages_recursive

def main():
    source_dir = "./static"
    public_dir = "./docs"
    content_dir = "./content"
    template_file = "./template.html"
    
    # Grab the first CLI argument if provided, otherwise default to "/"
    basepath = "/"
    if len(sys.argv) > 1:
        basepath = sys.argv[1]
        
    print(f"--- Initiating Clean Build with basepath: '{basepath}' ---")
    
    # 1. Purge production outputs and replicate static files
    clear_directory(public_dir)
    copy_directory_recursive(source_dir, public_dir)
    
    # 2. Run deep directory parsing loops, passing the custom basepath configuration
    print("--- Initiating Recursive Document Tree Compilations ---")
    generate_pages_recursive(content_dir, template_file, public_dir, basepath)
    
    print("--- Static Generation Phase Completed Successfully ---")

if __name__ == "__main__":
    main()
