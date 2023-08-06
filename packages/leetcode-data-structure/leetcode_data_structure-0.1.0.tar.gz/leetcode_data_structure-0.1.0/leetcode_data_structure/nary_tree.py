from __future__ import annotations

from collections import deque


class Node:
    """
    A node in a tree data structure with a value and a list of children nodes.

    Attributes:
        val: The value of the node.
        children: The list of children nodes.

    Methods:
        to_array: Converts the tree rooted at this node to a list.
        from_array: Constructs a tree rooted at this node from a list.
    """

    def __init__(self, val=None, children=None) -> None:
        """
        Initializes a new Node object with a value and a list of children.

        Args:
            val: The value of the node.
            children: A list of children nodes.
        """
        self.val = val
        self.children: list[Node] = children if children is not None else []

    def __repr__(self) -> str:
        """
        Returns a string representation of the node.

        Returns:
            str: The string representation of the node.
        """
        return str(self.val)

    @staticmethod
    def to_array(root: Node) -> list[int]:
        """
        Converts the tree rooted at the specified node to a list.

        Args:
            root: The root node of the tree.

        Returns:
            list[int]: The list representation of the tree.
        """
        q = deque[Node]()
        q.append(root)
        arr = [root.val, None]
        qSize = len(q)
        while qSize > 0:
            for i in range(qSize):
                n: Node = q.popleft()

                for child in n.children:
                    arr.append(child.val)
                    q.append(child)
                arr.append(None)
            qSize = len(q)
        # trim
        while arr[-1] is None:
            arr = arr[:-1]
        return arr

    @staticmethod
    def from_array(arr: list[int]) -> Node:
        """
        Constructs a tree rooted at this node from a list.

        Args:
            arr: The list representation of the tree.

        Returns:
            Node: The root node of the tree.
        """
        q = deque[Node]()
        root = Node(arr[0])
        q.append(root)
        qSize = len(q)
        index = 2
        while qSize > 0 and index < len(arr):
            for i in range(qSize):
                n: Node = q.popleft()
                while index < len(arr) and arr[index] is not None:
                    subNode = Node(arr[index])
                    n.children.append(subNode)
                    q.append(subNode)
                    index += 1
                index += 1
            qSize = len(q)
        return root
