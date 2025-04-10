from utility import copy_directory
from page_generator import generate_pages_recursive
import os
import shutil
import sys


def main():
    """
    Main function to run the static site generator
    """
    print("Starting static site generator...")
    
    # Get basepath from command line argument or default to '/'
    basepath = sys.argv[1] if len(sys.argv) > 1 else "/"
    print(f"Using basepath: {basepath}")
    
    # Define directories
    static_dir = "static"
    docs_dir = "docs"  # Changed from public to docs for GitHub Pages
    content_dir = "content"
    template_path = "template.html"
    
    # 1. Delete anything in the docs directory if it exists
    if os.path.exists(docs_dir):
        print(f"Cleaning {docs_dir} directory")
        shutil.rmtree(docs_dir)
    
    # 2. Copy all the static files from static to docs
    print(f"Copying static files from {static_dir} to {docs_dir}")
    copy_directory(static_dir, docs_dir)
    
    # 3. Generate HTML files for all markdown files in the content directory
    print(f"Generating pages from {content_dir} to {docs_dir}")
    generate_pages_recursive(content_dir, template_path, docs_dir, basepath)
    
    print("Static site generation complete!")

if __name__ == "__main__":
    main()

