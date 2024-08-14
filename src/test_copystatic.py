import unittest

from copystatic import extract_title


class TestCopyStatic(unittest.TestCase):
    def test_extract_title(self):
        heading1 = "# heading 1"
        self.assertEqual(extract_title(heading1), "heading 1")
        example = "# Example title"
        self.assertEqual(extract_title(example), "Example title")
        bad_title = "## bad title"
        self.assertRaises(Exception, extract_title, bad_title)
        long_example = """
        paragraph

        # Title

        ## Sub heading

        other paragraph
        """
        self.assertEqual(extract_title(long_example), "Title")