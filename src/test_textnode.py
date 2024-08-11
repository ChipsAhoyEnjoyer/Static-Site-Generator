import unittest

from textnode import TextNode, text_type_bold, text_type_text, text_type_italic, text_type_link, text_type_image, text_type_code

class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode(text_type_bold, "This is a text node")
        node2 = TextNode(text_type_bold, "This is a text node")
        self.assertEqual(node, node2)
    
    def test_eq2(self):
        node = TextNode(text_type_italic, "This is a text node")
        node2 = TextNode(text_type_bold, "This is a text node")
        self.assertNotEqual(node, node2)

    def test_eq3(self):
        node = TextNode(text_type_bold, "This is a text node")
        node2 = TextNode(text_type_bold, "Text node")
        self.assertNotEqual(node, node2)

    def test_url(self):
        node = TextNode(text_type_bold, "This is a text node", "https://www.boot.dev")
        node2 = TextNode(text_type_bold, "This is a text node", "https://www.boot.dev")
        self.assertEqual(node, node2)

    def test_url2(self):
        node = TextNode(text_type_bold, "This is a text node", "https://www.boot.dev")
        node2 = TextNode(text_type_bold, "This is a text node")
        self.assertNotEqual(node, node2)
    
    def test_url3(self):
        node = TextNode(text_type_bold, "This is a text node", "https://www.boot.dev")
        node2 = TextNode(text_type_bold, "This is a text node", "https://www.google.com")
        self.assertNotEqual(node, node2)

    def test_repr(self):
        node = TextNode(text_type_bold, "This is a text node", "https://www.boot.dev")
        self.assertEqual(repr(node), "TextNode(bold, This is a text node, https://www.boot.dev)")


if __name__ == "__main__":
    unittest.main()
