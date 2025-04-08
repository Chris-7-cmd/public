from htmlnode import TextNode, TextType
from text_processing import split_nodes_delimiter, split_nodes_image, split_nodes_link

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
    nodes = split_nodes_delimiter(nodes, "_", TextType.ITALIC)
    nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)
    nodes = split_nodes_image(nodes)
    # Process links with [text](url) syntax
    nodes = split_nodes_link(nodes)
    
    return nodes