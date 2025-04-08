import unittest
from block_parser import BlockType, block_to_block_type

class TestBlockParser(unittest.TestCase):
    def test_paragraph(self):
        # Test simple paragraph
        block = "This is a simple paragraph of text."
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)
        
        # Test paragraph with multiple lines
        block = "This is a paragraph\nwith multiple lines\nof text."
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)
        
        # Test paragraph with formatting
        block = "This is a paragraph with **bold** and _italic_ text."
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)
    
    def test_heading(self):
        # Test h1
        block = "# Heading Level 1"
        self.assertEqual(block_to_block_type(block), BlockType.HEADING)
        
        # Test h2
        block = "## Heading Level 2"
        self.assertEqual(block_to_block_type(block), BlockType.HEADING)
        
        # Test h6
        block = "###### Heading Level 6"
        self.assertEqual(block_to_block_type(block), BlockType.HEADING)
        
        # Test invalid heading (no space after #)
        block = "#Invalid Heading"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)
        
        # Test invalid heading (too many #)
        block = "####### Too Many Hashtags"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)
    
    def test_code(self):
        # Test simple code block
        block = "```\ncode block\n```"
        self.assertEqual(block_to_block_type(block), BlockType.CODE)
        
        # Test code block with language specification
        block = "```python\ndef hello_world():\n    print('Hello, world!')\n```"
        self.assertEqual(block_to_block_type(block), BlockType.CODE)
        
        # Test invalid code block (missing closing backticks)
        block = "```\ncode block without closing"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)
    
    def test_quote(self):
        # Test simple quote
        block = "> This is a quote"
        self.assertEqual(block_to_block_type(block), BlockType.QUOTE)
        
        # Test multi-line quote
        block = "> This is a quote\n> that spans multiple lines\n> of text."
        self.assertEqual(block_to_block_type(block), BlockType.QUOTE)
        
        # Test invalid quote (missing > on some lines)
        block = "> This is a quote\nBut this line is not a quote"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)
    
    def test_unordered_list(self):
        # Test simple unordered list
        block = "- Item 1\n- Item 2\n- Item 3"
        self.assertEqual(block_to_block_type(block), BlockType.UNORDERED_LIST)
        
        # Test unordered list with formatted items
        block = "- Item with **bold**\n- Item with _italic_\n- Item with `code`"
        self.assertEqual(block_to_block_type(block), BlockType.UNORDERED_LIST)
        
        # Test invalid unordered list (missing space after -)
        block = "-Item 1\n-Item 2"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)
        
        # Test invalid unordered list (mixed with other content)
        block = "- Item 1\nThis is not a list item\n- Item 2"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)
    
    def test_ordered_list(self):
        # Test simple ordered list
        block = "1. Item 1\n2. Item 2\n3. Item 3"
        self.assertEqual(block_to_block_type(block), BlockType.ORDERED_LIST)
        
        # Test ordered list with formatted items
        block = "1. Item with **bold**\n2. Item with _italic_\n3. Item with `code`"
        self.assertEqual(block_to_block_type(block), BlockType.ORDERED_LIST)
        
        # Test invalid ordered list (wrong numbering)
        block = "1. Item 1\n3. Item 2"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)
        
        # Test invalid ordered list (not starting at 1)
        block = "2. Item 1\n3. Item 2"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)
        
        # Test invalid ordered list (missing space after number)
        block = "1.Item 1\n2.Item 2"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)
        
        # Test invalid ordered list (mixed with other content)
        block = "1. Item 1\nThis is not a list item\n2. Item 2"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)
    
    def test_empty_block(self):
        # Test empty block
        block = ""
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)
    
    def test_mixed_content(self):
        # This should be treated as paragraph since it doesn't fully match any specific type
        block = "Some text\n> Quote line\n- List item"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)


if __name__ == "__main__":
    unittest.main()