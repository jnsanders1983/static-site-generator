import unittest
from textnode import TextNode, TextType


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

    def test_eq_with_url(self):
            node = TextNode("This is a text node", TextType.BOLD, "https://boot.dev")
            node2 = TextNode("This is a text node", TextType.BOLD, "https://boot.dev")
            self.assertEqual(node, node2)

    def test_not_eq_text(self):
                node = TextNode("This is a text node", TextType.BOLD, "https://boot.dev")
                node2 = TextNode("This is different text", TextType.BOLD, "https://boot.dev")
                self.assertNotEqual(node, node2)

    def test_not_eq_text_type(self):
                    node = TextNode("This is a text node", TextType.BOLD, "https://boot.dev")
                    node2 = TextNode("This is a text node", TextType.ITALIC, "https://boot.dev")
                    self.assertNotEqual(node, node2)

    def test_not_eq_url(self):
                        node = TextNode("This is a text node", TextType.BOLD, "https://boot.dev")
                        node2 = TextNode("This is a text node", TextType.BOLD, "https://www.google.com")
                        self.assertNotEqual(node, node2)
                        
    def test_not_eq_url_none(self):
                    node = TextNode("This is a text node", TextType.BOLD, "https://boot.dev")
                    node2 = TextNode("This is a text node", TextType.BOLD)
                    self.assertNotEqual(node, node2)

if __name__ == "__main__":
    unittest.main()