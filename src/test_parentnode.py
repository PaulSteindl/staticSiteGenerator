import unittest
from leafnode import LeafNode
from parentnode import ParentNode

class TestParentNode(unittest.TestCase):
    def test_to_html_with_child(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_children(self):
        child_node1 = LeafNode("span", "child1")
        child_node2 = LeafNode("p", "child2")
        parent_node = ParentNode("div", [child_node1, child_node2])
        self.assertEqual(parent_node.to_html(), "<div><span>child1</span><p>child2</p></div>")

    def test_to_html_with_children_and_prop(self):
        child_node1 = LeafNode("span", "child1")
        child_node2 = LeafNode("p", "child2")
        parent_node = ParentNode("div", [child_node1, child_node2], {"key" : "value"})
        self.assertEqual(parent_node.to_html(), "<div><span>child1</span><p>child2</p></div>")

    def test_to_html_with_grandchild(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(),"<div><span><b>grandchild</b></span></div>")

    def test_to_html_with_grandchildren(self):
        grandchild_node1 = LeafNode("a", "grandchild1")
        grandchild_node2 = LeafNode("p", "grandchild2")
        child_node = ParentNode("span", [grandchild_node1, grandchild_node2])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span><a>grandchild1</a><p>grandchild2</p></span></div>")

    def test_to_html_with_children_and_grandchild(self):
        grandchild_node1 = LeafNode("a", "grandchild1")
        grandchild_node2 = LeafNode("p", "grandchild2")
        child_node1 = ParentNode("span", [grandchild_node1, grandchild_node2])
        child_node2 = LeafNode("b", "child2")
        parent_node = ParentNode("div", [child_node1, child_node2])
        self.assertEqual(parent_node.to_html(), "<div><span><a>grandchild1</a><p>grandchild2</p></span><b>child2</b></div>")

    def test_to_html_with_children_and_grandchild_and_prop(self):
        grandchild_node1 = LeafNode("a", "grandchild1")
        grandchild_node2 = LeafNode("p", "grandchild2")
        child_node1 = ParentNode("span", [grandchild_node1, grandchild_node2])
        child_node2 = LeafNode("b", "child2")
        parent_node = ParentNode("div", [child_node1, child_node2], {"key" : "value"})
        self.assertEqual(parent_node.to_html(), "<div><span><a>grandchild1</a><p>grandchild2</p></span><b>child2</b></div>")

    def test_to_html_with_children_no_tag_and_grandchild_no_tag(self):
        grandchild_node1 = LeafNode(None, "grandchild1")
        grandchild_node2 = LeafNode(None, "grandchild2")
        child_node1 = ParentNode("span", [grandchild_node1, grandchild_node2])
        child_node2 = LeafNode(None, "child2")
        parent_node = ParentNode("div", [child_node1, child_node2])
        self.assertEqual(parent_node.to_html(), "<div><span>grandchild1grandchild2</span>child2</div>")

    def test_to_html_empty_tag(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("", [child_node])
        with self.assertRaises(ValueError):
            parent_node.to_html()

    def test_to_html_none_tag(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode(None, [child_node])
        with self.assertRaises(ValueError):
            parent_node.to_html()

    def test_to_html_empty_child(self):
        parent_node = ParentNode("div", [])
        with self.assertRaises(ValueError):
            parent_node.to_html()

    def test_to_html_none_child(self):
        parent_node = ParentNode("div", None)
        with self.assertRaises(ValueError):
            parent_node.to_html()
        

if __name__ == "__main__":
    unittest.main()