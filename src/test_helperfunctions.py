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
        self.assertListEqual([test_node0, test_node1, test_node2], new_nodes)

    def test_multiple_bold_split_nodes_delimiter(self):
        node = TextNode("This is a **amazing bold** text node **with more bold**", TextType.NORMAL)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        test_node0 = TextNode("This is a ", TextType.NORMAL, None)
        test_node1 = TextNode("amazing bold", TextType.BOLD, None)
        test_node2 = TextNode(" text node ", TextType.NORMAL, None)
        test_node3 = TextNode("with more bold", TextType.BOLD, None)
        self.assertListEqual([test_node0, test_node1, test_node2, test_node3], new_nodes)

    def test_multiple_bold_and_nodes_split_nodes_delimiter(self):
        node1 = TextNode("This is a **amazing bold** text node **with more bold**", TextType.NORMAL)
        node2 = TextNode("This is a **amazing bold** text node **with more bold**", TextType.NORMAL)
        new_nodes = split_nodes_delimiter([node1, node2], "**", TextType.BOLD)
        test_node0 = TextNode("This is a ", TextType.NORMAL, None)
        test_node1 = TextNode("amazing bold", TextType.BOLD, None)
        test_node2 = TextNode(" text node ", TextType.NORMAL, None)
        test_node3 = TextNode("with more bold", TextType.BOLD, None)
        self.assertListEqual([test_node0, test_node1, test_node2, test_node3, test_node0, test_node1, test_node2, test_node3], new_nodes)

    def test_italic_split_nodes_delimiter(self):
        node = TextNode("This is a _amazing italic_ text node", TextType.NORMAL)
        new_nodes = split_nodes_delimiter([node], "_", TextType.ITALIC)
        test_node0 = TextNode("This is a ", TextType.NORMAL, None)
        test_node1 = TextNode("amazing italic", TextType.ITALIC, None)
        test_node2 = TextNode(" text node", TextType.NORMAL, None)
        self.assertListEqual([test_node0, test_node1, test_node2], new_nodes)

    def test_multiple_italic_split_nodes_delimiter(self):
        node = TextNode("This is a _amazing italic_ text node _with more italic_", TextType.NORMAL)
        new_nodes = split_nodes_delimiter([node], "_", TextType.ITALIC)
        test_node0 = TextNode("This is a ", TextType.NORMAL, None)
        test_node1 = TextNode("amazing italic", TextType.ITALIC, None)
        test_node2 = TextNode(" text node ", TextType.NORMAL, None)
        test_node3 = TextNode("with more italic", TextType.ITALIC, None)
        self.assertListEqual([test_node0, test_node1, test_node2, test_node3], new_nodes)

    def test_multiple_italic_and_nodes_split_nodes_delimiter(self):
        node1 = TextNode("This is a _amazing italic_ text node _with more italic_", TextType.NORMAL)
        node2 = TextNode("This is a _amazing italic_ text node _with more italic_", TextType.NORMAL)
        new_nodes = split_nodes_delimiter([node1, node2], "_", TextType.ITALIC)
        test_node0 = TextNode("This is a ", TextType.NORMAL, None)
        test_node1 = TextNode("amazing italic", TextType.ITALIC, None)
        test_node2 = TextNode(" text node ", TextType.NORMAL, None)
        test_node3 = TextNode("with more italic", TextType.ITALIC, None)
        self.assertListEqual([test_node0, test_node1, test_node2, test_node3, test_node0, test_node1, test_node2, test_node3], new_nodes)

    def test_code_split_nodes_delimiter(self):
        node = TextNode("This is a `amazing code` text node", TextType.NORMAL)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        test_node0 = TextNode("This is a ", TextType.NORMAL, None)
        test_node1 = TextNode("amazing code", TextType.CODE, None)
        test_node2 = TextNode(" text node", TextType.NORMAL, None)
        self.assertListEqual([test_node0, test_node1, test_node2], new_nodes)

    def test_code_split_nodes_delimiter(self):
        node = TextNode("This is a `amazing code` text node `with more code`", TextType.NORMAL)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        test_node0 = TextNode("This is a ", TextType.NORMAL, None)
        test_node1 = TextNode("amazing code", TextType.CODE, None)
        test_node2 = TextNode(" text node ", TextType.NORMAL, None)
        test_node3 = TextNode("with more code", TextType.CODE, None)
        self.assertListEqual([test_node0, test_node1, test_node2, test_node3], new_nodes)

    def test_multiple_code_and_nodes_split_nodes_delimiter(self):
        node1 = TextNode("This is a `amazing code` text node `with more code`", TextType.NORMAL)
        node2 = TextNode("This is a `amazing code` text node `with more code`", TextType.NORMAL)
        new_nodes = split_nodes_delimiter([node1, node2], "`", TextType.CODE)
        test_node0 = TextNode("This is a ", TextType.NORMAL, None)
        test_node1 = TextNode("amazing code", TextType.CODE, None)
        test_node2 = TextNode(" text node ", TextType.NORMAL, None)
        test_node3 = TextNode("with more code", TextType.CODE, None)
        self.assertListEqual([test_node0, test_node1, test_node2, test_node3, test_node0, test_node1, test_node2, test_node3], new_nodes)

    def test_bold_split_italic_split_nodes_delimiter(self):
        node = TextNode("This is a amazing bold _with some italic_ text node", TextType.BOLD)
        new_nodes = split_nodes_delimiter([node], "_", TextType.ITALIC)
        test_node0 = TextNode("This is a amazing bold ", TextType.BOLD, None)
        test_node1 = TextNode("with some italic", TextType.ITALIC, None)
        test_node2 = TextNode(" text node", TextType.BOLD, None)
        self.assertListEqual([test_node0, test_node1, test_node2], new_nodes)

    """extract_markdown_images function test"""
    def test_extract_markdown_images(self):
        matches = extract_markdown_images(
            "This is text with an ![image](https://avatars.githubusercontent.com/u/81384142?v=4)"
        )
        self.assertListEqual([("image", "https://avatars.githubusercontent.com/u/81384142?v=4")], matches)

    def test_multiple_images_extract_markdown_images(self):
        matches = extract_markdown_images(
            "This is text with an ![image](https://avatars.githubusercontent.com/u/81384142?v=4) and ![anotherImage](https://imgs.search.brave.com/Rf89szbFGT1-Xw_wtvjNhVDHmC3KfdDOx-eu5yGd0oQ/rs:fit:860:0:0:0/g:ce/aHR0cHM6Ly9pMC53/cC5jb20vaGlwZXJ0/ZXh0dWFsLmNvbS93/cC1jb250ZW50L3Vw/bG9hZHMvMjAwOC8w/NC9yaWNrcm9sbGVk/LmpwZz9yZXNpemU9/MjMwLDE5MSZxdWFs/aXR5PTcwJnN0cmlw/PWFsbA)"
        )
        self.assertListEqual([("image", "https://avatars.githubusercontent.com/u/81384142?v=4"),
                              ("anotherImage", "https://imgs.search.brave.com/Rf89szbFGT1-Xw_wtvjNhVDHmC3KfdDOx-eu5yGd0oQ/rs:fit:860:0:0:0/g:ce/aHR0cHM6Ly9pMC53/cC5jb20vaGlwZXJ0/ZXh0dWFsLmNvbS93/cC1jb250ZW50L3Vw/bG9hZHMvMjAwOC8w/NC9yaWNrcm9sbGVk/LmpwZz9yZXNpemU9/MjMwLDE5MSZxdWFs/aXR5PTcwJnN0cmlw/PWFsbA")
                              ], matches)

    def test_with_link_extract_markdown_images(self):
        matches = extract_markdown_images(
            "This is text with a [link](https://github.com/PaulSteindl)"
        )
        self.assertListEqual([], matches)

    """extract_markdown_links function test"""
    def test_extract_markdown_links(self):
        matches = extract_markdown_links(
            "This is text with a [link](https://github.com/PaulSteindl)"
        )
        self.assertListEqual([("link", "https://github.com/PaulSteindl")], matches)

    def test_multiple_links_extract_markdown_links(self):
        matches = extract_markdown_links(
            "This is text with a [link](https://github.com/PaulSteindl) and [anotherLink](https://github.com/PaulSteindl/staticSiteGenerator)"
        )
        self.assertListEqual([("link", "https://github.com/PaulSteindl"),
                              ("anotherLink", "https://github.com/PaulSteindl/staticSiteGenerator")
                              ], matches)

    def test_with_image_extract_markdown_links(self):
        matches = extract_markdown_links(
            "This is text with an ![image](https://github.com/PaulSteindl)"
        )
        self.assertListEqual([], matches)

    """split_nodes_image function test"""
    def test_split_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.NORMAL
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.NORMAL),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.NORMAL),
                TextNode(
                    "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
                )
            ],
            new_nodes
        )

    def test_only_image_split_images(self):
        node = TextNode(
            "![image](https://avatars.githubusercontent.com/u/81384142?v=4)",
            TextType.NORMAL,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("image", TextType.IMAGE, "https://avatars.githubusercontent.com/u/81384142?v=4")
            ],
            new_nodes
        )

    def test_only_images_split_images(self):
        node = TextNode(
            "![image](https://avatars.githubusercontent.com/u/81384142?v=4)![image](https://imgs.search.brave.com/Rf89szbFGT1-Xw_wtvjNhVDHmC3KfdDOx-eu5yGd0oQ/rs:fit:860:0:0:0/g:ce/aHR0cHM6Ly9pMC53/cC5jb20vaGlwZXJ0/ZXh0dWFsLmNvbS93/cC1jb250ZW50L3Vw/bG9hZHMvMjAwOC8w/NC9yaWNrcm9sbGVk/LmpwZz9yZXNpemU9/MjMwLDE5MSZxdWFs/aXR5PTcwJnN0cmlw/PWFsbA)",
            TextType.NORMAL,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("image", TextType.IMAGE, "https://avatars.githubusercontent.com/u/81384142?v=4"),
                TextNode("image", TextType.IMAGE, "https://imgs.search.brave.com/Rf89szbFGT1-Xw_wtvjNhVDHmC3KfdDOx-eu5yGd0oQ/rs:fit:860:0:0:0/g:ce/aHR0cHM6Ly9pMC53/cC5jb20vaGlwZXJ0/ZXh0dWFsLmNvbS93/cC1jb250ZW50L3Vw/bG9hZHMvMjAwOC8w/NC9yaWNrcm9sbGVk/LmpwZz9yZXNpemU9/MjMwLDE5MSZxdWFs/aXR5PTcwJnN0cmlw/PWFsbA")
            ],
            new_nodes
        )

    def test_no_images_split_images(self):
        node = TextNode(
            "This is text with no images",
            TextType.NORMAL
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with no images", TextType.NORMAL)
            ],
            new_nodes
        )

    def test_bold_split_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.BOLD
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.BOLD),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.BOLD),
                TextNode(
                    "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
                )
            ],
            new_nodes
        )

    def test_with_link_split_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and a [link](https://github.com/PaulSteindl)",
            TextType.NORMAL
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.NORMAL),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and a [link](https://github.com/PaulSteindl)", TextType.NORMAL)
            ],
            new_nodes
        )

    """split_nodes_link function test"""
    def test_split_links(self):
        node = TextNode(
            "This is text with a [link](https://github.com/PaulSteindl) and another [second link](https://github.com/PaulSteindl/staticSiteGenerator)",
            TextType.NORMAL
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.NORMAL),
                TextNode("link", TextType.LINK, "https://github.com/PaulSteindl"),
                TextNode(" and another ", TextType.NORMAL),
                TextNode("second link", TextType.LINK, "https://github.com/PaulSteindl/staticSiteGenerator")
            ],
            new_nodes
        )

    def test_only_link_split_links(self):
        node = TextNode(
            "[link](https://github.com/PaulSteindl)",
            TextType.NORMAL,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("link", TextType.LINK, "https://github.com/PaulSteindl")
            ],
            new_nodes
        )

    def test_only_links_split_links(self):
        node = TextNode(
            "[link](https://github.com/PaulSteindl)[second link](https://github.com/PaulSteindl/staticSiteGenerator)",
            TextType.NORMAL,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("link", TextType.LINK, "https://github.com/PaulSteindl"),
                TextNode("second link", TextType.LINK, "https://github.com/PaulSteindl/staticSiteGenerator")
            ],
            new_nodes
        )

    def test_no_links_split_links(self):
        node = TextNode(
            "This is text with no links",
            TextType.NORMAL
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is text with no links", TextType.NORMAL)
            ],
            new_nodes
        )

    def test_bold_split_links(self):
        node = TextNode(
            "This is text with a [link](https://github.com/PaulSteindl) and another [second link](https://github.com/PaulSteindl/staticSiteGenerator)",
            TextType.BOLD
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.BOLD),
                TextNode("link", TextType.LINK, "https://github.com/PaulSteindl"),
                TextNode(" and another ", TextType.BOLD),
                TextNode("second link", TextType.LINK, "https://github.com/PaulSteindl/staticSiteGenerator")
            ],
            new_nodes
        )
    
    def test_with_image_split_links(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and a [link](https://github.com/PaulSteindl)",
            TextType.NORMAL
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and a ", TextType.NORMAL),
                TextNode("link", TextType.LINK, "https://github.com/PaulSteindl")
            ],
            new_nodes
        )









if __name__ == "__main__":
    unittest.main()