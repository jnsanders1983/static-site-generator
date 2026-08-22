import unittest
from gencontent import extract_title

class TestGenContent(unittest.TestCase):
    def test_extract_title_standard(self):
        md = "# Hello World"
        self.assertEqual(extract_title(md), "Hello World")
        
    def test_extract_title_with_whitespace(self):
        md = "   #    Clean Title    \nParagraph data here."
        self.assertEqual(extract_title(md), "Clean Title")
        
    def test_extract_title_missing_raises_exception(self):
        md = "## Subheader line\nPlain paragraph string."
        with self.assertRaises(ValueError):
            extract_title(md)
            
    def test_extract_title_multiline_fallback(self):
        md = "Some introductory line text\n\n# Dynamic Target Header\n- Bullet items"
        self.assertEqual(extract_title(md), "Dynamic Target Header")

if __name__ == "__main__":
    unittest.main()
