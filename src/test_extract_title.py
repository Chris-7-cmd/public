import unittest
from extract_title import extract_title

class TestExtractTitle(unittest.TestCase):
    def test_extract_simple_title(self):
        markdown = "# Hello"
        self.assertEqual(extract_title(markdown), "Hello")
    
    def test_extract_title_with_whitespace(self):
        markdown = "#    Hello World    "
        self.assertEqual(extract_title(markdown), "Hello World")
    
    def test_extract_title_with_formatting(self):
        markdown = "# Hello **World** with _formatting_"
        self.assertEqual(extract_title(markdown), "Hello **World** with _formatting_")
    
    def test_extract_title_from_multiline(self):
        markdown = """Some text before
# This is the title
Some text after"""
        self.assertEqual(extract_title(markdown), "This is the title")
    
    def test_extract_title_from_complex_document(self):
        markdown = """# Main Title
## Subtitle
Content paragraph

### Sub-section
More content"""
        self.assertEqual(extract_title(markdown), "Main Title")
    
    def test_no_title_raises_exception(self):
        markdown = """No title here
Just some text
## This is h2, not h1"""
        with self.assertRaises(Exception):
            extract_title(markdown)
    
    def test_empty_document_raises_exception(self):
        markdown = ""
        with self.assertRaises(Exception):
            extract_title(markdown)

if __name__ == "__main__":
    unittest.main()