import os
from markdown_to_html import markdown_to_html_node
from extract_title import extract_title

def generate_page(from_path, template_path, dest_path):
    """
    Generate an HTML page from a markdown file using a template.
    
    Args:
        from_path: Path to the markdown file
        template_path: Path to the HTML template file
        dest_path: Path where the generated HTML file will be saved
    """
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    
    # Read the markdown file
    with open(from_path, 'r', encoding='utf-8') as file:
        markdown_content = file.read()
    
    # Read the template file
    with open(template_path, 'r', encoding='utf-8') as file:
        template_content = file.read()
    
    # Extract the title from the markdown
    title = extract_title(markdown_content)
    
    # Convert markdown to HTML
    html_node = markdown_to_html_node(markdown_content)
    html_content = html_node.to_html()
    
    # Replace placeholders in the template
    full_html = template_content.replace('{{ Title }}', title).replace('{{ Content }}', html_content)
    
    # Create destination directory if it doesn't exist
    os.makedirs(os.path.dirname(dest_path), exist_ok=True)
    
    # Write the new HTML page to the destination path
    with open(dest_path, 'w', encoding='utf-8') as file:
        file.write(full_html)
    
    print(f"Successfully generated {dest_path}")

def generate_pages_recursive(dir_path_content, template_path, dest_dir_path, basepath="/"):
    """
    Recursively generate HTML pages from markdown files in a directory.
    
    Args:
        dir_path_content: Path to the content directory containing markdown files
        template_path: Path to the HTML template file
        dest_dir_path: Path to the destination directory for generated HTML files
        basepath: Base path for the site (default: '/')
    """
    print(f"Crawling directory: {dir_path_content}")
    
    # Ensure the destination directory exists
    os.makedirs(dest_dir_path, exist_ok=True)
    
    # Walk through all entries in the content directory
    for root, dirs, files in os.walk(dir_path_content):
        for filename in files:
            # Check if the file is a markdown file
            if filename.endswith('.md'):
                # Get the full path to the markdown file
                markdown_path = os.path.join(root, filename)
                
                # Calculate the relative path from content directory to the markdown file
                rel_path = os.path.relpath(markdown_path, dir_path_content)
                
                # Determine the output HTML path
                if filename == 'index.md':
                    # For index.md files, maintain the directory structure
                    output_dir = os.path.join(dest_dir_path, os.path.dirname(rel_path))
                    output_path = os.path.join(output_dir, 'index.html')
                else:
                    # For other markdown files, replace .md with .html
                    output_dir = os.path.join(dest_dir_path, os.path.dirname(rel_path))
                    output_name = os.path.splitext(filename)[0] + '.html'
                    output_path = os.path.join(output_dir, output_name)
                
                # Create the output directory if it doesn't exist
                os.makedirs(output_dir, exist_ok=True)
                
                # Generate the HTML page
                generate_page(markdown_path, template_path, output_path, basepath)
    
    print(f"Completed recursive page generation from {dir_path_content} to {dest_dir_path}")