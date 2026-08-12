import unittest
from src.htmlnode import HTMLNode  # Adjust the import path if your file name differs


class TestHTMLNode(unittest.TestCase):

    def test_props_to_html_with_multiple_props(self):
        props = {"href": "https://google.com", "target": "_blank"}
        node = HTMLNode(tag="a", value="Click me", props=props)
        self.assertEqual(
            node.props_to_html(), ' href="https://google.com" target="_blank"'
        )

    def test_props_to_html_empty(self):
        node = HTMLNode(tag="p", value="Hello world")
        self.assertEqual(node.props_to_html(), "")

    def test_props_to_html_single_prop(self):
        props = {"class": "primary-btn"}
        node = HTMLNode(tag="button", value="Submit", props=props)
        self.assertEqual(node.props_to_html(), ' class="primary-btn"')

    def test_repr_formatting(self):
        node = HTMLNode(tag="h1", value="Title")
        expected_repr = "HTMLNode(tag='h1', value='Title', children=None, props=None)"
        self.assertEqual(repr(node), expected_repr)


if __name__ == "__main__":
    unittest.main()
