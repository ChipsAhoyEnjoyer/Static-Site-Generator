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