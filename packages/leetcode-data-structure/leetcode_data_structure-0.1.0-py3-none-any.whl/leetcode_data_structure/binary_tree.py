from __future__ import annotations

from collections import deque


class TreeNode:
    """
    A node in a singly-linked list.

    Attributes:
        val (int): The value of the node.
        next (ListNode or None): The next node in the list.

    Methods:
        to_array: Converts a binary tree into a list of integers.
        from_array: Converts a list of integers into a binary tree.
        get_by_val: Finds a node in a binary tree with the given value.
    """

    def __init__(self, val=0, left: TreeNode | None = None, right: TreeNode | None = None) -> None:
        """
        Initializes a new instance of the TreeNode class.

        Args:
            val (int, optional): The integer value to store in the node. Defaults to 0.
            left (TreeNode | None, optional): The left child node. Defaults to None.
            right (TreeNode | None, optional): The right child node. Defaults to None.
        """
        self.val = val
        self.left: TreeNode | None = left
        self.right: TreeNode | None = right

    def __repr__(self) -> str:
        """
        Returns a string representation of the node.

        Returns:
            str: The string representation of the node.
        """
        return str(self.val)

    @staticmethod
    def from_array(arr: list[int | None]) -> TreeNode | None:
        """
        Converts a list of integers into a binary tree.

        Args:
            arr (list[int | None]): The list of integers to convert. The integers can be None.

        Returns:
            TreeNode | None: The root node of the binary tree, or None if the list is empty.
        """
        if not arr:
            return None
        root = TreeNode(arr[0])
        q = deque([root])
        for i in range(1, len(arr), 2):
            node = q.popleft()
            if arr[i] is not None:
                node.left = TreeNode(arr[i])
                q.append(node.left)
            if i + 1 < len(arr) and arr[i + 1] is not None:
                node.right = TreeNode(arr[i + 1])
                q.append(node.right)

        return root

    @staticmethod
    def to_array(root: TreeNode | None) -> list[int | None]:
        """
        Converts a binary tree into a list of integers.

        Args:
            root (TreeNode | None): The root node of the binary tree.

        Returns:
            list[int | None]: The list of integers representing the binary tree.
            The value 'None' represents a null child node.
        """
        q = deque([root])
        arr: list = []
        while q:
            node = q.popleft()
            if node:
                arr.append(node.val)
                q.append(node.left)
                q.append(node.right)
            else:
                arr.append(None)

        while arr and arr[-1] is None:
            arr.pop()

        return arr

    @staticmethod
    def get_by_val(root: TreeNode, val: int) -> TreeNode | None:
        """
        Finds a node in a binary tree with the given value.

        Args:
            root (TreeNode): The root node of the binary tree.
            val (int): The value to search for.

        Returns:
            TreeNode | None: The node with the given value, or None if it is not found.
        """
        ans = None

        def dfs(node):
            nonlocal ans
            if node is None:
                return

            if node.val == val:
                ans = node
                return

            dfs(node.left)
            dfs(node.right)

        dfs(root)
        return ans

    @staticmethod
    def get_by_vals(root: TreeNode, vals: list[int]) -> list[TreeNode]:
        """Finds all nodes with values in a given list in the binary tree.

        Args:
            root (TreeNode): The root node of the binary tree.
            vals (list[int]): The list of values to search for.

        Returns:
            list[TreeNode]: The list of nodes with the given
        """
        ans: list[TreeNode] = []

        def dfs(node):
            if node is None:
                return

            if node.val in vals:
                ans.append(node)

            dfs(node.left)
            dfs(node.right)

        dfs(root)
        return ans
