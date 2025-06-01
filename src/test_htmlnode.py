import unittest
from htmlnode import HTMLNode

class TestHTMLNode(unittest.TestCase):
    def test_to_html(self):
        node = HTMLNode()
        with self.assertRaises(NotImplementedError):
            node.to_html()

    def test_with_values_to_html(self):
        node = HTMLNode("<a>", "This is a value", ["this is a child", "this is also a child"], {"key1" : "value1", "key2" : "value2"})
        with self.assertRaises(NotImplementedError):
            node.to_html()

    def test_props_to_html(self):
        node = HTMLNode("<a>", "This is a value", ["this is a child", "this is also a child"], {"key1" : "value1", "key2" : "value2"})
        testProp = " key1=\"value1\" key2=\"value2\""
        self.assertEqual(node.props_to_html(), testProp)

    def test_none_props_to_html(self):
        node = HTMLNode("<a>", "This is a value", ["this is a child", "this is also a child"], None)
        self.assertEqual(node.props_to_html(), "")

    def test_empty_props_to_html(self):
        node = HTMLNode("<a>", "This is a value", ["this is a child", "this is also a child"], {})
        self.assertEqual(node.props_to_html(), "")

    def test_default_props_to_html(self):
        node = HTMLNode("<a>", "This is a value", ["this is a child", "this is also a child"])
        self.assertEqual(node.props_to_html(), "")

    def test_repr(self):
        node = HTMLNode("<a>", "This is a value", ["this is a child", "this is also a child"], {"key1" : "value1", "key2" : "value2"})
        testString = "HTMLNode(<a>, This is a value, ['this is a child', 'this is also a child'], {'key1': 'value1', 'key2': 'value2'})"
        self.assertEqual(str(node), testString)

    def test_default_repr(self):
        node = HTMLNode()
        testString = "HTMLNode(None, None, None, None)"
        self.assertEqual(str(node), testString)

    def test_partial_repr(self):
        node = HTMLNode("<a>", None, ["this is a child", "this is also a child"])
        testString = "HTMLNode(<a>, None, ['this is a child', 'this is also a child'], None)"
        self.assertEqual(str(node), testString)

if __name__ == "__main__":
    unittest.main()