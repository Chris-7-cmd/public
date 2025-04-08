def markdown_to_blocks(markdown):
    """
    Split a markdown string into blocks based on double newlines.
    
    Args:
        markdown: A string containing markdown text
        
    Returns:
        A list of strings, each representing a markdown block
    """
    # Split the markdown by double newlines to get blocks
    # The regex '\n\n+' matches two or more consecutive newlines
    blocks = markdown.split("\n\n")
    
    # Process each block
    processed_blocks = []
    for block in blocks:
        # Strip leading and trailing whitespace
        block = block.strip()
        
        # Skip empty blocks
        if block:
            processed_blocks.append(block)
    
    return processed_blocks