import unittest
from markdown_blocks import markdown_to_blocks

class TestMarkdownToBlocks(unittest.TestCase):
    def test_markdown_to_blocks(self):
        md = """This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items"""
        
        blocks = markdown_to_blocks(md)
        
        expected = [
            "This is **bolded** paragraph",
            "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
            "- This is a list\n- with items"
        ]
        
        self.assertEqual(blocks, expected)
    
    def test_with_headings(self):
        md = """# This is a heading

This is a paragraph of text. It has some **bold** and _italic_ words

- This is the first list item in a list block
- This is a list item
- This is another list item"""
        
        blocks = markdown_to_blocks(md)
        
        expected = [
            "# This is a heading",
            "This is a paragraph of text. It has some **bold** and _italic_ words",
            "- This is the first list item in a list block\n- This is a list item\n- This is another list item"
        ]
        
        self.assertEqual(blocks, expected)
    
    def test_empty_blocks(self):
        md = """First block

  

Second block"""
        
        blocks = markdown_to_blocks(md)
        
        expected = [
            "First block",
            "Second block"
        ]
        
        self.assertEqual(blocks, expected)
    
    def test_multiple_newlines(self):
        md = """Block 1



Block 2




Block 3"""
        
        blocks = markdown_to_blocks(md)
        
        expected = [
            "Block 1",
            "Block 2",
            "Block 3"
        ]
        
        self.assertEqual(blocks, expected)
    
    def test_code_blocks(self):
        md = """Here's some code:

```python
def hello_world():
    print("Hello, world!")
```

And another paragraph."""
        
        blocks = markdown_to_blocks(md)
        
        expected = [
            "Here's some code:",
            "```python\ndef hello_world():\n    print(\"Hello, world!\")\n```",
            "And another paragraph."
        ]
        
        self.assertEqual(blocks, expected)
    
    def test_empty_input(self):
        md = ""
        
        blocks = markdown_to_blocks(md)
        
        expected = []
        
        self.assertEqual(blocks, expected)


if __name__ == "__main__":
    unittest.main()