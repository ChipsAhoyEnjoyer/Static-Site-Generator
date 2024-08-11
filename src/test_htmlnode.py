import unittest

from htmlnode import HTMLNode, LeafNode, ParentNode

from textnode import TextNode, text_type_bold, text_type_text, text_type_italic, text_type_link, text_type_image, text_type_code

from inline_md import text_node_to_html_node

class TestHTMLNode(unittest.TestCase):
	def test_repr(self):
		node = HTMLNode(tag="a", value="Boot.dev", props={"href": "https://www.boot.dev"})
		self.assertEqual(repr(node), "HTMLNode(a, Boot.dev, children: None, {'href': 'https://www.boot.dev'})")

	def test_repr(self):
		node = HTMLNode(tag="a", value="Boot.dev", children=["a", "div"], props={"href": "https://www.boot.dev"})
		self.assertEqual(repr(node), "HTMLNode(a, Boot.dev, children: ['a', 'div'], {'href': 'https://www.boot.dev'})")

	def test_props_to_html(self):
		node = HTMLNode(tag="p", value="Boot.dev", props={"attr": "content",
														  "attr2": "content2"})
		self.assertEqual(node.props_to_html(), " attr='content' attr2='content2'")

	def test_props_to_html2(self):
		node = HTMLNode(tag="p", value="Boot.dev", props={"attr": "content",
														  "attr2": "content2"})
		node2 = HTMLNode(tag="a", value="Google.com", props={"attr": "content",
														   "attr2": "content2"})
		self.assertEqual(node.props_to_html(), node2.props_to_html())
	
	def test_to_html(self):
		node = HTMLNode(tag="p", value="Boot.dev", props={"attr": "content",
														  "attr2": "content2"})
		with self.assertRaises(NotImplementedError):
			node.to_html()


class TestLeafNode(unittest.TestCase):
	def test_no_children_allowed(self):
		node2 = LeafNode("p", "test_value")
	
	def test_value_required(self):
		with self.assertRaises(ValueError):
			node = LeafNode(value=None, tag="p")
			node.to_html()
	
	def test_repr(self):
		node = LeafNode("p", "test value")
		self.assertEqual(node.__repr__(), "LeafNode(p, test value, None)")

	def test_no_tag(self):
		node = LeafNode(tag=None, value="Lurom Ipsum", props={"href": "www.dummylink.com"})
		self.assertEqual(node.to_html(), node.value)

	def test_to_html(self):
		node_img = LeafNode("img", "dummy text", children=None, props={"src": "deez/nuts.jpg", "alt": "Picture of almonds"})
		self.assertEqual(node_img.to_html(), "<img src='deez/nuts.jpg' alt='Picture of almonds'>")
		node_link = LeafNode("a", "Dummy link", children=None, props={"href": "www.dummylink.com"})
		self.assertEqual(node_link.to_html(), "<a href='www.dummylink.com'>Dummy link</a>")

	def test_to_html2(self):
		node_ol = LeafNode("ol", "item1\nitem2\n")
		self.assertEqual(node_ol.to_html(), "\n  <li>item1</li>\n  <li>item2</li>\n")
		node_ul = LeafNode("ul", "item1\nitem2\n")
		self.assertEqual(node_ul.to_html(), "\n  <li>item1</li>\n  <li>item2</li>\n")

	def test_to_html3(self):
		node_blockquote = LeafNode("blockquote", "item1")
		self.assertEqual(node_blockquote.to_html(), "<blockquote>\nitem1\n</blockquote>")

	def test_to_html4(self):
		node_h3 = LeafNode("h3", "item1")
		self.assertEqual(node_h3.to_html(), "<h3>item1</h3>")
		node_p = LeafNode("p", "item1")
		self.assertEqual(node_p.to_html(), "<p>item1</p>")
		node_code = LeafNode("code", "item1")
		self.assertEqual(node_code.to_html(), "<code>item1</code>")
		node_bold = LeafNode("b", "item1")
		self.assertEqual(node_bold.to_html(), "<b>item1</b>")

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


class TestParentNode(unittest.TestCase):
	def test_to_html_single_child(self):
		node = ParentNode(
						  tag="p",
						  children=[
									LeafNode(None, "Normal text"),
									],
						  )
		self.assertEqual(node.to_html(), "<p>Normal text</p>")


	def test_to_html_multiple_children(self):
		node = ParentNode(
					      tag="p",
						  children=[
							        LeafNode("b", "Bold text"),
							        LeafNode(None, "Normal text"),
							        LeafNode("i", "italic text"),
							        LeafNode(None, "Normal text"),
									],
						  )
		self.assertEqual(node.to_html(), 
				 	     "<p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p>",
				 	     )

	def test_to_html_no_children(self):
		node = ParentNode(
					      tag="p",
						  )
		with self.assertRaises(ValueError):
			node.to_html()

	def test_to_html_nested_parent_node(self):
		node1 = ParentNode(
					      tag="p",
						  children=[
							        LeafNode("b", "Bold text"),
							        LeafNode(None, "Normal text"),
							        LeafNode("i", "italic text"),
							        LeafNode(None, "Normal text"),
									],
						  )
		node2 = ParentNode(
					      tag="body",
						  children=[
							  		LeafNode(None, "Read below"),
							        node1,
									LeafNode(None, "The end."),
									],
						  )
		self.assertEqual(node2.to_html(), "<body>Read below<p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p>The end.</body>")