import re

def extract_markdown_images(text):
    """
    Extract all markdown images from text.
    
    Args:
        text: A string containing markdown text
        
    Returns:
        A list of tuples, each containing (alt_text, url)
    """
    # Regex pattern for markdown images: ![alt text](url)
    pattern = r"!\[(.*?)\]\((.*?)\)"
    matches = re.findall(pattern, text)
    return matches

def extract_markdown_links(text):
    """
    Extract all markdown links from text.
    
    Args:
        text: A string containing markdown text
        
    Returns:
        A list of tuples, each containing (anchor_text, url)
    """
    # Regex pattern for markdown links: [anchor text](url)
    pattern = r"\[(.*?)\]\((.*?)\)"
    matches = re.findall(pattern, text)
    return matches