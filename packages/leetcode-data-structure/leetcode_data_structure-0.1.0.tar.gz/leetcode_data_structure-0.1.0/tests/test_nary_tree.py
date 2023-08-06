import unittest
from typing import List

from leetcode_data_structure import Node


class TestStringMethods(unittest.TestCase):
    def test_1(self):
        test(self, [1, None, 3, 2, 4, None, 5, 6])

    def test_2(self):
        test(self, [1, None, 2])

    def test_3(self):
        test(
            self,
            [
                1,
                None,
                2,
                3,
                4,
                5,
                None,
                None,
                6,
                7,
                None,
                8,
                None,
                9,
                10,
                None,
                None,
                11,
                None,
                12,
                None,
                13,
                None,
                None,
                14,
            ],
        )

    def test_4(self):
        test(self, [1, None, 2, 2, None, 3, None, 3])


def test(testObj: unittest.TestCase, nums: List[int]) -> None:
    root = Node.from_array(nums)
    actual = Node.to_array(root)

    testObj.assertEqual(actual, nums)


if __name__ == "__main__":
    unittest.main()
