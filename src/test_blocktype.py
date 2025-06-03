import unittest
import blocktype
from itertools import count
from blocktype import block_to_block_type, BlockType

class TestBlockType(unittest.TestCase):
    def setUp(self):
        blocktype.counter = count(1)

    def test_block_to_block_type(self):
        result = block_to_block_type("This is a paragraph")
        self.assertEqual(result, BlockType.PARAGRAPH)

    def test_heading_one_block_to_block_type(self):
        result = block_to_block_type("# This is a heading")
        self.assertEqual(result, BlockType.HEADING)

    def test_heading_two_block_to_block_type(self):
        result = block_to_block_type("## This is a heading")
        self.assertEqual(result, BlockType.HEADING)
    
    def test_heading_three_block_to_block_type(self):
        result = block_to_block_type("### This is a heading")
        self.assertEqual(result, BlockType.HEADING)

    def test_heading_four_block_to_block_type(self):
        result = block_to_block_type("#### This is a heading")
        self.assertEqual(result, BlockType.HEADING)

    def test_heading_five_block_to_block_type(self):
        result = block_to_block_type("##### This is a heading")
        self.assertEqual(result, BlockType.HEADING)

    def test_heading_six_block_to_block_type(self):
        result = block_to_block_type("###### This is a heading")
        self.assertEqual(result, BlockType.HEADING)

    def test_heading_seven_block_to_block_type(self):
        result = block_to_block_type("####### This is NOT a heading")
        self.assertEqual(result, BlockType.PARAGRAPH)

    def test_code_block_to_block_type(self):
        result = block_to_block_type("```This is a code block```")
        self.assertEqual(result, BlockType.CODE)

    def test_code_extra_symbols_block_to_block_type(self):
        result = block_to_block_type("```This is a code block`````")
        self.assertEqual(result, BlockType.CODE)

    def test_quote_block_to_block_type(self):
        result = block_to_block_type(">This is a quote block")
        self.assertEqual(result, BlockType.QUOTE)

    def test_quote_with_space_block_to_block_type(self):
        result = block_to_block_type("> This is a quote block")
        self.assertEqual(result, BlockType.QUOTE)
    
    def test_double_quote_block_to_block_type(self):
        result = block_to_block_type(">>This is a quote block")
        self.assertEqual(result, BlockType.QUOTE)

    def test_unorded_list_block_to_block_type(self):
        result = block_to_block_type("- This is an unorderd list block")
        self.assertEqual(result, BlockType.UNORDERED_LIST)

    def test_unorded_list_no_space_block_to_block_type(self):
        result = block_to_block_type("-This is an unorderd list block")
        self.assertEqual(result, BlockType.PARAGRAPH)

    def test_orded_list_block_to_block_type(self):
        result = block_to_block_type("1. This is an orderd list block")
        self.assertEqual(result, BlockType.ORDERED_LIST)

    def test_multiple_orded_list_block_to_block_type(self):
        result_one = block_to_block_type("1. This is an orderd list block")
        result_two = block_to_block_type("2. This is an orderd list block")
        result_three = block_to_block_type("3. This is an orderd list block")
        self.assertEqual(result_one, BlockType.ORDERED_LIST)
        self.assertEqual(result_two, BlockType.ORDERED_LIST)
        self.assertEqual(result_three, BlockType.ORDERED_LIST)

    def test_wrong_order_orded_list_block_to_block_type(self):
        result_one = block_to_block_type("1. This is an orderd list block")
        result_two = block_to_block_type("3. This is an orderd list block")
        result_three = block_to_block_type("2. This is an orderd list block")
        self.assertEqual(result_one, BlockType.ORDERED_LIST)
        self.assertEqual(result_two, BlockType.PARAGRAPH)
        self.assertEqual(result_three, BlockType.PARAGRAPH)

if __name__ == "__main__":
    unittest.main()