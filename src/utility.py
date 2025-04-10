import os
import shutil

def copy_directory(source_dir, dest_dir):
    """
    Recursively copies all contents from source_dir to dest_dir.
    First deletes all contents of dest_dir to ensure a clean copy.
    
    Args:
        source_dir: Path to the source directory
        dest_dir: Path to the destination directory
    """
    # Make sure the source directory exists
    if not os.path.exists(source_dir):
        print(f"Error: Source directory '{source_dir}' does not exist.")
        return
    
    # Create the destination directory if it doesn't exist
    if not os.path.exists(dest_dir):
        print(f"Creating destination directory: {dest_dir}")
        os.makedirs(dest_dir)
    else:
        # Delete all contents of the destination directory
        print(f"Cleaning destination directory: {dest_dir}")
        for item in os.listdir(dest_dir):
            item_path = os.path.join(dest_dir, item)
            try:
                if os.path.isfile(item_path) or os.path.islink(item_path):
                    os.unlink(item_path)
                    print(f"Deleted file: {item_path}")
                elif os.path.isdir(item_path):
                    shutil.rmtree(item_path)
                    print(f"Deleted directory: {item_path}")
            except Exception as e:
                print(f"Error: {e}")
    
    # Copy all contents from source to destination
    print(f"Copying from {source_dir} to {dest_dir}")
    for item in os.listdir(source_dir):
        s = os.path.join(source_dir, item)
        d = os.path.join(dest_dir, item)
        
        if os.path.isdir(s):
            # Recursively copy subdirectory
            print(f"Copying directory: {s} -> {d}")
            shutil.copytree(s, d, dirs_exist_ok=True)
        else:
            # Copy file
            print(f"Copying file: {s} -> {d}")
            shutil.copy2(s, d)
    
    print("Copy completed successfully!")