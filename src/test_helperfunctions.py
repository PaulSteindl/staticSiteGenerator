from itertools import count
import unittest
import blocktype
from textnode import TextNode, TextType
from helperfunctions import *

class TestHelperfunctions(unittest.TestCase):

    def setUp(self):
        blocktype.counter = count(1)

    """------------------------------------"""
    """text_node_to_html_node function test"""
    """------------------------------------"""

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
        self.assertEqual(html_node.value, "")
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

    def test_image_type_value_is_empty_string(self):
        node = TextNode("Alt text", TextType.IMAGE, "https://example.com/image.png")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "img")
        self.assertEqual(html_node.value, "")
        self.assertEqual(html_node.props, {"src": "https://example.com/image.png", "alt": "Alt text"})

    def test_image_type_to_html_outputs_img_tag(self):
        node = TextNode("Alt text", TextType.IMAGE, "https://example.com/image.png")
        html_node = text_node_to_html_node(node)
        html = html_node.to_html()
        # Accept both <img ...> and <img .../>
        self.assertTrue(
            html.startswith('<img') and 'src="https://example.com/image.png"' in html and 'alt="Alt text"' in html
        )

    def test_image_type_missing_url_raises(self):
        node = TextNode("Alt text", TextType.IMAGE, "")
        with self.assertRaises(ValueError):
            text_node_to_html_node(node)

    def test_image_type_none_url_raises(self):
        node = TextNode("Alt text", TextType.IMAGE, None)
        with self.assertRaises(ValueError):
            text_node_to_html_node(node)

    """-----------------------------------"""
    """split_nodes_delimiter function test"""
    """-----------------------------------"""

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

    """-------------------------------------"""
    """extract_markdown_images function test"""
    """-------------------------------------"""

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

    """------------------------------------"""
    """extract_markdown_links function test"""
    """------------------------------------"""

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

    """-------------------------------"""
    """split_nodes_image function test"""
    """-------------------------------"""

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

    """------------------------------"""
    """split_nodes_link function test"""
    """------------------------------"""

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

    """-------------------------------"""
    """text_to_textnodes function test"""
    """-------------------------------"""

    def test_text_to_textnodes(self):
        new_nodes = text_to_textnodes("This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://github.com/PaulSteindl)")
        self.assertListEqual(
            [
                TextNode("This is ", TextType.NORMAL),
                TextNode("text", TextType.BOLD),
                TextNode(" with an ", TextType.NORMAL),
                TextNode("italic", TextType.ITALIC),
                TextNode(" word and a ", TextType.NORMAL),
                TextNode("code block", TextType.CODE),
                TextNode(" and an ", TextType.NORMAL),
                TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
                TextNode(" and a ", TextType.NORMAL),
                TextNode("link", TextType.LINK, "https://github.com/PaulSteindl"),
            ],
            new_nodes
        )

    def test_normal_text_to_textnodes(self):
        new_nodes = text_to_textnodes("A normal text with nothing unusual")
        self.assertListEqual(
            [
                TextNode("A normal text with nothing unusual", TextType.NORMAL)
            ],
            new_nodes
        )

    """--------------------------------"""
    """markdown_to_blocks function test"""
    """--------------------------------"""

    def test_markdown_to_blocks(self):
        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items"
            ],
        )

    def test_markdown_to_blocks_diffrent_text(self):
        md = """



This is **bolded** paragraph
With Alot of bs

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list


- And this is another list
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph\nWith Alot of bs",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list",
                "- And this is another list"
            ]
        )

    """-----------------------------------"""
    """markdown_to_html_node function test"""
    """-----------------------------------"""

    def test_paragraphs(self):
        md = """
This is **bolded** paragraph
text in a p
tag here

This is another paragraph with _italic_ text and `code` here"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
        )

    def test_codeblock(self):
        md = """
```
This is text that _should_ remain
the **same** even with inline stuff
```
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre></div>",
        )

    def test_markdown_to_html_node_heading(self):
        md = "# Heading 1"
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(html, "<div><h1>Heading 1</h1></div>")

    def test_markdown_to_html_node_multiple_headings(self):
        md = "# Heading 1\n\n## Heading 2\n\n### Heading 3"
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(html, "<div><h1>Heading 1</h1><h2>Heading 2</h2><h3>Heading 3</h3></div>")

    def test_markdown_to_html_node_unordered_list(self):
        md = "- Item 1\n- Item 2\n- Item 3"
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(html, "<div><ul><li>Item 1</li><li>Item 2</li><li>Item 3</li></ul></div>")

    def test_markdown_to_html_node_ordered_list(self):
        md = """1. First
2. Second
3. Third"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(html, "<div><ol><li>First</li><li>Second</li><li>Third</li></ol></div>")

    def test_markdown_to_html_node_quote(self):
        md = "> This is a quote"
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(html, "<div><blockquote>This is a quote</blockquote></div>")

    def test_markdown_to_html_node_code_block(self):
        md = "```\ncode block\nwith multiple lines\n```"
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(html, "<div><pre><code>code block\nwith multiple lines\n</code></pre></div>")

    def test_markdown_to_html_node_mixed_blocks(self):
        md = "# Heading\n\nParagraph text\n\n- List item 1\n- List item 2\n\n> Quote"
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><h1>Heading</h1><p>Paragraph text</p><ul><li>List item 1</li><li>List item 2</li></ul><blockquote>Quote</blockquote></div>"
        )

    def test_markdown_to_html_node_empty(self):
        md = ""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(html, "<div></div>")

    def test_markdown_to_html_node_multiple_paragraphs_and_lists(self):
        md = "Paragraph one.\n\nParagraph two.\n\n- List 1\n- List 2\n\n1. First\n2. Second"
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>Paragraph one.</p><p>Paragraph two.</p><ul><li>List 1</li><li>List 2</li></ul><ol><li>First</li><li>Second</li></ol></div>"
        )

    """---------------------------"""
    """extract_title function test"""
    """---------------------------"""

    def test_extract_title_h1_at_start(self):
        md = "# My Title\nSome content"
        result = extract_title(md)
        self.assertEqual(result, "My Title")

    def test_extract_title_h1_with_leading_spaces(self):
        md = "   # Leading Title\nContent"
        result = extract_title(md)
        self.assertEqual(result, "Leading Title")

    def test_extract_title_h1_with_trailing_spaces(self):
        md = "# Trailing Title   \nContent"
        result = extract_title(md)
        self.assertEqual(result, "Trailing Title")

    def test_extract_title_h1_with_special_characters(self):
        md = "# Title! @2024 *&^%\nContent"
        result = extract_title(md)
        self.assertEqual(result, "Title! @2024 *&^%")

    def test_extract_title_h1_not_first_line(self):
        md = "Intro text\n# Actual Title\nMore text"
        result = extract_title(md)
        self.assertEqual(result, "Actual Title")

    def test_extract_title_multiple_h1(self):
        md = "# First Title\n# Second Title"
        result = extract_title(md)
        self.assertEqual(result, "First Title")

    def test_extract_title_no_h1_raises_exception(self):
        md = "No heading here\n## Not h1"
        with self.assertRaises(Exception):
            extract_title(md)

    def test_extract_title_h1_with_extra_spaces(self):
        md = "   #    Title With Extra Spaces    \nContent"
        result = extract_title(md)
        self.assertEqual(result, "Title With Extra Spaces")
        
if __name__ == "__main__":
    unittest.main()