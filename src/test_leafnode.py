import unittest
from src.htmlnode import HTMLNode  # Adjust the import path if needed
from src.leafnode import LeafNode  # Adjust the import path if needed


class TestLeafNode(unittest.TestCase):

    def test_to_html_with_tag(self):
        node = LeafNode(tag="p", value="This is a paragraph of text.")
        self.assertEqual(node.to_html(), "<p>This is a paragraph of text.</p>")

    def test_to_html_with_props(self):
        node = LeafNode(
            tag="a", value="Click me!", props={"href": "https://google.com"}
        )
        self.assertEqual(
            node.to_html(), '<a href="https://google.com">Click me!</a>'
        )

    def test_to_html_raw_text(self):
        node = LeafNode(tag=None, value="Just some raw text string.")
        self.assertEqual(node.to_html(), "Just some raw text string.")

    def test_value_is_required(self):
        with self.assertRaises(ValueError):
            LeafNode(tag="p", value=None)

    def test_repr_formatting(self):
        node = LeafNode(tag="b", value="Bold text", props={"id": "bold-id"})
        expected_repr = "LeafNode(tag='b', value='Bold text', props={'id': 'bold-id'})"
        self.assertEqual(repr(node), expected_repr)


if __name__ == "__main__":
    unittest.main()
