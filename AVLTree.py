# username - yoavs2
# id1      - 216282996
# name1    - Yoav Steinberg
# id2      - 215387507
# name2    - Edo Friedman


"""A class represnting a node in an AVL tree"""


class AVLNode(object):
    """Constructor, you are allowed to add more fields.

    @type key: int or None
    @param key: key of your node
    @type value: any
    @param value: data of your node
    """

    def __init__(self, key, value):
        self.key = key
        self.value = value
        self.left = None
        self.right = None
        self.parent = None
        self.height = -1
        self.size = 0

    """returns the key

    @rtype: int or None
    @returns: the key of self, None if the node is virtual
    """

    def get_key(self):
        return self.key

    """returns the value

    @rtype: any
    @returns: the value of self, None if the node is virtual
    """

    def get_value(self):
        return self.value

    """returns the left child
    @rtype: AVLNode
    @returns: the left child of self, None if there is no left child (if self is virtual)
    """

    def get_left(self):
        return self.left

    """returns the right child

    @rtype: AVLNode
    @returns: the right child of self, None if there is no right child (if self is virtual)
    """

    def get_right(self):
        return self.right

    """returns the parent 

    @rtype: AVLNode
    @returns: the parent of self, None if there is no parent
    """

    def get_parent(self):
        return self.parent

    """returns the height

    @rtype: int
    @returns: the height of self, -1 if the node is virtual
    """

    def get_height(self):
        return self.height

    """returns the size of the subtree

    @rtype: int
    @returns: the size of the subtree of self, 0 if the node is virtual
    """

    def get_size(self):
        return self.size

    """sets key

    @type key: int or None
    @param key: key
    """

    def set_key(self, key):
        self.key = key

    """sets value

    @type value: any
    @param value: data
    """

    def set_value(self, value):
        self.value = value

    """sets left child

    @type node: AVLNode
    @param node: a node
    """

    def set_left(self, node):
        self.left = node

    """sets right child

    @type node: AVLNode
    @param node: a node
    """

    def set_right(self, node):
        self.right = node

    """sets parent

    @type node: AVLNode
    @param node: a node
    """

    def set_parent(self, node):
        self.parent = node

    """sets the height of the node

    @type h: int
    @param h: the height
    """

    def set_height(self, h):
        self.height = h

    """sets the size of node

    @type s: int
    @param s: the size
    """

    def set_size(self, s):
        self.size = s

    """returns whether self is not a virtual node 

    @rtype: bool
    @returns: False if self is a virtual node, True otherwise.
    """

    def is_real_node(self):
        return self.key is not None


"""
A class implementing an AVL tree.
"""


class AVLTree(object):
    """
    Constructor, you are allowed to add more fields.

    """

    def __init__(self):
        self.root = AVLNode(None, None)

    # add your fields here

    """searches for a node in the dictionary corresponding to the key

    @type key: int
    @param key: a key to be searched
    @rtype: AVLNode
    @returns: node corresponding to key.
    
    Complexity: O(log(n))
    """

    def search(self, key):
        # standard search algorithm in a BST.
        node = self.root
        while node.is_real_node():
            if node.key == key:
                return node
            if key < node.key:
                node = node.left
            elif key > node.key:
                node = node.right
        return None

    """inserts val at position i in the dictionary

    @type key: int
    @pre: key currently does not appear in the dictionary
    @param key: key of item that is to be inserted to self
    @type val: any
    @param val: the value of the item
    @rtype: int
    @returns: the number of rebalancing operation due to AVL rebalancing
    
    Complexity: O(log(n))
    """

    def insert(self, key, val):
        # find leaf to connect the new node to.
        node = self.root
        while node.is_real_node():
            if key < node.key:
                node = node.left
            else:
                node = node.right
        node.key = key
        node.value = val
        node.left = AVLNode(None, None)
        node.right = AVLNode(None, None)
        node.left.parent = node
        node.right.parent = node
        update_attribs(node)
        node = node.parent
        # do rebalancing operations using the algorithm we saw in class.
        rebalancing_ops = 0
        while node is not None:
            rotation_count = do_rotations(self, node)
            rebalancing_ops += rotation_count
            node.size = node.left.size + node.right.size + 1
            if node.height == max(node.left.height, node.right.height) + 1:
                break
            else:
                rebalancing_ops += 1
                node.set_height(max(node.left.height, node.right.height) + 1)
            if rotation_count > 0:
                break
            node = node.parent
        while node is not None:
            node.size = node.left.size + node.right.size + 1
            node = node.parent

        return rebalancing_ops

    """deletes node from the dictionary

    @type node: AVLNode
    @pre: node is a real pointer to a node in self
    @rtype: int
    @returns: the number of rebalancing operation due to AVL rebalancing
    
    Complexity: O(log(n))
    """

    def delete(self, node):
        rebalancing_ops = 0
        # Delete normally.
        if node.height == 0:  # leaf.
            if node.parent is not None:
                # find if node is left or right child of its parent and remove it.
                if node.parent.right == node:
                    node.parent.right = AVLNode(None, None)
                    node.parent.right.parent = node.parent
                elif node.parent.left == node:
                    node.parent.left = AVLNode(None, None)
                    node.parent.left.parent = node.parent
            else:
                self.root = AVLNode(None, None)
                self.root.parent = node.parent
            parent = node.parent
        elif not node.left.is_real_node():  # no left child
            if node.parent is not None:
                # find if node is left or right child of its parent and remove it.
                if node.parent.right == node:
                    node.parent.right = node.right
                elif node.parent.left == node:
                    node.parent.left = node.right
            else:
                self.root = node.right
            node.right.parent = node.parent
            parent = node.parent
        elif not node.right.is_real_node():  # no right child
            if node.parent is not None:
                # find if node is left or right child of its parent and remove it.
                if node.parent.right == node:
                    node.parent.right = node.left
                elif node.parent.left == node:
                    node.parent.left = node.left
            else:
                self.root = node.left
            node.left.parent = node.parent
            parent = node.parent
        else:
            # find successor
            successor = node.right
            while successor.left.is_real_node():
                successor = successor.left

            # remove successor
            if successor.parent.left == successor:
                successor.parent.left = successor.right  # if successor.right doesn't exist it's a virtual node
            else:
                successor.parent.right = successor.right
            successor.right.parent = successor.parent

            if successor.parent == node:
                # in this case the parent of the physically deleted node is about to be removed
                parent = successor
            else:
                parent = successor.parent

            # replace node with successor
            successor.left = node.left
            successor.left.parent = successor
            successor.right = node.right
            successor.right.parent = successor
            successor.parent = node.parent
            if node.parent is not None:
                if node.parent.left == node:
                    node.parent.left = successor
                else:
                    node.parent.right = successor
            else:
                self.root = successor

            if successor.height != max(successor.left.height, successor.right.height) + 1:
                rebalancing_ops += 1
                successor.set_height(max(successor.left.height, successor.right.height) + 1)
            successor.size = successor.left.size + successor.right.size + 1

        # Fix BF
        while parent is not None:
            parent.size = parent.left.size + parent.right.size + 1
            if parent.height != max(parent.left.height, parent.right.height) + 1:
                rebalancing_ops += 1
                parent.set_height(max(parent.left.height, parent.right.height) + 1)
                # height_changed = True
            # else:
            # height_changed = False
            rotation_count = do_rotations(self, parent)
            rebalancing_ops += rotation_count
            # if rotation_count == 0 and not height_changed:
            #     break
            parent = parent.parent
        return rebalancing_ops

    """returns an array representing dictionary 

    @rtype: list
    @returns: a sorted list according to key of tuples (key, value) representing the data structure
    
    Complexity: O(n)
    """

    def avl_to_array(self):
        arr = [0] * self.size()  # create array to store final result
        self.avl_to_array_rec(arr, self.root, 0)  # call recursive function to modify array accordingly.
        return arr

    """recursively creates a sorted array of (key, value) pairs from an avl tree
    @type node: array
    @param node: the array to place the (key, value) pairs into
    @type node: AVLNode
    @param node: the subtree to add to the array
    @type index: int
    @param index: the array index to put the first (key, value) pair in
    
    Complexity: O(n)
    """

    def avl_to_array_rec(self, array, node, index):
        if not node.is_real_node():
            return
        self.avl_to_array_rec(array, node.left, index)
        index += node.left.size
        array[index] = (node.key, node.value)
        index += 1
        self.avl_to_array_rec(array, node.right, index)

    """returns the number of items in dictionary 

    @rtype: int
    @returns: the number of items in dictionary 
    """

    def size(self):
        return self.root.get_size()

    """splits the dictionary at a given node

    @type node: AVLNode
    @pre: node is in self
    @param node: The intended node in the dictionary according to whom we split
    @rtype: list
    @returns: a list [left, right], where left is an AVLTree representing the keys in the 
    dictionary smaller than node.key, right is an AVLTree representing the keys in the 
    dictionary larger than node.key.
    
    Complexity: O(log(n))
    """

    def split(self, node):
        less = AVLTree()
        less.root = node.left
        less.root.parent = None
        greater = AVLTree()
        greater.root = node.right
        greater.root.parent = None
        parent = node.parent
        while parent is not None:
            if node == parent.left:
                right_subtree = AVLTree()
                right_subtree.root = parent.right
                right_subtree.root.parent = None
                greater.join(right_subtree, parent.key, parent.value)
            else:  # node == parent.right
                left_subtree = AVLTree()
                left_subtree.root = parent.left
                left_subtree.root.parent = None
                less.join(left_subtree, parent.key, parent.value)
            node = parent
            parent = node.parent
        return [less, greater]

    """joins self with key and another AVLTree

    @type tree: AVLTree 
    @param tree: a dictionary to be joined with self
    @type key: int 
    @param key: The key separting self with tree
    @type val: any 
    @param val: The value attached to key
    @pre: all keys in self are smaller than key and all keys in tree are larger than key,
    or the other way around.
    @rtype: int
    @returns: the absolute value of the difference between the height of the AVL trees joined +1
    
    Complexity: O(log(n))
    """

    def join(self, tree, key, val):
        if (self.root.is_real_node() and self.root.key < key) or \
                (tree.root.is_real_node() and tree.root.key > key):
            t1 = self
            t2 = tree
        elif (tree.root.is_real_node() and tree.root.key < key) or \
                (self.root.is_real_node() and self.root.key > key):
            t1 = tree
            t2 = self
        else:  # both trees are empty
            self.insert(key, val)
            return 1
        x = AVLNode(key, val)
        height_difference = abs(t2.root.height - t1.root.height) + 1
        if t2.root.height > t1.root.height:
            b = t2.root
            while b.height > t1.root.height:
                b = b.left
            x.left = t1.root
            t1.root.parent = x
            x.right = b
            x.parent = b.parent
            b.parent.left = x
            b.parent = x
            self.root = t2.root
        else:
            b = t1.root
            while b.height > t2.root.height:
                b = b.right
            x.left = b
            x.right = t2.root
            t2.root.parent = x
            x.parent = b.parent
            if b.parent is not None:
                b.parent.right = x
            else:
                t1.root = x
            b.parent = x
            self.root = t1.root
        while x is not None:
            # x.size = x.left.size + x.right.size + 1
            # if x.height == max(x.left.height, x.right.height) + 1:
            #     break
            # else:
            #     x.set_height(max(x.left.height, x.right.height) + 1)
            update_attribs(x)
            do_rotations(self, x)
            x = x.parent
        while x is not None:
            x.size = x.left.size + x.right.size + 1
            x = x.parent
        return height_difference

    """compute the rank of node in the self

    @type node: AVLNode
    @pre: node is in self
    @param node: a node in the dictionary which we want to compute its rank
    @rtype: int
    @returns: the rank of node in self
    
    Complexity: O(log(n))
    """

    def rank(self, node):
        rank = node.left.size + 1
        x = node
        while x.parent is not None:
            if x == x.parent.right:
                rank += x.parent.left.size + 1
            x = x.parent

        return rank

    """finds the i'th smallest item (according to keys) in self

    @type i: int
    @pre: 1 <= i <= self.size()
    @param i: the rank to be selected in self
    @rtype: int
    @returns: the item of rank i in self
    
    Complexity: O(log(n))
    """

    def select(self, i):
        return self.select_rec(self.root, i)

    """recursively finds the i'th smallest item (according to keys) in self

    @type i: int
    @pre: 1 <= i <= self.size()
    @param i: the rank to be selected in x
    @type x: AVLNode
    @param x: root of tree to select in. 
    @rtype: int
    @returns: the item of rank i in self
    
    Complexity: O(log(n))
    """

    def select_rec(self, x, i):
        rank = x.left.size + 1
        if rank == i:  # found the i'th smallest element
            return x
        elif rank > i:  # i'th smallest element is on the left:
            return self.select_rec(x.left, i)
        else:  # i'th smallest element is on the right
            return self.select_rec(x.right, i - rank)

    """returns the root of the tree representing the dictionary

    @rtype: AVLNode
    @returns: the root, None if the dictionary is empty
    """

    def get_root(self):
        if self.root.is_real_node():
            return self.root
        return None


"""rotates a given node right, as seen in class
@type node: AVLNode
@param node: the node to rotate
"""


def rotate_right(tree, node):
    # AVL lecture slide 62
    left_child = node.left
    node.set_left(left_child.right)
    node.left.set_parent(node)
    update_attribs(node)
    left_child.set_right(node)
    update_attribs(left_child)
    left_child.set_parent(node.parent)
    if node.parent is not None:
        if node.parent.left == node:
            node.parent.set_left(left_child)
        else:
            node.parent.set_right(left_child)
        update_attribs(left_child.parent)
    else:  # if node was the root
        tree.root = left_child
    node.set_parent(left_child)


"""rotates a given node left, as seen in class
@type node: AVLNode
@param node: the node to rotate
"""


def rotate_left(tree, node):
    right_child = node.right
    node.set_right(right_child.left)
    node.right.set_parent(node)
    update_attribs(node)
    right_child.set_left(node)
    update_attribs(right_child)
    right_child.set_parent(node.parent)
    if node.parent is not None:
        if node.parent.left == node:
            node.parent.set_left(right_child)
        else:
            node.parent.set_right(right_child)
        update_attribs(right_child.parent)
    else:  # if node was the root
        tree.root = right_child
    node.set_parent(right_child)


"""Checks balance factor and does rotations
    @type node: AVLNode
    @param node: the node to rotate (if needed)
    @rtype: int
    @returns: the number of rotations that have been done
"""


def do_rotations(tree, node):
    if bf(node) == 2:
        if bf(node.left) == -1:
            rotate_left(tree, node.left)
            rotate_right(tree, node)
            return 2
        else:
            rotate_right(tree, node)
            return 1
    elif bf(node) == -2:
        if bf(node.right) == 1:
            rotate_right(tree, node.right)
            rotate_left(tree, node)
            return 2
        else:
            rotate_left(tree, node)
            return 1
    return 0


"""updates a given node's height
@type node: AVLNode
@param node: the node to update
"""


def update_attribs(node):
    node.set_height(max(node.left.height, node.right.height) + 1)
    node.size = node.left.size + node.right.size + 1


"""calculates a given node's balance factor
@type node: AVLNode
@param node: the node to update
@rtype: int
@returns: the node's balance factor
"""


def bf(node):
    return node.left.height - node.right.height
