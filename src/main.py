from utility import copy_directory
from page_generator import generate_pages_recursive
import os
import shutil
import sys

def main():
    """
    Main function to run the static site generator
    
    Args:
        basepath: The base path for the site (from command line arguments)
    """
    # Get basepath from command line arguments if provided
    basepath = "/"
    if len(sys.argv) > 1:
        basepath = sys.argv[1]
        if not basepath.endswith('/'):
            basepath += '/'
    
    print(f"Starting static site generator with basepath: {basepath}")
    
    # Define directories
    static_dir = "static"
    output_dir = "docs"  # Changed from 'public' to 'docs' for GitHub Pages
    content_dir = "content"
    template_path = "template.html"
    
    # 1. Delete anything in the output directory
    if os.path.exists(output_dir):
        print(f"Cleaning {output_dir} directory")
        shutil.rmtree(output_dir)
    
    # 2. Copy all the static files from static to output
    print(f"Copying static files from {static_dir} to {output_dir}")
    copy_directory(static_dir, output_dir)
    
    # 3. Generate HTML files for all markdown files in the content directory
    print(f"Generating pages from {content_dir} to {output_dir}")
    generate_pages_recursive(content_dir, template_path, output_dir, basepath)
    
    print("Static site generation complete!")

