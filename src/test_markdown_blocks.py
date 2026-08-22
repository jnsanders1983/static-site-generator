import unittest
from markdown_blocks import block_to_block_type, BlockType

class TestBlockToBlockType(unittest.TestCase):

    def test_paragraph(self):
        block = "This is a normal paragraph of text with multiple words."
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    def test_headings(self):
        self.assertEqual(block_to_block_type("# Heading 1"), BlockType.HEADING)
        self.assertEqual(block_to_block_type("### Heading 3"), BlockType.HEADING)
        self.assertEqual(block_to_block_type("###### Heading 6"), BlockType.HEADING)

    def test_invalid_headings(self):
        # Missing space
        self.assertEqual(block_to_block_type("#Heading"), BlockType.PARAGRAPH)
        # Too many hashes
        self.assertEqual(
            block_to_block_type("####### Heading 7"), BlockType.PARAGRAPH
        )

    def test_code_block(self):
        block = "```\ndef my_func():\n    return True\n```"
        self.assertEqual(block_to_block_type(block), BlockType.CODE)

    def test_invalid_code_block(self):
        # Missing newline after initial backticks
        block = "```def my_func():\n    return True\n```"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    def test_quote_blocks(self):
        # With spaces after '>'
        block = "> This is a quote\n> line two"
        self.assertEqual(block_to_block_type(block), BlockType.QUOTE)
        # Without spaces after '>'
        block_no_space = ">This is a quote\n>line two"
        self.assertEqual(block_to_block_type(block_no_space), BlockType.QUOTE)

    def test_invalid_quote_block(self):
        # One line misses the '>'
        block = "> This is a quote\n line two"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    def test_unordered_list(self):
        block = "- Item 1\n- Item 2\n- Item 3"
        self.assertEqual(block_to_block_type(block), BlockType.UNORDERED_LIST)

    def test_invalid_unordered_list(self):
        # Missing space on the second item
        block = "- Item 1\n-Item 2"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    def test_ordered_list(self):
        block = "1. First item\n2. Second item\n3. Third item"
        self.assertEqual(block_to_block_type(block), BlockType.ORDERED_LIST)

    def test_invalid_ordered_list_numbers(self):
        # Does not start at 1
        block_wrong_start = "2. First item\n3. Second item"
        self.assertEqual(
            block_to_block_type(block_wrong_start), BlockType.PARAGRAPH
        )

        # Skips a number
        block_skipped_num = "1. First item\n3. Second item"
        self.assertEqual(
            block_to_block_type(block_skipped_num), BlockType.PARAGRAPH
        )

        # Missing space
        block_missing_space = "1.First item\n2.Second item"
        self.assertEqual(
            block_to_block_type(block_missing_space), BlockType.PARAGRAPH
        )

#if __name__ == "__main__":
#    unittest.main()