from inline_markdown import split_nodes_delimiter, extract_markdown_images, extract_markdown_links
from textnode import TextNode, TextType

import unittest

class TestSplitNodesDelimiter(unittest.TestCase):
    
    def test_code_block_delimiter(self):
        node = TextNode("This is text with a `code block` word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(
            new_nodes,
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("code block", TextType.CODE),
                TextNode(" word", TextType.TEXT),
            ]
        )

    def test_bold_delimiter(self):
        node = TextNode("Hello **world** of markdown", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(
            new_nodes,
            [
                TextNode("Hello ", TextType.TEXT),
                TextNode("world", TextType.BOLD),
                TextNode(" of markdown", TextType.TEXT),
            ]
        )

    def test_italic_delimiter(self):
        node = TextNode("An *italicized* message", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "*", TextType.ITALIC)
        self.assertEqual(
            new_nodes,
            [
                TextNode("An ", TextType.TEXT),
                TextNode("italicized", TextType.ITALIC),
                TextNode(" message", TextType.TEXT),
            ]
        )

    def test_multiple_same_delimiters(self):
        node = TextNode("This `code` and that `code` here", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(
            new_nodes,
            [
                TextNode("This ", TextType.TEXT),
                TextNode("code", TextType.CODE),
                TextNode(" and that ", TextType.TEXT),
                TextNode("code", TextType.CODE),
                TextNode(" here", TextType.TEXT),
            ]
        )

    def test_delimiter_at_start(self):
        node = TextNode("**Bold** at the beginning", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(
            new_nodes,
            [
                TextNode("Bold", TextType.BOLD),
                TextNode(" at the beginning", TextType.TEXT),
            ]
        )

    def test_non_text_nodes_ignored(self):
        node1 = TextNode("Already bold", TextType.BOLD)
        node2 = TextNode("Plain text with `code`", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node1, node2], "`", TextType.CODE)
        self.assertEqual(
            new_nodes,
            [
                TextNode("Already bold", TextType.BOLD),
                TextNode("Plain text with ", TextType.TEXT),
                TextNode("code", TextType.CODE),
            ]
        )

    def test_missing_closing_delimiter_raises_error(self):
        node = TextNode("This is **broken markdown syntax", TextType.TEXT)
        with self.assertRaises(ValueError):
            split_nodes_delimiter([node], "**", TextType.BOLD)

    def test_extract_markdown_images(self):
        text = "This is text with a ![rick roll](https://imgur.com) and ![obi wan](https://imgur.com)"
        matches = extract_markdown_images(text)
        self.assertListEqual(
            [
                ("rick roll", "https://imgur.com"),
                ("obi wan", "https://imgur.com")
            ], 
            matches
        )

    def test_extract_markdown_links(self):
        text = "This is text with a link [to boot dev](https://boot.dev) and [to youtube](https://youtube.com)"
        matches = extract_markdown_links(text)
        self.assertListEqual(
            [
                ("to boot dev", "https://boot.dev"),
                ("to youtube", "https://youtube.com")
            ], 
            matches
        )

    def test_links_ignore_images(self):
        # Link extractor must absolutely ignore image syntax
        text = "Here is an image ![star wars](https://imgur.com) and a [real link](https://google.com)"
        link_matches = extract_markdown_links(text)
        self.assertListEqual([("real link", "https://google.com")], link_matches)

    def test_images_ignore_links(self):
        # Image extractor must absolutely ignore standard link syntax
        text = "Here is an image ![star wars](https://imgur.com) and a [real link](https://google.com)"
        image_matches = extract_markdown_images(text)
        self.assertListEqual([("star wars", "https://imgur.com")], image_matches)

    def test_no_matches(self):
        text = "This is a plain text string with no markdown syntax elements at all."
        self.assertListEqual([], extract_markdown_images(text))
        self.assertListEqual([], extract_markdown_links(text))

if __name__ == "__main__":
    unittest.main()
