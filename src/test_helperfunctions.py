import unittest
from textnode import TextNode, TextType
from helperfunctions import *

class TestHelperfunctions(unittest.TestCase):

    """text_node_to_html_node function test"""
    def test_normal_type(self):
        node = TextNode("This is a text node", TextType.NORMAL)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")

    def test_bold_type(self):
        node = TextNode("This is a text node", TextType.BOLD)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "b")
        self.assertEqual(html_node.value, "This is a text node")

    def test_italic_type(self):
        node = TextNode("This is a text node", TextType.ITALIC)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "i")
        self.assertEqual(html_node.value, "This is a text node")

    def test_code_type(self):
        node = TextNode("This is a text node", TextType.CODE)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "code")
        self.assertEqual(html_node.value, "This is a text node")

    def test_link_type(self):
        node = TextNode("This is a text node", TextType.LINK, "https://github.com/PaulSteindl")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "a")
        self.assertEqual(html_node.value, "This is a text node")
        self.assertEqual(html_node.props, {"href" : "https://github.com/PaulSteindl"})

    def test_no_url_link_type(self):
        node = TextNode("This is a text node", TextType.LINK, "")
        with self.assertRaises(ValueError):
            text_node_to_html_node(node)

    def test_none_url_link_type(self):
        node = TextNode("This is a text node", TextType.LINK, None)
        with self.assertRaises(ValueError):
            text_node_to_html_node(node)

    def test_image_type(self):
        node = TextNode("This is a text node", TextType.IMAGE, "https://github.com/PaulSteindl")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "img")
        self.assertEqual(html_node.value, None)
        self.assertEqual(html_node.props, {"src" : "https://github.com/PaulSteindl", "alt" : "This is a text node"})

    def test_no_url_image_type(self):
        node = TextNode("This is a text node", TextType.IMAGE, "")
        with self.assertRaises(ValueError):
            text_node_to_html_node(node)

    def test_none_url_image_type(self):
        node = TextNode("This is a text node", TextType.IMAGE, None)
        with self.assertRaises(ValueError):
            text_node_to_html_node(node)

    def test_invalid_image_type(self):
        with self.assertRaises(AttributeError):
            TextNode("This is a text node", TextType.INVALIDBS, None)

    """split_nodes_delimiter function test"""
    def test_bold_split_nodes_delimiter(self):
        node = TextNode("This is a **amazing bold** text node", TextType.NORMAL)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        test_node0 = TextNode("This is a ", TextType.NORMAL, None)
        test_node1 = TextNode("amazing bold", TextType.BOLD, None)
        test_node2 = TextNode(" text node", TextType.NORMAL, None)
        self.assertEqual(new_nodes[0], test_node0)
        self.assertEqual(new_nodes[1], test_node1)
        self.assertEqual(new_nodes[2], test_node2)

    def test_multiple_bold_split_nodes_delimiter(self):
        node = TextNode("This is a **amazing bold** text node **with more bold**", TextType.NORMAL)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        test_node0 = TextNode("This is a ", TextType.NORMAL, None)
        test_node1 = TextNode("amazing bold", TextType.BOLD, None)
        test_node2 = TextNode(" text node ", TextType.NORMAL, None)
        test_node3 = TextNode("with more bold", TextType.BOLD, None)
        self.assertEqual(new_nodes[0], test_node0)
        self.assertEqual(new_nodes[1], test_node1)
        self.assertEqual(new_nodes[2], test_node2)
        self.assertEqual(new_nodes[3], test_node3)

    def test_multiple_bold_and_nodes_split_nodes_delimiter(self):
        node1 = TextNode("This is a **amazing bold** text node **with more bold**", TextType.NORMAL)
        node2 = TextNode("This is a **amazing bold** text node **with more bold**", TextType.NORMAL)
        new_nodes = split_nodes_delimiter([node1, node2], "**", TextType.BOLD)
        test_node0 = TextNode("This is a ", TextType.NORMAL, None)
        test_node1 = TextNode("amazing bold", TextType.BOLD, None)
        test_node2 = TextNode(" text node ", TextType.NORMAL, None)
        test_node3 = TextNode("with more bold", TextType.BOLD, None)
        self.assertEqual(new_nodes[0], test_node0)
        self.assertEqual(new_nodes[1], test_node1)
        self.assertEqual(new_nodes[2], test_node2)
        self.assertEqual(new_nodes[3], test_node3)
        self.assertEqual(new_nodes[4], test_node0)
        self.assertEqual(new_nodes[5], test_node1)
        self.assertEqual(new_nodes[6], test_node2)
        self.assertEqual(new_nodes[7], test_node3)

    def test_italic_split_nodes_delimiter(self):
        node = TextNode("This is a _amazing italic_ text node", TextType.NORMAL)
        new_nodes = split_nodes_delimiter([node], "_", TextType.ITALIC)
        test_node0 = TextNode("This is a ", TextType.NORMAL, None)
        test_node1 = TextNode("amazing italic", TextType.ITALIC, None)
        test_node2 = TextNode(" text node", TextType.NORMAL, None)
        self.assertEqual(new_nodes[0], test_node0)
        self.assertEqual(new_nodes[1], test_node1)
        self.assertEqual(new_nodes[2], test_node2)

    def test_multiple_italic_split_nodes_delimiter(self):
        node = TextNode("This is a _amazing italic_ text node _with more italic_", TextType.NORMAL)
        new_nodes = split_nodes_delimiter([node], "_", TextType.ITALIC)
        test_node0 = TextNode("This is a ", TextType.NORMAL, None)
        test_node1 = TextNode("amazing italic", TextType.ITALIC, None)
        test_node2 = TextNode(" text node ", TextType.NORMAL, None)
        test_node3 = TextNode("with more italic", TextType.ITALIC, None)
        self.assertEqual(new_nodes[0], test_node0)
        self.assertEqual(new_nodes[1], test_node1)
        self.assertEqual(new_nodes[2], test_node2)
        self.assertEqual(new_nodes[3], test_node3)

    def test_multiple_italic_and_nodes_split_nodes_delimiter(self):
        node1 = TextNode("This is a _amazing italic_ text node _with more italic_", TextType.NORMAL)
        node2 = TextNode("This is a _amazing italic_ text node _with more italic_", TextType.NORMAL)
        new_nodes = split_nodes_delimiter([node1, node2], "_", TextType.ITALIC)
        test_node0 = TextNode("This is a ", TextType.NORMAL, None)
        test_node1 = TextNode("amazing italic", TextType.ITALIC, None)
        test_node2 = TextNode(" text node ", TextType.NORMAL, None)
        test_node3 = TextNode("with more italic", TextType.ITALIC, None)
        self.assertEqual(new_nodes[0], test_node0)
        self.assertEqual(new_nodes[1], test_node1)
        self.assertEqual(new_nodes[2], test_node2)
        self.assertEqual(new_nodes[3], test_node3)
        self.assertEqual(new_nodes[4], test_node0)
        self.assertEqual(new_nodes[5], test_node1)
        self.assertEqual(new_nodes[6], test_node2)
        self.assertEqual(new_nodes[7], test_node3)

    def test_code_split_nodes_delimiter(self):
        node = TextNode("This is a `amazing code` text node", TextType.NORMAL)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        test_node0 = TextNode("This is a ", TextType.NORMAL, None)
        test_node1 = TextNode("amazing code", TextType.CODE, None)
        test_node2 = TextNode(" text node", TextType.NORMAL, None)
        self.assertEqual(new_nodes[0], test_node0)
        self.assertEqual(new_nodes[1], test_node1)
        self.assertEqual(new_nodes[2], test_node2)

    def test_code_split_nodes_delimiter(self):
        node = TextNode("This is a `amazing code` text node `with more code`", TextType.NORMAL)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        test_node0 = TextNode("This is a ", TextType.NORMAL, None)
        test_node1 = TextNode("amazing code", TextType.CODE, None)
        test_node2 = TextNode(" text node ", TextType.NORMAL, None)
        test_node3 = TextNode("with more code", TextType.CODE, None)
        self.assertEqual(new_nodes[0], test_node0)
        self.assertEqual(new_nodes[1], test_node1)
        self.assertEqual(new_nodes[2], test_node2)
        self.assertEqual(new_nodes[3], test_node3)

    def test_multiple_code_and_nodes_split_nodes_delimiter(self):
        node1 = TextNode("This is a `amazing code` text node `with more code`", TextType.NORMAL)
        node2 = TextNode("This is a `amazing code` text node `with more code`", TextType.NORMAL)
        new_nodes = split_nodes_delimiter([node1, node2], "`", TextType.CODE)
        test_node0 = TextNode("This is a ", TextType.NORMAL, None)
        test_node1 = TextNode("amazing code", TextType.CODE, None)
        test_node2 = TextNode(" text node ", TextType.NORMAL, None)
        test_node3 = TextNode("with more code", TextType.CODE, None)
        self.assertEqual(new_nodes[0], test_node0)
        self.assertEqual(new_nodes[1], test_node1)
        self.assertEqual(new_nodes[2], test_node2)
        self.assertEqual(new_nodes[3], test_node3)
        self.assertEqual(new_nodes[4], test_node0)
        self.assertEqual(new_nodes[5], test_node1)
        self.assertEqual(new_nodes[6], test_node2)
        self.assertEqual(new_nodes[7], test_node3)

    def test_bold_split_italic_split_nodes_delimiter(self):
        node = TextNode("This is a amazing bold _with some italic_ text node", TextType.BOLD)
        new_nodes = split_nodes_delimiter([node], "_", TextType.ITALIC)
        test_node0 = TextNode("This is a amazing bold ", TextType.BOLD, None)
        test_node1 = TextNode("with some italic", TextType.ITALIC, None)
        test_node2 = TextNode(" text node", TextType.BOLD, None)
        self.assertEqual(new_nodes[0], test_node0)
        self.assertEqual(new_nodes[1], test_node1)
        self.assertEqual(new_nodes[2], test_node2)

if __name__ == "__main__":
    unittest.main()