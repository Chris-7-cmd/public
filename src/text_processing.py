from htmlnode import TextNode, TextType
from markdown import extract_markdown_images, extract_markdown_links

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    """
    Split TextNodes of type TEXT based on the given delimiter and text_type.
    
    Args:
        old_nodes: List of TextNode objects
        delimiter: String delimiter to split on (e.g., "**", "`", "_")
        text_type: TextType enum value to apply to text between delimiters
        
    Returns:
        List of TextNode objects with TEXT nodes split based on delimiters
    """
    new_nodes = []
    
    for old_node in old_nodes:
        # Only process TEXT type nodes, add others as-is
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue
        
        # Process the text for this node
        text = old_node.text
        
        # Check if the delimiter exists in the text
        if delimiter not in text:
            new_nodes.append(old_node)
            continue
        
        # Split the text by the delimiter
        segments = []
        remaining_text = text
        
        while delimiter in remaining_text:
            # Find the first occurrence of the delimiter
            start_pos = remaining_text.find(delimiter)
            
            # Add text before the delimiter if it exists
            if start_pos > 0:
                segments.append((remaining_text[:start_pos], TextType.TEXT))
            
            # Find the closing delimiter
            remaining_text = remaining_text[start_pos + len(delimiter):]
            end_pos = remaining_text.find(delimiter)
            
            if end_pos == -1:
                # No closing delimiter found, raise an exception
                raise Exception(f"Missing closing delimiter '{delimiter}' in '{text}'")
            
            # Add the text between delimiters with the specified type
            segments.append((remaining_text[:end_pos], text_type))
            
            # Update remaining text
            remaining_text = remaining_text[end_pos + len(delimiter):]
        
        # Add any remaining text
        if remaining_text:
            segments.append((remaining_text, TextType.TEXT))
        
        # Create TextNode objects from the segments
        for segment_text, segment_type in segments:
            if segment_text:  # Only create nodes for non-empty text
                new_nodes.append(TextNode(segment_text, segment_type))
    
    return new_nodes


def split_nodes_image(old_nodes):
    """
    Split TextNodes of type TEXT that contain markdown image syntax ![alt](url).
    
    Args:
        old_nodes: List of TextNode objects
    
    Returns:
        List of TextNode objects with markdown images converted to IMAGE nodes
    """
    new_nodes = []
    
    for old_node in old_nodes:
        # Only process TEXT type nodes, add others as-is
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue
        
        # Process the text for this node
        text = old_node.text
        
        # Extract all markdown images
        images = extract_markdown_images(text)
        
        if not images:
            # No images found, keep the node as is
            new_nodes.append(old_node)
            continue
        
        # Process text with images
        remaining_text = text
        
        for alt_text, url in images:
            # Find the position of the image syntax
            image_syntax = f"![{alt_text}]({url})"
            start_pos = remaining_text.find(image_syntax)
            
            if start_pos == -1:
                # This shouldn't happen if extract_markdown_images is working correctly
                continue
            
            # Add text before the image if it exists
            if start_pos > 0:
                new_nodes.append(TextNode(remaining_text[:start_pos], TextType.TEXT))
            
            # Add the image node
            image_node = TextNode(alt_text, TextType.IMAGE)
            image_node.set_url(url)
            new_nodes.append(image_node)
            
            # Update remaining text
            remaining_text = remaining_text[start_pos + len(image_syntax):]
        
        # Add any remaining text
        if remaining_text:
            new_nodes.append(TextNode(remaining_text, TextType.TEXT))
    
    return new_nodes


def split_nodes_link(old_nodes):
    """
    Split TextNodes of type TEXT that contain markdown link syntax [text](url).
    
    Args:
        old_nodes: List of TextNode objects
    
    Returns:
        List of TextNode objects with markdown links converted to LINK nodes
    """
    new_nodes = []
    
    for old_node in old_nodes:
        # Only process TEXT type nodes, add others as-is
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue
        
        # Process the text for this node
        text = old_node.text
        
        # Extract all markdown links (but not images)
        links = extract_markdown_links(text)
        # Filter out any image matches that might have been caught
        links = [(anchor, url) for anchor, url in links if not text.find(f"![{anchor}]({url})") >= 0]
        
        if not links:
            # No links found, keep the node as is
            new_nodes.append(old_node)
            continue
        
        # Process text with links
        remaining_text = text
        
        for anchor_text, url in links:
            # Find the position of the link syntax
            link_syntax = f"[{anchor_text}]({url})"
            start_pos = remaining_text.find(link_syntax)
            
            if start_pos == -1:
                # This shouldn't happen if extract_markdown_links is working correctly
                continue
            
            # Add text before the link if it exists
            if start_pos > 0:
                new_nodes.append(TextNode(remaining_text[:start_pos], TextType.TEXT))
            
            # Add the link node
            link_node = TextNode(anchor_text, TextType.LINK)
            link_node.set_url(url)
            new_nodes.append(link_node)
            
            # Update remaining text
            remaining_text = remaining_text[start_pos + len(link_syntax):]
        
        # Add any remaining text
        if remaining_text:
            new_nodes.append(TextNode(remaining_text, TextType.TEXT))
    
    return new_nodes