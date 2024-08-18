import unittest

from textnode import TextNode, text_type_bold, text_type_text, text_type_italic, text_type_link, text_type_image

from textnode import text_node_to_html_node

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

    def test_text_node_to_html_node(self):
        node_text = TextNode(text_type_text, "item 1")
        leaf_node_from_text_node = text_node_to_html_node(node_text)
        self.assertEqual(leaf_node_from_text_node.__repr__(), "LeafNode(None, item 1, None)")

        node_link = TextNode(text_type_link, "Google", "www.google.com")
        leaf_node_from_link_node = text_node_to_html_node(node_link)
        self.assertEqual(leaf_node_from_link_node.to_html(), "<a href='www.google.com'>Google</a>")

        node_img = TextNode(text_type_image, "Dolphin image", "www.jotarosfavimage.com")
        leaf_node_from_img_node = text_node_to_html_node(node_img)
        self.assertEqual(leaf_node_from_img_node.to_html(), "<img src='www.jotarosfavimage.com' alt='Dolphin image'>")


if __name__ == "__main__":
    unittest.main()
