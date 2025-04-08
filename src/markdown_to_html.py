from htmlnode import HTMLNode, LeafNode, TextNode, TextType
from markdown_blocks import markdown_to_blocks
from block_parser import BlockType, block_to_block_type
import re

def markdown_to_html_node(markdown):
    """
    Convert a markdown string to a parent HTMLNode with nested children.
    
    Args:
        markdown: A string containing markdown text
        
    Returns:
        HTMLNode: A parent div node containing all the HTML elements
    """
    # Split the markdown into blocks
    blocks = markdown_to_blocks(markdown)
    
    # Create a parent div to hold all the blocks
    parent_node = HTMLNode("div", None, [], None)
    
    # Process each block
    for block in blocks:
        # Determine the type of block
        block_type = block_to_block_type(block)
        
        # Create an HTMLNode based on the block type
        if block_type == BlockType.PARAGRAPH:
            node = create_paragraph_node(block)
        elif block_type == BlockType.HEADING:
            node = create_heading_node(block)
        elif block_type == BlockType.CODE:
            node = create_code_node(block)
        elif block_type == BlockType.QUOTE:
            node = create_quote_node(block)
        elif block_type == BlockType.UNORDERED_LIST:
            node = create_unordered_list_node(block)
        elif block_type == BlockType.ORDERED_LIST:
            node = create_ordered_list_node(block)
        else:
            # This shouldn't happen with proper block type detection
            node = create_paragraph_node(block)
        
        # Add the node to the parent
        if parent_node.children is None:
            parent_node.children = []
        parent_node.children.append(node)
    
    return parent_node


def text_to_children(text):
    """
    Convert markdown text to a list of HTMLNode objects representing inline elements.
    
    Args:
        text: A string containing markdown text with inline formatting
        
    Returns:
        list: A list of HTMLNode objects
    """
    # First convert the text to TextNode objects
    text_nodes = text_to_textnodes(text)
    
    # Then convert each TextNode to an HTMLNode
    html_nodes = []
    for text_node in text_nodes:
        html_node = text_node_to_html_node(text_node)
        html_nodes.append(html_node)
    
    return html_nodes


def text_to_textnodes(text):
    """
    Convert markdown text to a list of TextNode objects.
    
    Args:
        text: A string containing markdown text with various formatting
        
    Returns:
        A list of TextNode objects representing the formatted text
    """
    # Start with a single text node
    nodes = [TextNode(text, TextType.TEXT)]
    
    # Split by different delimiters and syntax in sequence
    
    # 1. Process bold text with ** delimiter
    nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)
    
    # 2. Process italic text with _ delimiter
    nodes = split_nodes_delimiter(nodes, "_", TextType.ITALIC)
    
    # 3. Process code blocks with ` delimiter
    nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)
    
    # 4. Process images with ![alt](url) syntax
    nodes = split_nodes_image(nodes)
    
    # 5. Process links with [text](url) syntax
    nodes = split_nodes_link(nodes)
    
    return nodes


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
                # No closing delimiter found, treat as plain text
                new_nodes.append(old_node)
                return new_nodes
            
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
    
    # Filter out image matches (those preceded by !)
    return [(anchor, url) for anchor, url in matches if not re.search(f"!\[{re.escape(anchor)}\]\({re.escape(url)}\)", text)]


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
            image_node.url = url
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
            link_node.url = url
            new_nodes.append(link_node)
            
            # Update remaining text
            remaining_text = remaining_text[start_pos + len(link_syntax):]
        
        # Add any remaining text
        if remaining_text:
            new_nodes.append(TextNode(remaining_text, TextType.TEXT))
    
    return new_nodes


def text_node_to_html_node(text_node):
    """
    Convert a TextNode to an HTMLNode.
    
    Args:
        text_node: A TextNode object
        
    Returns:
        HTMLNode: An HTMLNode representing the TextNode
    """
    if text_node.text_type == TextType.TEXT:
        return LeafNode(None, text_node.text)
    
    elif text_node.text_type == TextType.BOLD:
        return LeafNode("b", text_node.text)
    
    elif text_node.text_type == TextType.ITALIC:
        return LeafNode("i", text_node.text)
    
    elif text_node.text_type == TextType.CODE:
        return LeafNode("code", text_node.text)
    
    elif text_node.text_type == TextType.LINK:
        return LeafNode("a", text_node.text, {"href": text_node.url})
    
    elif text_node.text_type == TextType.IMAGE:
        return LeafNode("img", "", {"src": text_node.url, "alt": text_node.text})
    
    else:
        raise ValueError(f"Invalid TextType: {text_node.text_type}")


def create_paragraph_node(block):
    """
    Create an HTMLNode for a paragraph block.
    
    Args:
        block: A string containing the paragraph text
        
    Returns:
        HTMLNode: An HTMLNode with tag 'p' and children representing the inline elements
    """
    children = text_to_children(block)
    return HTMLNode("p", None, children, None)


def create_heading_node(block):
    """
    Create an HTMLNode for a heading block.
    
    Args:
        block: A string containing the heading text
        
    Returns:
        HTMLNode: An HTMLNode with tag 'h1'-'h6' and children representing the inline elements
    """
    # Determine the heading level (h1-h6) by counting # characters
    match = re.match(r"^(#{1,6})\s+", block)
    level = len(match.group(1)) if match else 1
    
    # Remove the # characters and space from the text
    text = block.lstrip("#").lstrip()
    
    children = text_to_children(text)
    return HTMLNode(f"h{level}", None, children, None)


def create_code_node(block):
    """
    Create an HTMLNode for a code block.
    
    Args:
        block: A string containing the code text with triple backtick delimiters
        
    Returns:
        HTMLNode: A nested HTMLNode with pre and code tags
    """
    # Remove the triple backticks and any language specification
    lines = block.split("\n")
    if len(lines) >= 2:  # Multiple lines
        # Skip the first and last lines (which contain the backticks)
        code_content = "\n".join(lines[1:-1])
    else:  # Single line (shouldn't happen with proper markdown, but just in case)
        code_content = block.strip("`").strip()
    
    # Create a leaf node for the code content without processing inline markdown
    code_node = LeafNode("code", code_content)
    
    # Wrap in a pre tag
    return HTMLNode("pre", None, [code_node], None)


def create_quote_node(block):
    """
    Create an HTMLNode for a quote block.
    
    Args:
        block: A string containing the quote text with > characters
        
    Returns:
        HTMLNode: An HTMLNode with tag 'blockquote' and children representing the inline elements
    """
    # Remove the > characters from each line
    lines = block.split("\n")
    processed_lines = [line.lstrip(">").lstrip() for line in lines]
    processed_block = "\n".join(processed_lines)
    
    children = text_to_children(processed_block)
    return HTMLNode("blockquote", None, children, None)


def create_unordered_list_node(block):
    """
    Create an HTMLNode for an unordered list block.
    
    Args:
        block: A string containing the list items with - characters
        
    Returns:
        HTMLNode: An HTMLNode with tag 'ul' and children representing list items
    """
    lines = block.split("\n")
    list_items = []
    
    for line in lines:
        if line.strip():
            # Remove the - character and space from the line
            item_text = line.lstrip("-").lstrip()
            item_children = text_to_children(item_text)
            list_items.append(HTMLNode("li", None, item_children, None))
    
    return HTMLNode("ul", None, list_items, None)


def create_ordered_list_node(block):
    """
    Create an HTMLNode for an ordered list block.
    
    Args:
        block: A string containing the list items with numbers
        
    Returns:
        HTMLNode: An HTMLNode with tag 'ol' and children representing list items
    """
    lines = block.split("\n")
    list_items = []
    
    for line in lines:
        if line.strip():
            # Remove the number, period, and space from the line
            match = re.match(r"^\d+\.\s+(.*)$", line)
            if match:
                item_text = match.group(1)
                item_children = text_to_children(item_text)
                list_items.append(HTMLNode("li", None, item_children, None))
    
    return HTMLNode("ol", None, list_items, None)