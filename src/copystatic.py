import os
import shutil

def clear_directory(directory_path: str) -> None:
    """
    Deletes all contents of the destination directory to ensure a clean copy.
    """
    if os.path.exists(directory_path):
        print(f"Purging destination folder: {directory_path}")
        shutil.rmtree(directory_path)
    
    print(f"Creating empty destination directory: {directory_path}")
    os.mkdir(directory_path)

def copy_directory_recursive(source_path: str, destination_path: str) -> None:
    """
    Recursively copies all files and subdirectories from source to destination.
    Uses log prints to track file system mutations during copy phases.
    """
    if not os.path.exists(source_path):
        raise ValueError(f"Source directory does not exist: {source_path}")

    # List all items inside the current source directory level
    items = os.listdir(source_path)
    
    for item in items:
        # Join path strings to evaluate full locations
        src_item_path = os.path.join(source_path, item)
        dst_item_path = os.path.join(destination_path, item)
        
        if os.path.isfile(src_item_path):
            print(f"Copying file: {src_item_path} -> {dst_item_path}")
            shutil.copy(src_item_path, dst_item_path)
        else:
            print(f"Creating subdirectory: {dst_item_path}")
            os.mkdir(dst_item_path)
            # Recurse down into nested child subdirectories
            copy_directory_recursive(src_item_path, dst_item_path)
