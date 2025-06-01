import unittest
from textnode import TextNode, TextType

class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

    def test_url_eq(self):
        node = TextNode("This is a text node", TextType.BOLD, "https://github.com/PaulSteindl")
        node2 = TextNode("This is a text node", TextType.BOLD, "https://github.com/PaulSteindl")
        self.assertEqual(node, node2)

    def test_url_default_vs_none_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD, None)
        self.assertEqual(node, node2)

    def test_text_not_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is also a text node", TextType.BOLD)
        self.assertNotEqual(node, node2)

    def test_text_type_not_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.ITALIC)
        self.assertNotEqual(node, node2)

    def test_url_not_eq(self):
        node = TextNode("This is a text node", TextType.BOLD, "https://github.com/PaulSteindl")
        node2 = TextNode("This is a text node", TextType.BOLD, "https://orf.at")
        self.assertNotEqual(node, node2)

    def test_url_default_vs_value_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD, "https://orf.at")
        self.assertNotEqual(node, node2)

    
if __name__ == "__main__":
    unittest.main()