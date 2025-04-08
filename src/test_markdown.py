import unittest
from markdown import extract_markdown_images, extract_markdown_links

class TestMarkdownParser(unittest.TestCase):
    def test_extract_markdown_images(self):
        # Test extracting a single image
        text = "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        expected = [("image", "https://i.imgur.com/zjjcJKZ.png")]
        self.assertListEqual(extract_markdown_images(text), expected)
        
        # Test extracting multiple images
        text = "Images: ![img1](https://example.com/img1.jpg) and ![img2](https://example.com/img2.png)"
        expected = [
            ("img1", "https://example.com/img1.jpg"),
            ("img2", "https://example.com/img2.png")
        ]
        self.assertListEqual(extract_markdown_images(text), expected)
        
        # Test with empty alt text
        text = "Empty alt: ![](https://example.com/empty.jpg)"
        expected = [("", "https://example.com/empty.jpg")]
        self.assertListEqual(extract_markdown_images(text), expected)
        
        # Test with no images
        text = "No images here, just [a link](https://example.com)"
        expected = []
        self.assertListEqual(extract_markdown_images(text), expected)
        
        # Test with the example from the requirements
        text = "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif)"
        expected = [("rick roll", "https://i.imgur.com/aKaOqIh.gif")]
        self.assertListEqual(extract_markdown_images(text), expected)
        
        # Test with special characters in alt text
        text = "Special chars: ![image with (brackets)](https://example.com/special.jpg)"
        expected = [("image with (brackets)", "https://example.com/special.jpg")]
        self.assertListEqual(extract_markdown_images(text), expected)
    
    def test_extract_markdown_links(self):
        # Test extracting a single link
        text = "This is text with a [link](https://example.com)"
        expected = [("link", "https://example.com")]
        self.assertListEqual(extract_markdown_links(text), expected)
        
        # Test extracting multiple links
        text = "Links: [link1](https://example1.com) and [link2](https://example2.com)"
        expected = [
            ("link1", "https://example1.com"),
            ("link2", "https://example2.com")
        ]
        self.assertListEqual(extract_markdown_links(text), expected)
        
        # Test with empty anchor text
        text = "Empty anchor: [](https://example.com/empty)"
        expected = [("", "https://example.com/empty")]
        self.assertListEqual(extract_markdown_links(text), expected)
        
        # Test with no links
        text = "No links here, just plain text"
        expected = []
        self.assertListEqual(extract_markdown_links(text), expected)
        
        # Test with the example from the requirements
        text = "This is text with a link [to boot dev](https://www.boot.dev)"
        expected = [("to boot dev", "https://www.boot.dev")]
        self.assertListEqual(extract_markdown_links(text), expected)
        
        # Test with special characters in anchor text
        text = "Special chars: [link with (brackets)](https://example.com/special)"
        expected = [("link with (brackets)", "https://example.com/special")]
        self.assertListEqual(extract_markdown_links(text), expected)
        
        
        
        


if __name__ == "__main__":
    unittest.main()