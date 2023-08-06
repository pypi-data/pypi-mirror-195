import unittest

from leetcode_data_structure.link_list import ListNode


class TestListNode(unittest.TestCase):
    def test_ListNode(self) -> None:
        # Test from_array and to_array
        arr = [1, 2, 3, 4, 5]
        head = ListNode.from_array(arr)
        assert ListNode.to_array(head) == arr

        arr = [1]
        head = ListNode.from_array(arr)
        assert ListNode.to_array(head) == arr

        arr = []
        head = ListNode.from_array(arr)
        assert ListNode.to_array(head) == arr

        # Test with None
        head = None
        assert ListNode.to_array(head) == []

        # Test initialization
        node = ListNode()
        assert node.val == 0
        assert node.next is None

        node = ListNode(1)
        assert node.val == 1
        assert node.next is None

    def test_to_array(self):
        # Test case 1: empty linked list
        head = None
        self.assertEqual(ListNode.to_array(head), [])

        # Test case 2: single element linked list
        head = ListNode(5)
        self.assertEqual(ListNode.to_array(head), [5])

        # Test case 3: multiple element linked list
        head = ListNode(1, ListNode(2, ListNode(3, ListNode(4, ListNode(5)))))
        self.assertEqual(ListNode.to_array(head), [1, 2, 3, 4, 5])


if __name__ == '__main__':
    unittest.main()
