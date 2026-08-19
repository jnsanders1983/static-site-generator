from inline_markdown import ( split_nodes_delimiter, extract_markdown_images, 
                                extract_markdown_links, split_nodes_image,
                                split_nodes_link, text_to_textnodes,
                                markdown_to_blocks
                            )  
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

    def test_split_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode("second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"),
            ],
            new_nodes,
        )

    def test_split_image_at_start(self):
        node = TextNode("![start](img.png) trailing words here", TextType.TEXT)
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("start", TextType.IMAGE, "img.png"),
                TextNode(" trailing words here", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_split_image_at_end(self):
        node = TextNode("Leading text here ![end](img.png)", TextType.TEXT)
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("Leading text here ", TextType.TEXT),
                TextNode("end", TextType.IMAGE, "img.png"),
            ],
            new_nodes,
        )

    def test_split_links(self):
        node = TextNode(
            "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is text with a link ", TextType.TEXT),
                TextNode("to boot dev", TextType.LINK, "https://www.boot.dev"),
                TextNode(" and ", TextType.TEXT),
                TextNode("to youtube", TextType.LINK, "https://www.youtube.com/@bootdotdev"),
            ],
            new_nodes,
        )

    def test_no_images_or_links(self):
        node = TextNode("Just completely plain text with zero markdown tags.", TextType.TEXT)
        self.assertListEqual([node], split_nodes_image([node]))
        self.assertListEqual([node], split_nodes_link([node]))

    def test_non_text_nodes_preserved(self):
        bold_node = TextNode("Bold block", TextType.BOLD)
        link_node = TextNode("Click [here](url)", TextType.TEXT)
        
        nodes = [bold_node, link_node]
        result = split_nodes_link(nodes)
        
        self.assertEqual(result[0], bold_node)
        self.assertEqual(result[1], TextNode("Click ", TextType.TEXT))
        self.assertEqual(result[2], TextNode("here", TextType.LINK, "url"))

    def test_comprehensive_text_to_nodes(self):
        text = "This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://imgur.com) and a [link](https://boot.dev)"
        nodes = text_to_textnodes(text)
        
        self.assertListEqual(
            [
                TextNode("This is ", TextType.TEXT),
                TextNode("text", TextType.BOLD),
                TextNode(" with an ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
                TextNode(" word and a ", TextType.TEXT),
                TextNode("code block", TextType.CODE),
                TextNode(" and an ", TextType.TEXT),
                TextNode("obi wan image", TextType.IMAGE, "https://imgur.com"),
                TextNode(" and a ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://boot.dev"),
            ],
            nodes
        )

    def test_pure_plain_text(self):
        text = "Just plain text without any formatting whatsoever."
        nodes = text_to_textnodes(text)
        self.assertListEqual([TextNode(text, TextType.TEXT)], nodes)

    def test_empty_string(self):
        nodes = text_to_textnodes("")
        self.assertListEqual([], nodes)

    def test_markdown_to_blocks(self):
        # Starter test case with flush-left multiline strings
        md = """This is **bolded** paragraph

                This is another paragraph with _italic_ text and `code` here
                This is the same paragraph on a new line

                - This is a list
                - with items"""

        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )

    def test_markdown_to_blocks_excessive_newlines(self):
        # Ensures that multiple consecutive empty lines are correctly discarded
        md = """# This is a heading



This is a normal paragraph block.


- List item 1
- List item 2"""
        
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "# This is a heading",
                "This is a normal paragraph block.",
                "- List item 1\n- List item 2"
            ]
        )

    def test_markdown_to_blocks_whitespace_surround(self):
        # Verifies that leading/trailing document whitespace gets stripped entirely
        md = """  
# Heading with leading spaces
  
Paragraph block text here.
  
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "# Heading with leading spaces",
                "Paragraph block text here."
            ]
        )

    def test_markdown_to_blocks_single_block(self):
        # A single line doc shouldn't break or generate empty trailing blocks
        md = "Just a lone paragraph."
        blocks = markdown_to_blocks(md)
        self.assertEqual(blocks, ["Just a lone paragraph."])
if __name__ == "__main__":
    unittest.main()
