from utility import copy_directory
from page_generator import generate_pages_recursive
import os
import shutil

def main():
    """
    Main function to run the static site generator
    """
    print("Starting static site generator...")
    
    # Define directories
    static_dir = "static"
    public_dir = "public"
    content_dir = "content"
    template_path = "template.html"
    
    # 1. Delete anything in the public directory
    if os.path.exists(public_dir):
        print(f"Cleaning {public_dir} directory")
        shutil.rmtree(public_dir)
    
    # 2. Copy all the static files from static to public
    print(f"Copying static files from {static_dir} to {public_dir}")
    copy_directory(static_dir, public_dir)
    
    # 3. Generate HTML files for all markdown files in the content directory
    print(f"Generating pages from {content_dir} to {public_dir}")
    generate_pages_recursive(content_dir, template_path, public_dir)
    
    print("Static site generation complete!")

if __name__ == "__main__":
    main()