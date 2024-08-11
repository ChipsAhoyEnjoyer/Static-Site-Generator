import unittest

from textnode import TextNode, text_type_bold, text_type_text, text_type_italic, text_type_link, text_type_image, text_type_code

from inline_md import split_nodes_delimiter, extract_markdown_images, extract_markdown_links, split_nodes_image, split_nodes_link, text_to_textnodes

class TestInlineMD(unittest.TestCase):
    def test_split_nodes_delimiter(self):
        node = TextNode(text_type_text, "check out this `code` here.")
        new_nodes = split_nodes_delimiter([node], "`", text_type_code)
        correct_textnode_text = ["check out this ", "code", " here."]
        for i in range(len(new_nodes)):
            self.assertEqual(new_nodes[i].text, correct_textnode_text[i])

        node2 = TextNode(text_type_text, "check out this `code.`")
        new_nodes2 = split_nodes_delimiter([node2], "`", text_type_code)
        correct_textnode_text2 = ["check out this ", "code."]
        for i in range(len(new_nodes2)):
            self.assertEqual(new_nodes2[i].text, correct_textnode_text2[i])

    def test_split_nodes_delimiter2(self):
        node = TextNode(text_type_text, "check out this `code` here with `that code` there.")
        new_nodes = split_nodes_delimiter([node], "`", text_type_code)
        correct_textnode_text = ["check out this ", "code", " here with ", "that code", " there."]
        for i in range(len(new_nodes)):
            self.assertEqual(new_nodes[i].text, correct_textnode_text[i])
        
    def test_split_nodes_delimiter3(self):
        node = TextNode(text_type_text, "check out this `code` here.")
        node2 = TextNode(text_type_text, "look at this `other code` here.")
        new_nodes = split_nodes_delimiter([node, node2], "`", text_type_code)
        correct_textnode_text = ["check out this ", "code", " here.", "look at this ", "other code", " here."]
        for i in range(len(new_nodes)):
            self.assertEqual(new_nodes[i].text, correct_textnode_text[i])

    def test_split_nodes_delimiter4(self):
        node = TextNode(text_type_text, "check out this **bold** text here.")
        new_nodes = split_nodes_delimiter([node], "**", text_type_bold)
        correct_textnode_text = ["check out this ", "bold", " text here."]
        for i in range(len(new_nodes)):
            self.assertEqual(new_nodes[i].text, correct_textnode_text[i])
        self.assertEqual(new_nodes[1].text_type, "bold")
    
    def test_split_nodes_delimiter5(self):
        node = TextNode(text_type_text, "check out this **bold text here.")
        with self.assertRaises(SyntaxError):
            new_nodes = split_nodes_delimiter([node], "**", text_type_bold)

    def test_split_nodes_delimiter6(self):
        node = TextNode(text_type_code, "code **block**")
        new_nodes = split_nodes_delimiter([node], "**", text_type_bold)
        correct_textnode_text = ["code **block**"]
        for i in range(len(new_nodes)):
            self.assertEqual(new_nodes[i].text, correct_textnode_text[i])

    def test_extract_images(self):
        text = "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
        self.assertEqual([("rick roll", "https://i.imgur.com/aKaOqIh.gif"), ("obi wan", "https://i.imgur.com/fJRm4Vk.jpeg")], 
                           extract_markdown_images(text))

    def test_extract_link(self):
        text = "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"
        self.assertEqual([("to boot dev", "https://www.boot.dev"), ("to youtube", "https://www.youtube.com/@bootdotdev")], 
                           extract_markdown_links(text))
        
    def test_extract_markdown_links(self):
        matches = extract_markdown_links(
            "This is text with a [link](https://boot.dev) and [another link](https://blog.boot.dev)"
        )
        self.assertListEqual(
            [
                ("link", "https://boot.dev"),
                ("another link", "https://blog.boot.dev"),
            ],
            matches,
        )

    def test_split_image(self):
        node = TextNode(
            text_type_text,
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)",
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode(text_type_text, "This is text with an "),
                TextNode(text_type_image, "image", "https://i.imgur.com/zjjcJKZ.png"),
            ],
            new_nodes,
        )

    def test_split_image_single(self):
        node = TextNode(
            text_type_text,
            "![image](https://www.example.com/image.png)",
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode(text_type_image, "image", "https://www.example.com/image.png"),
            ],
            new_nodes,
        )

    def test_split_images(self):
        node = TextNode(
            text_type_text,
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode(text_type_text, "This is text with an "),
                TextNode(text_type_image, "image", "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(text_type_text, " and another "),
                TextNode(
                    text_type_image, "second image", "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )

    def test_split_links(self):
        node = TextNode(
            text_type_text,
            "This is text with a [link](https://boot.dev) and [another link](https://blog.boot.dev) with text that follows",
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode(text_type_text, "This is text with a "),
                TextNode(text_type_link, "link", "https://boot.dev"),
                TextNode(text_type_text, " and "),
                TextNode(text_type_link, "another link", "https://blog.boot.dev"),
                TextNode(text_type_text, " with text that follows"),
            ],
            new_nodes,
        )

    def test_text_to_textnode(self):
        node = "This is a **bold** text and an *italic* text."
        formatted_node = text_to_textnodes(node)
        self.assertEqual(
            formatted_node, 
            [
             TextNode(text_type_text, "This is a ", None), 
             TextNode(text_type_bold, "bold", None), 
             TextNode(text_type_text, " text and an ", None), 
             TextNode(text_type_italic, "italic", None), 
             TextNode(text_type_text, " text.", None)
             ])

    def test_text_to_textnode(self):
        node = "a"
        formatted_node = text_to_textnodes(node)
        self.assertEqual(formatted_node, [TextNode(text_type_text, "a", None)])

    def test_text_to_textnode(self):
        node = "a [link](google.com) and an ![image](catjpeg.com)"
        formatted_node = text_to_textnodes(node)
        self.assertEqual(
                         formatted_node, 
                        [
                         TextNode(text_type_text, "a ", None), 
                         TextNode(text_type_link, "link", "google.com"), 
                         TextNode(text_type_text, " and an ", None), 
                         TextNode(text_type_image, "image", "catjpeg.com")
                         ])
