import unittest
from htmlnode import HTMLNode, LeafNode, ValueError, TextNode, TextType, text_node_to_html_node

class TestHTMLNode(unittest.TestCase):
    def test_init_with_defaults(self):
        # Test that all parameters default to None
        node = HTMLNode()
        self.assertIsNone(node.tag)
        self.assertIsNone(node.value)
        self.assertIsNone(node.children)
        self.assertIsNone(node.props)
    
    def test_init_with_values(self):
        # Test initialization with values
        tag = "a"
        value = "Click me"
        children = [HTMLNode("span", "child")]
        props = {"href": "https://www.google.com", "target": "_blank"}
        
        node = HTMLNode(tag, value, children, props)
        
        self.assertEqual(node.tag, tag)
        self.assertEqual(node.value, value)
        self.assertEqual(node.children, children)
        self.assertEqual(node.props, props)
    
    def test_props_to_html(self):
        # Test with no props
        node = HTMLNode()
        self.assertEqual(node.props_to_html(), "")
        
        # Test with single prop
        node = HTMLNode(props={"href": "https://www.google.com"})
        self.assertEqual(node.props_to_html(), " href=\"https://www.google.com\"")
        
        # Test with multiple props
        node = HTMLNode(props={"href": "https://www.google.com", "target": "_blank"})
        
        # Since dictionaries don't guarantee order, we need to check both possible orderings
        possible_outputs = [
            " href=\"https://www.google.com\" target=\"_blank\"",
            " target=\"_blank\" href=\"https://www.google.com\""
        ]
        
        self.assertIn(node.props_to_html(), possible_outputs)
    
    def test_to_html_raises_not_implemented(self):
        # Test that to_html raises NotImplementedError
        node = HTMLNode()
        with self.assertRaises(NotImplementedError):
            node.to_html()
    
    def test_repr(self):
        # Test the __repr__ method
        node = HTMLNode("div", "content", [], {"class": "container"})
        expected = "HTMLNode(div, content, [], {'class': 'container'})"
        self.assertEqual(repr(node), expected)


class TestLeafNode(unittest.TestCase):
    def test_init_requires_value(self):
        # Test that LeafNode requires a value
        with self.assertRaises(ValueError):
            LeafNode("p")
        
        # Test that LeafNode can be created with just a value
        node = LeafNode(value="Just some text")
        self.assertIsNone(node.tag)
        self.assertEqual(node.value, "Just some text")
        self.assertIsNone(node.children)
        self.assertIsNone(node.props)
        
        # Test that LeafNode can be created with a tag, value and props
        node = LeafNode("a", "Click me", {"href": "https://www.google.com"})
        self.assertEqual(node.tag, "a")
        self.assertEqual(node.value, "Click me")
        self.assertIsNone(node.children)
        self.assertEqual(node.props, {"href": "https://www.google.com"})
    
    def test_leaf_to_html(self):
        # Test rendering with no tag (raw text)
        node = LeafNode(value="Just some text")
        self.assertEqual(node.to_html(), "Just some text")
        
        # Test rendering with a tag but no props
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")
        
        # Test rendering with a tag and props
        node = LeafNode("a", "Click me", {"href": "https://www.google.com"})
        self.assertEqual(node.to_html(), '<a href="https://www.google.com">Click me</a>')
        
        # Test rendering with more complex props
        node = LeafNode("a", "Click me", {"href": "https://www.google.com", "target": "_blank"})
        # Since dict order isn't guaranteed, we need to check both possible outputs
        possible_outputs = [
            '<a href="https://www.google.com" target="_blank">Click me</a>',
            '<a target="_blank" href="https://www.google.com">Click me</a>'
        ]
        self.assertIn(node.to_html(), possible_outputs)
    
    def test_leaf_to_html_examples(self):
        # Test the specific examples given in the requirements
        node = LeafNode("p", "This is a paragraph of text.")
        self.assertEqual(node.to_html(), "<p>This is a paragraph of text.</p>")
        
        node = LeafNode("a", "Click me!", {"href": "https://www.google.com"})
        self.assertEqual(node.to_html(), '<a href="https://www.google.com">Click me!</a>')


class TestTextNodeToHtmlNode(unittest.TestCase):
    def test_text_type(self):
        # Test TEXT type
        text_node = TextNode("This is a text node", TextType.TEXT)
        html_node = text_node_to_html_node(text_node)
        self.assertIsInstance(html_node, LeafNode)
        self.assertIsNone(html_node.tag)
        self.assertEqual(html_node.value, "This is a text node")
    
    def test_bold_type(self):
        # Test BOLD type
        text_node = TextNode("Bold text", TextType.BOLD)
        html_node = text_node_to_html_node(text_node)
        self.assertIsInstance(html_node, LeafNode)
        self.assertEqual(html_node.tag, "b")
        self.assertEqual(html_node.value, "Bold text")
    
    def test_italic_type(self):
        # Test ITALIC type
        text_node = TextNode("Italic text", TextType.ITALIC)
        html_node = text_node_to_html_node(text_node)
        self.assertIsInstance(html_node, LeafNode)
        self.assertEqual(html_node.tag, "i")
        self.assertEqual(html_node.value, "Italic text")
    
    def test_code_type(self):
        # Test CODE type
        text_node = TextNode("Code text", TextType.CODE)
        html_node = text_node_to_html_node(text_node)
        self.assertIsInstance(html_node, LeafNode)
        self.assertEqual(html_node.tag, "code")
        self.assertEqual(html_node.value, "Code text")
    
    def test_link_type(self):
        # Test LINK type
        text_node = TextNode("Link text", TextType.LINK)
        # Links require a URL
        with self.assertRaises(ValueError):
            text_node_to_html_node(text_node)
        
        text_node.set_url("https://www.example.com")
        html_node = text_node_to_html_node(text_node)
        self.assertIsInstance(html_node, LeafNode)
        self.assertEqual(html_node.tag, "a")
        self.assertEqual(html_node.value, "Link text")
        self.assertEqual(html_node.props, {"href": "https://www.example.com"})
    
    def test_image_type(self):
        # Test IMAGE type
        text_node = TextNode("Image alt text", TextType.IMAGE)
        # Images require a URL
        with self.assertRaises(ValueError):
            text_node_to_html_node(text_node)
        
        text_node.set_url("https://www.example.com/image.jpg")
        html_node = text_node_to_html_node(text_node)
        self.assertIsInstance(html_node, LeafNode)
        self.assertEqual(html_node.tag, "img")
        self.assertEqual(html_node.value, "")  # Empty string value for img tags
        self.assertEqual(html_node.props, {"src": "https://www.example.com/image.jpg", "alt": "Image alt text"})
    
    def test_invalid_node_type(self):
        # Test that a non-TextNode raises an exception
        with self.assertRaises(Exception):
            text_node_to_html_node("Not a TextNode")
    
    def test_example(self):
        # Test the example given in the requirements
        node = TextNode("This is a text node", TextType.TEXT)
        html_node = text_node_to_html_node(node)
        self.assertIsNone(html_node.tag)
        self.assertEqual(html_node.value, "This is a text node")


if __name__ == "__main__":
    unittest.main()