import unittest
from leafnode import LeafNode

class TestLeafNode(unittest.TestCase):
    def test_p_to_html(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

    def test_p_none_props_to_html(self):
        node = LeafNode("p", "Hello, world!", None)
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

    def test_a_with_props_to_html(self):
        node = LeafNode("a", "Hello, world!", {"href": "https://github.com/PaulSteindl"})
        self.assertEqual(node.to_html(), "<a href=\"https://github.com/PaulSteindl\">Hello, world!</a>")

    def test_none_tag_to_html(self):
        node = LeafNode(None, "Hello, world!")
        self.assertEqual(node.to_html(), "Hello, world!")

    def test_none_value_to_html(self):
        node = LeafNode("p", None)
        with self.assertRaises(ValueError):
            node.to_html()

    def test_none_value_none_tag_to_html(self):
        node = LeafNode(None, None)
        with self.assertRaises(ValueError):
            node.to_html()

if __name__ == "__main__":
    unittest.main()