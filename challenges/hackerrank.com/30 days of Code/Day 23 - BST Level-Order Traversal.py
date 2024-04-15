import sys

class Node:
    def __init__(self,data):
        self.right=self.left=None
        self.data = data
class Solution:
    def insert(self,root,data):
        if root==None:
            return Node(data)
        else:
            if data<=root.data:
                cur=self.insert(root.left,data)
                root.left=cur
            else:
                cur=self.insert(root.right,data)
                root.right=cur
        return root

    def levelOrder(self,root):
        #Write your code here

        from queue import Queue

        pending_nodes = Queue()
        pending_nodes.put(root)
        result = []

        while not pending_nodes.empty():
            # Lets do a pre-order traversal
            node = pending_nodes.get()
            result.append(str(node.data))
            if node.left:
                pending_nodes.put(node.left)
            if node.right:
                pending_nodes.put(node.right)
        print(' '.join(result))

T=int(input())
myTree=Solution()
root=None
for i in range(T):
    data=int(input())
    root=myTree.insert(root,data)
myTree.levelOrder(root)
