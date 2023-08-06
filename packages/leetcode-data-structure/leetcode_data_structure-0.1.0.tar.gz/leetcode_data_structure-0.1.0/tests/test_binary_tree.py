import unittest
from typing import List

from leetcode_data_structure import TreeNode


def test(testObj: unittest.TestCase, nums: List[int]) -> None:
    root = TreeNode.from_array(nums)
    actual = TreeNode.to_array(root)

    testObj.assertEqual(actual, nums)


class TestStringMethods(unittest.TestCase):
    def test_1(self):
        test(self, [1, 2, 3, 4, 5])

    def test_2(self):
        test(self, [1, None, 2])

    def test_3(self):
        test(self, [1, 2, 2, 3, 4, 4, 3])

    def test_4(self):
        test(self, [1, 2, 2, None, 3, None, 3])


if __name__ == "__main__":
    unittest.main()
