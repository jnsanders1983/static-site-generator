import os
from copystatic import clear_directory, copy_directory_recursive
# Make sure to import generate_pages_recursive instead of generate_page
from gencontent import generate_pages_recursive

def main():
    source_dir = "./static"
    public_dir = "./public"
    content_dir = "./content"          # Point this to the root content directory
    template_file = "./template.html"
    
    print("--- Initiating Comprehensive Clean Build ---")
    
    # 1. Clear target outputs and replicate raw assets
    clear_directory(public_dir)
    copy_directory_recursive(source_dir, public_dir)
    
    # 2. Fire the deep recursive compiler across the whole content folder tree
    print("--- Initiating Dynamic Page Generation Phase ---")
    generate_pages_recursive(content_dir, template_file, public_dir)
    
    print("--- Build Processes Completed Successfully ---")

if __name__ == "__main__":
    main()
