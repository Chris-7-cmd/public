from enum import Enum
import re

class BlockType(Enum):
    PARAGRAPH = 1
    HEADING = 2
    CODE = 3
    QUOTE = 4
    UNORDERED_LIST = 5
    ORDERED_LIST = 6

def block_to_block_type(block):
    """
    Determine the type of a markdown block.
    
    Args:
        block: A string containing a block of markdown text
        
    Returns:
        BlockType: The type of the markdown block
    """
    # If the block is empty, it's a paragraph
    if not block.strip():
        return BlockType.PARAGRAPH
    
    # Split the block into lines to check patterns
    lines = block.split("\n")
    first_line = lines[0] if lines else ""
    
    # Check for heading (starts with 1-6 # characters followed by a space)
    if re.match(r"^#{1,6} ", first_line):
        return BlockType.HEADING
    
    # Check for code block (starts and ends with three backticks)
    if block.startswith("```") and block.endswith("```"):
        return BlockType.CODE
    
    # Check for quote block (every line starts with >)
    if all(line.startswith(">") for line in lines if line.strip()):
        # Make sure there's at least one non-empty line
        if any(line.strip() for line in lines):
            return BlockType.QUOTE
    
    # Check for unordered list (every line starts with - followed by a space)
    if all(line.startswith("- ") for line in lines if line.strip()):
        # Make sure there's at least one non-empty line
        if any(line.strip() for line in lines):
            return BlockType.UNORDERED_LIST
    
    # Check for ordered list
    if _is_ordered_list(lines):
        return BlockType.ORDERED_LIST
    
    # Default to paragraph
    return BlockType.PARAGRAPH


def _is_ordered_list(lines):
    """
    Helper function to determine if lines form an ordered list.
    
    An ordered list must:
    - Have each line start with a number followed by a . and a space
    - The numbers must start at 1 and increment by 1 for each line
    
    Args:
        lines: A list of strings representing lines of text
        
    Returns:
        bool: True if the lines form an ordered list, False otherwise
    """
    # Filter out empty lines
    non_empty_lines = [line for line in lines if line.strip()]
    
    if not non_empty_lines:
        return False
    
    # Check if all lines start with a number followed by . and space
    for i, line in enumerate(non_empty_lines, 1):
        if not re.match(f"^{i}\\. ", line):
            return False
    
    return True