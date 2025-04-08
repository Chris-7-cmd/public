import unittest
from markdown_to_html import markdown_to_html_node

class TestMarkdownProcessor(unittest.TestCase):
    def test_paragraphs(self):
        md = """This is **bolded** paragraph
text in a p
tag here

This is another paragraph with _italic_ text and `code` here"""
        
        node = markdown_to_html_node(md)
        html = node.to_html()
        
        expected = "<div><p>This is <b>bolded</b> paragraph\ntext in a p\ntag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>"
        self.assertEqual(html, expected)
    
    def test_codeblock(self):
        md = """```
This is text that _should_ remain
the **same** even with inline stuff
```"""
        
        node = markdown_to_html_node(md)
        html = node.to_html()
        
        expected = "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff</code></pre></div>"
        self.assertEqual(html, expected)
    
    def test_headings(self):
        md = """# Heading 1

## Heading 2

### Heading 3 with **bold**"""
        
        node = markdown_to_html_node(md)
        html = node.to_html()
        
        expected = "<div><h1>Heading 1</h1><h2>Heading 2</h2><h3>Heading 3 with <b>bold</b></h3></div>"
        self.assertEqual(html, expected)
    
    def test_quotes(self):
        md = """> This is a quote
> With multiple lines
> And some **formatting**"""
        
        node = markdown_to_html_node(md)
        html = node.to_html()
        
        expected = "<div><blockquote>This is a quote\nWith multiple lines\nAnd some <b>formatting</b></blockquote></div>"
        self.assertEqual(html, expected)
    
    def test_unordered_list(self):
        md = """- Item 1
- Item 2 with **bold**
- Item 3 with `code`"""
        
        node = markdown_to_html_node(md)
        html = node.to_html()
        
        expected = "<div><ul><li>Item 1</li><li>Item 2 with <b>bold</b></li><li>Item 3 with <code>code</code></li></ul></div>"
        self.assertEqual(html, expected)
    
    def test_ordered_list(self):
        md = """1. First item
2. Second item with _italic_
3. Third item with [link](https://example.com)"""
        
        node = markdown_to_html_node(md)
        html = node.to_html()
        
        expected = '<div><ol><li>First item</li><li>Second item with <i>italic</i></li><li>Third item with <a href="https://example.com">link</a></li></ol></div>'
        self.assertEqual(html, expected)
    
    def test_mixed_content(self):
        md = """# Mixed Markdown Test

This is a paragraph with **bold** and _italic_ text.

## Code Example

```
function example() {
  return "Hello, world!";
}
```

> Here's a quote
> With multiple lines

### Lists

- Unordered list item 1
- Unordered list item 2

1. Ordered list item 1
2. Ordered list item 2"""
        
        node = markdown_to_html_node(md)
        html = node.to_html()
        
        # Just test that it generates something non-empty and with expected tags
        self.assertIn("<div>", html)
        self.assertIn("<h1>", html)
        self.assertIn("<h2>", html)
        self.assertIn("<h3>", html)
        self.assertIn("<p>", html)
        self.assertIn("<pre><code>", html)
        self.assertIn("<blockquote>", html)
        self.assertIn("<ul><li>", html)
        self.assertIn("<ol><li>", html)
        self.assertIn("<b>bold</b>", html)
        self.assertIn("<i>italic</i>", html)


if __name__ == "__main__":
    unittest.main()