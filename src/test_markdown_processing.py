import unittest
from htmlnode import TextNode, TextType
from markdown_processing import text_to_textnodes

class TestTextToTextnodes(unittest.TestCase):
    def test_simple_text(self):
        # Test with simple plain text
        text = "This is simple text"
        nodes = text_to_textnodes(text)
        
        self.assertEqual(len(nodes), 1)
        self.assertEqual(nodes[0].text, "This is simple text")
        self.assertEqual(nodes[0].text_type, TextType.TEXT)
    
    def test_bold_text(self):
        # Test with bold text
        text = "This is **bold** text"
        nodes = text_to_textnodes(text)
        
        self.assertEqual(len(nodes), 3)
        self.assertEqual(nodes[0].text, "This is ")
        self.assertEqual(nodes[0].text_type, TextType.TEXT)
        self.assertEqual(nodes[1].text, "bold")
        self.assertEqual(nodes[1].text_type, TextType.BOLD)
        self.assertEqual(nodes[2].text, " text")
        self.assertEqual(nodes[2].text_type, TextType.TEXT)
    
    def test_italic_text(self):
        # Test with italic text
        text = "This is _italic_ text"
        nodes = text_to_textnodes(text)
        
        self.assertEqual(len(nodes), 3)
        self.assertEqual(nodes[0].text, "This is ")
        self.assertEqual(nodes[0].text_type, TextType.TEXT)
        self.assertEqual(nodes[1].text, "italic")
        self.assertEqual(nodes[1].text_type, TextType.ITALIC)
        self.assertEqual(nodes[2].text, " text")
        self.assertEqual(nodes[2].text_type, TextType.TEXT)
    
    def test_code_text(self):
        # Test with code blocks
        text = "This is `code` text"
        nodes = text_to_textnodes(text)
        
        self.assertEqual(len(nodes), 3)
        self.assertEqual(nodes[0].text, "This is ")
        self.assertEqual(nodes[0].text_type, TextType.TEXT)
        self.assertEqual(nodes[1].text, "code")
        self.assertEqual(nodes[1].text_type, TextType.CODE)
        self.assertEqual(nodes[2].text, " text")
        self.assertEqual(nodes[2].text_type, TextType.TEXT)
    
    def test_image(self):
        # Test with image
        text = "This is an ![image](https://example.com/img.jpg)"
        nodes = text_to_textnodes(text)
        
        self.assertEqual(len(nodes), 2)
        self.assertEqual(nodes[0].text, "This is an ")
        self.assertEqual(nodes[0].text_type, TextType.TEXT)
        self.assertEqual(nodes[1].text, "image")
        self.assertEqual(nodes[1].text_type, TextType.IMAGE)
        self.assertEqual(nodes[1].url, "https://example.com/img.jpg")
    
    def test_link(self):
        # Test with link
        text = "This is a [link](https://example.com)"
        nodes = text_to_textnodes(text)
        
        self.assertEqual(len(nodes), 2)
        self.assertEqual(nodes[0].text, "This is a ")
        self.assertEqual(nodes[0].text_type, TextType.TEXT)
        self.assertEqual(nodes[1].text, "link")
        self.assertEqual(nodes[1].text_type, TextType.LINK)
        self.assertEqual(nodes[1].url, "https://example.com")
    
    def test_complex_example(self):
        # Test with the complex example from the requirements
        text = "This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4vk.jpg) and a [link](https://boot.dev)"
        nodes = text_to_textnodes(text)
        
        # Create expected nodes properly
        expected_nodes = [
            TextNode("This is ", TextType.TEXT),
            TextNode("text", TextType.BOLD),
            TextNode(" with an ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" word and a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" and an ", TextType.TEXT),
            TextNode("obi wan image", TextType.IMAGE),  # URL set below
            TextNode(" and a ", TextType.TEXT),
            TextNode("link", TextType.LINK)  # URL set below
        ]
        # Set URLs separately
        expected_nodes[7].set_url("https://i.imgur.com/fJRm4vk.jpg")
        expected_nodes[9].set_url("https://boot.dev")
        
        self.assertEqual(len(nodes), len(expected_nodes))
        
        for i, (node, expected) in enumerate(zip(nodes, expected_nodes)):
            self.assertEqual(node.text, expected.text, f"Text mismatch at node {i}")
            self.assertEqual(node.text_type, expected.text_type, f"Type mismatch at node {i}")
            
            # Check URLs for IMAGE and LINK types
            if expected.text_type in (TextType.LINK, TextType.IMAGE):
                self.assertEqual(node.url, expected.url, f"URL mismatch at node {i}")
    
    


if __name__ == "__main__":
    unittest.main()