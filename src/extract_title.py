def extract_title(markdown):
    """
    Extract the h1 header (title) from a markdown string.
    
    Args:
        markdown: A string containing markdown text
        
    Returns:
        The title without the # prefix and leading/trailing whitespace,
        or raises an exception if no h1 header is found
    """
    # Split the markdown into lines
    lines = markdown.split('\n')
    
    # Look for a line that starts with a single #
    for line in lines:
        if line.strip().startswith('# '):
            # Extract the title (remove the # and any leading/trailing whitespace)
            title = line.strip()[2:].strip()
            return title
    
    # If no h1 header is found, raise an exception
    raise Exception("No h1 header found in markdown")