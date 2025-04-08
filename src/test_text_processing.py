import unittest
from htmlnode import TextNode, TextType
from text_processing import split_nodes_delimiter, split_nodes_image, split_nodes_link

class TestSplitNodesDelimiter(unittest.TestCase):
    def test_code_delimiter(self):
        # Test splitting with code blocks using backtick delimiters
        node = TextNode("This is text with a `code block` word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        
        self.assertEqual(len(new_nodes), 3)
        self.assertEqual(new_nodes[0].text, "This is text with a ")
        self.assertEqual(new_nodes[0].text_type, TextType.TEXT)
        self.assertEqual(new_nodes[1].text, "code block")
        self.assertEqual(new_nodes[1].text_type, TextType.CODE)
        self.assertEqual(new_nodes[2].text, " word")
        self.assertEqual(new_nodes[2].text_type, TextType.TEXT)
    
    def test_bold_delimiter(self):
        # Test splitting with bold text using ** delimiters
        node = TextNode("Normal text with **bold text** in it", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        
        self.assertEqual(len(new_nodes), 3)
        self.assertEqual(new_nodes[0].text, "Normal text with ")
        self.assertEqual(new_nodes[0].text_type, TextType.TEXT)
        self.assertEqual(new_nodes[1].text, "bold text")
        self.assertEqual(new_nodes[1].text_type, TextType.BOLD)
        self.assertEqual(new_nodes[2].text, " in it")
        self.assertEqual(new_nodes[2].text_type, TextType.TEXT)
    
    def test_italic_delimiter(self):
        # Test splitting with italic text using _ delimiters
        node = TextNode("Normal text with _italic text_ in it", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "_", TextType.ITALIC)
        
        self.assertEqual(len(new_nodes), 3)
        self.assertEqual(new_nodes[0].text, "Normal text with ")
        self.assertEqual(new_nodes[0].text_type, TextType.TEXT)
        self.assertEqual(new_nodes[1].text, "italic text")
        self.assertEqual(new_nodes[1].text_type, TextType.ITALIC)
        self.assertEqual(new_nodes[2].text, " in it")
        self.assertEqual(new_nodes[2].text_type, TextType.TEXT)
    
    def test_multiple_delimiters(self):
        # Test with multiple instances of the same delimiter
        node = TextNode("Text with `code1` and `code2` blocks", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        
        self.assertEqual(len(new_nodes), 5)
        self.assertEqual(new_nodes[0].text, "Text with ")
        self.assertEqual(new_nodes[1].text, "code1")
        self.assertEqual(new_nodes[1].text_type, TextType.CODE)
        self.assertEqual(new_nodes[2].text, " and ")
        self.assertEqual(new_nodes[3].text, "code2")
        self.assertEqual(new_nodes[3].text_type, TextType.CODE)
        self.assertEqual(new_nodes[4].text, " blocks")
    
    def test_delimiter_at_start(self):
        # Test with delimiter at the start of the text
        node = TextNode("`code` at the start", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        
        self.assertEqual(len(new_nodes), 2)
        self.assertEqual(new_nodes[0].text, "code")
        self.assertEqual(new_nodes[0].text_type, TextType.CODE)
        self.assertEqual(new_nodes[1].text, " at the start")
    
    def test_delimiter_at_end(self):
        # Test with delimiter at the end of the text
        node = TextNode("At the end `code`", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        
        self.assertEqual(len(new_nodes), 2)
        self.assertEqual(new_nodes[0].text, "At the end ")
        self.assertEqual(new_nodes[1].text, "code")
        self.assertEqual(new_nodes[1].text_type, TextType.CODE)
    
    def test_non_text_nodes(self):
        # Test with a mix of TEXT and non-TEXT nodes
        text_node = TextNode("Text with `code`", TextType.TEXT)
        bold_node = TextNode("Already bold", TextType.BOLD)
        
        new_nodes = split_nodes_delimiter([text_node, bold_node], "`", TextType.CODE)
        
        self.assertEqual(len(new_nodes), 3)
        self.assertEqual(new_nodes[0].text, "Text with ")
        self.assertEqual(new_nodes[1].text, "code")
        self.assertEqual(new_nodes[1].text_type, TextType.CODE)
        self.assertEqual(new_nodes[2].text, "Already bold")
        self.assertEqual(new_nodes[2].text_type, TextType.BOLD)
    
    def test_empty_text_between_delimiters(self):
        # Test with empty text between delimiters
        node = TextNode("Text with `` empty code", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        
        self.assertEqual(len(new_nodes), 2)
        self.assertEqual(new_nodes[0].text, "Text with ")
        self.assertEqual(new_nodes[1].text, " empty code")
    
    def test_missing_closing_delimiter(self):
        # Test with missing closing delimiter
        node = TextNode("Text with `unclosed code", TextType.TEXT)
        
        with self.assertRaises(Exception):
            split_nodes_delimiter([node], "`", TextType.CODE)
    
    def test_complex_mixed_content(self):
        # Test with a more complex mix of content
        nodes = [
            TextNode("Normal text", TextType.TEXT),
            TextNode("Bold text", TextType.BOLD),
            TextNode("Text with `code` in it", TextType.TEXT)
        ]
        
        new_nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)
        
        self.assertEqual(len(new_nodes), 5)
        self.assertEqual(new_nodes[0].text, "Normal text")
        self.assertEqual(new_nodes[1].text, "Bold text")
        self.assertEqual(new_nodes[1].text_type, TextType.BOLD)
        self.assertEqual(new_nodes[2].text, "Text with ")
        self.assertEqual(new_nodes[3].text, "code")
        self.assertEqual(new_nodes[3].text_type, TextType.CODE)
        self.assertEqual(new_nodes[4].text, " in it")


class TestSplitNodesImage(unittest.TestCase):
    def test_single_image(self):
        # Test with a single image
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)",
            TextType.TEXT
        )
        new_nodes = split_nodes_image([node])
        
        self.assertEqual(len(new_nodes), 2)
        self.assertEqual(new_nodes[0].text, "This is text with an ")
        self.assertEqual(new_nodes[0].text_type, TextType.TEXT)
        self.assertEqual(new_nodes[1].text, "image")
        self.assertEqual(new_nodes[1].text_type, TextType.IMAGE)
        self.assertEqual(new_nodes[1].url, "https://i.imgur.com/zjjcJKZ.png")
    
    def test_multiple_images(self):
        # Test with multiple images
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3e1NKJW.jpg)",
            TextType.TEXT
        )
        new_nodes = split_nodes_image([node])
        
        self.assertEqual(len(new_nodes), 4)
        self.assertEqual(new_nodes[0].text, "This is text with an ")
        self.assertEqual(new_nodes[1].text, "image")
        self.assertEqual(new_nodes[1].text_type, TextType.IMAGE)
        self.assertEqual(new_nodes[1].url, "https://i.imgur.com/zjjcJKZ.png")
        self.assertEqual(new_nodes[2].text, " and another ")
        self.assertEqual(new_nodes[3].text, "second image")
        self.assertEqual(new_nodes[3].text_type, TextType.IMAGE)
        self.assertEqual(new_nodes[3].url, "https://i.imgur.com/3e1NKJW.jpg")
    
    def test_no_images(self):
        # Test with no images
        node = TextNode("This is text with no images", TextType.TEXT)
        new_nodes = split_nodes_image([node])
        
        self.assertEqual(len(new_nodes), 1)
        self.assertEqual(new_nodes[0], node)
    
    def test_image_at_start(self):
        # Test with an image at the start
        node = TextNode("![image](https://example.com/img.jpg) at the start", TextType.TEXT)
        new_nodes = split_nodes_image([node])
        
        self.assertEqual(len(new_nodes), 2)
        self.assertEqual(new_nodes[0].text, "image")
        self.assertEqual(new_nodes[0].text_type, TextType.IMAGE)
        self.assertEqual(new_nodes[0].url, "https://example.com/img.jpg")
        self.assertEqual(new_nodes[1].text, " at the start")
    
    def test_image_at_end(self):
        # Test with an image at the end
        node = TextNode("At the end ![image](https://example.com/img.jpg)", TextType.TEXT)
        new_nodes = split_nodes_image([node])
        
        self.assertEqual(len(new_nodes), 2)
        self.assertEqual(new_nodes[0].text, "At the end ")
        self.assertEqual(new_nodes[1].text, "image")
        self.assertEqual(new_nodes[1].text_type, TextType.IMAGE)
        self.assertEqual(new_nodes[1].url, "https://example.com/img.jpg")
    
    def test_non_text_nodes(self):
        # Test with a mix of TEXT and non-TEXT nodes
        text_node = TextNode("Text with ![image](https://example.com/img.jpg)", TextType.TEXT)
        bold_node = TextNode("Already bold", TextType.BOLD)
        
        new_nodes = split_nodes_image([text_node, bold_node])
        
        self.assertEqual(len(new_nodes), 3)
        self.assertEqual(new_nodes[0].text, "Text with ")
        self.assertEqual(new_nodes[1].text, "image")
        self.assertEqual(new_nodes[1].text_type, TextType.IMAGE)
        self.assertEqual(new_nodes[1].url, "https://example.com/img.jpg")
        self.assertEqual(new_nodes[2].text, "Already bold")
        self.assertEqual(new_nodes[2].text_type, TextType.BOLD)
    
    def test_empty_alt_text(self):
        # Test with empty alt text
        node = TextNode("Image with ![](https://example.com/img.jpg) empty alt", TextType.TEXT)
        new_nodes = split_nodes_image([node])
        
        self.assertEqual(len(new_nodes), 3)
        self.assertEqual(new_nodes[0].text, "Image with ")
        self.assertEqual(new_nodes[1].text, "")
        self.assertEqual(new_nodes[1].text_type, TextType.IMAGE)
        self.assertEqual(new_nodes[1].url, "https://example.com/img.jpg")
        self.assertEqual(new_nodes[2].text, " empty alt")


class TestSplitNodesLink(unittest.TestCase):
    def test_single_link(self):
        # Test with a single link
        node = TextNode(
            "This is text with a link [to boot dev](https://www.boot.dev)",
            TextType.TEXT
        )
        new_nodes = split_nodes_link([node])
        
        self.assertEqual(len(new_nodes), 2)
        self.assertEqual(new_nodes[0].text, "This is text with a link ")
        self.assertEqual(new_nodes[0].text_type, TextType.TEXT)
        self.assertEqual(new_nodes[1].text, "to boot dev")
        self.assertEqual(new_nodes[1].text_type, TextType.LINK)
        self.assertEqual(new_nodes[1].url, "https://www.boot.dev")
    
    def test_multiple_links(self):
        # Test with multiple links
        node = TextNode(
            "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)",
            TextType.TEXT
        )
        new_nodes = split_nodes_link([node])
        
        self.assertEqual(len(new_nodes), 4)
        self.assertEqual(new_nodes[0].text, "This is text with a link ")
        self.assertEqual(new_nodes[1].text, "to boot dev")
        self.assertEqual(new_nodes[1].text_type, TextType.LINK)
        self.assertEqual(new_nodes[1].url, "https://www.boot.dev")
        self.assertEqual(new_nodes[2].text, " and ")
        self.assertEqual(new_nodes[3].text, "to youtube")
        self.assertEqual(new_nodes[3].text_type, TextType.LINK)
        self.assertEqual(new_nodes[3].url, "https://www.youtube.com/@bootdotdev")
    
    def test_no_links(self):
        # Test with no links
        node = TextNode("This is text with no links", TextType.TEXT)
        new_nodes = split_nodes_link([node])
        
        self.assertEqual(len(new_nodes), 1)
        self.assertEqual(new_nodes[0], node)
    
if __name__ == "__main__":
    unittest.main()