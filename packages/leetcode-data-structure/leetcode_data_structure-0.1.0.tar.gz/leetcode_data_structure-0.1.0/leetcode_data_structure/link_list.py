from __future__ import annotations


class ListNode:
    """
    A node in a singly-linked list.

    Attributes:
        val (int): The value of the node.
        next (ListNode or None): The next node in the list.

    Methods:
        to_array: Converts a linked list into an array of integers.
        from_array: Converts an array of integers into a linked list.
    """

    def __init__(self, val=0, next=None) -> None:
        """
        Initializes a new instance of the ListNode class.

        Args:
            val (int, optional): The value of the node. Defaults to 0.
            next (ListNode, optional): The next node in the list. Defaults to None.
        """
        self.val: int = val
        self.next: ListNode | None = next

    def __repr__(self) -> str:
        """
        Returns a string representation of the node.

        Returns:
            str: The string representation of the node.
        """
        return str(self.val)

    @staticmethod
    def from_array(arr: list[int]) -> ListNode | None:
        """
        Converts an array of integers into a linked list.

        Args:
            arr (list[int]): The array of integers representing the linked list.

        Returns:
            ListNode: The head node of the linked list.
            None: If the input array is empty.
        """
        n = len(arr)
        if n == 0:
            return None
        head = ListNode(arr[0])
        current = head
        for i in range(1, n):
            next = ListNode(arr[i])
            current.next = next
            current = next

        return head

    @staticmethod
    def to_array(head: ListNode | None) -> list[int]:
        """
        Converts a linked list into an array of integers.

        Args:
            head (ListNode | None): The head node of the linked list.

        Returns:
            list[int]: The array of integers representing the linked list.
        """
        arr: list = []
        current: ListNode | None = head
        while current is not None:
            arr.append(current.val)
            current = current.next
        return arr
