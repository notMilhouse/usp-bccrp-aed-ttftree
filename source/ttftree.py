__author__ = ["Gabriel Carvalho Silva", "Paulo Roberto Domingues dos Santos"]
__credits__ = ["Gabriel Carvalho Silva", "Maria Vitória Ribeiro Mendes", "Paulo Roberto Domingues dos Santos"]
__maintainer__ = ["Gabriel Carvalho", "Paulo Roberto Domingues dos Santos"]
__email__ = ["gabriel_carvalho@usp.br", "pds712@usp.br"]

"""
Over commenting was avoided and self documented code was preferred
"""


# contains the information and logic related to the tree father_node
class TTFTreeNode:
    max_keys = 3
    max_children = 4

    def __init__(self, is_leaf):
        self.keys = []
        self.children = []
        self.is_leaf = is_leaf

    # this method returns how many keys the father_node is holding
    def num_keys(self):
        return len(self.keys)

    # this method returns how many children the father_node points to
    def num_children(self):
        return len(self.children)

    # easy way to encapsulate checking data
    def is_last_child(self, child):
        return child == self.children[-1]

    def get_last_child(self):
        return self.children[-1]

    def get_last_key(self):
        return self.keys[-1]

    def get_rightmost_child(self):
        if self.is_leaf:
            return self

        last_child = self.get_last_child()
        return last_child.get_rightmost_child()

    """
    when inserting, the list method insert, 
    provided by the standard library,
    pushes current value in index forward automatically
    """

    def insert_key(self, key, index):
        self.keys.insert(index, key)

    def remove_key(self, key):
        removed = self.keys.remove(key)
        return removed

    def insert_child(self, child, index):
        self.children.insert(index, child)

    def remove_child(self, child):
        self.children.remove(child)
        return child

    # information about the father_node should be encapsulated, so this method informs
    #   if a father_node should be split without giving access to its private information
    # tells if the father_node has valid amounts of keys and children
    def should_split(self):
        reached_max_keys = TTFTreeNode.max_keys < self.num_keys()
        reached_max_children = TTFTreeNode.max_children < self.num_children()
        should_split = reached_max_keys or reached_max_children
        return should_split

    def has_key_underflow(self):
        return self.num_keys() < 1

    def has_children_overflow(self):
        return self.num_children() - self.num_keys() != 1

    def merge_children(self, target_index, sibling_index):
        target_node = self.children[target_index]
        sibling_node = self.children[sibling_index]

        target_node_relative_position = sibling_index - target_index

        for key in sibling_node.keys:
            if target_node_relative_position == -1:
                target_node.insert_key(key, 0)
            else:
                target_node.keys.append(key)

        for child in sibling_node.children:
            if target_node_relative_position == -1:
                target_node.insert_child(child, 0)
            else:
                target_node.children.append(child)

        self.remove_child(sibling_node)

    """
    {content} holds the stringfied keys in the father_node
    the keys in the children are added to content recursivelly
    adding tabs as you walk down the three.
    Also, children are presented in the order they would be in the tree
    """

    def __str__(self, level=0):
        content = "nivel {}: ".format(level) + "\t" * level
        for key in self.keys:
            content += str(key) + " "
        content += "\n"
        for child in self.children:
            content += child.__str__(level + 1)
        return content


# Represents a search for a key in a father_node
# in case the key was found, all information is what it seems to be
# otherwise, they inform where it would be expected to be
class TTFTreeSearchResult:
    def __init__(self, father_node: TTFTreeNode, target_node: TTFTreeNode, target_key_index, child_index, match):
        self.father_node = father_node
        self.target_node = target_node
        # where the key is or was expected to be
        self.target_key_index = target_key_index
        # the child index in the father_node that refers to the node where the key is or was expected to be
        self.child_index = child_index
        self.match = match

    def to_string(self):
        print("Indice: {}\nMatch: {}".format(self.target_key_index, self.match))


# The stack trace contains a stack of TTFTreeSearchResult objects
#   thus it represents a history, or log, of a search operation
#   through it, you may have access to all nodes that were visited in a walk

class TTFTreeSearchStackTrace:
    def __init__(self, trace_list=None):
        if trace_list is None:
            trace_list = []
        self.log = trace_list

    def add_log(self, search_result):
        self.log.append(search_result)

    # gives you access to the most recent search result, or the top element in the stack
    #   it does not remove it from the stack tho
    def get_last(self):
        return self.log[-1]

    # if you want to "go back in time" this method gives you all the search result log
    #   except for the most recent. In other words, it pops the top element in the stack and
    #   retrieves the remaining data in the stack (still as a stack)
    def get_previous(self):
        if len(self.log) == 1:
            interval = self.log
        else:
            interval = self.log[0:-1]
        return TTFTreeSearchStackTrace(interval)


class TTFTree:

    def __init__(self):
        self.root = TTFTreeNode(True)

    def find(self, key):
        trace_find = TTFTreeSearchStackTrace()
        trace_find = self._find(None, self.root, 0, key, trace_find)
        return trace_find

    def _find(self, father_node, candidate_node, child_index, key, trace_find: TTFTreeSearchStackTrace):
        index = 0

        while index < candidate_node.num_keys() and key > candidate_node.keys[index]:
            index = index + 1

        if index < candidate_node.num_keys() and key == candidate_node.keys[index]:
            trace_find.add_log(TTFTreeSearchResult(father_node, candidate_node, index, child_index, True))
            return trace_find
        elif candidate_node.is_leaf:
            trace_find.add_log(TTFTreeSearchResult(father_node, candidate_node, index, child_index, False))
            return trace_find
        else:
            trace_find.add_log(TTFTreeSearchResult(father_node, candidate_node, index, child_index, False))
            return self._find(candidate_node, candidate_node.children[index], index, key, trace_find)

    def insert(self, key):
        key_search_stack_trace = self.find(key)
        key_search_result = key_search_stack_trace.get_last()

        if key_search_result.match:
            print("Valor ja existe na arvore...")

        else:
            key_search_result.target_node.insert_key(key, key_search_result.target_key_index)

            should_split = key_search_result.target_node.should_split()

            if should_split:
                self._split(key_search_stack_trace)

    def _split(self, key_search_stack_trace: TTFTreeSearchStackTrace):
        node_reference = key_search_stack_trace.get_last()

        if node_reference.target_node == self.root:
            subtree_root_node = TTFTreeNode(False)
            new_sibling_node = TTFTreeNode(node_reference.target_node.is_leaf)

            subtree_root_node.insert_child(node_reference.target_node, node_reference.child_index)

            self.root = subtree_root_node

        else:
            subtree_root_node = node_reference.father_node
            new_sibling_node = TTFTreeNode(node_reference.target_node.is_leaf)

        subtree_root_node.insert_child(new_sibling_node, node_reference.child_index + 1)

        median_key = node_reference.target_node.keys[2]
        subtree_root_node.insert_key(median_key, node_reference.child_index)
        # child_index because it is from where the key came

        for key in node_reference.target_node.keys:
            if key > median_key:
                new_sibling_node.insert_key(key, 3)

        if not node_reference.target_node.is_leaf:
            for index in range(0, node_reference.target_node.num_keys()):
                if node_reference.target_node.keys[index] > median_key:
                    new_sibling_node.insert_child(node_reference.target_node.children[index], index)
            new_sibling_node.insert_child(node_reference.target_node.children[4], 3)
            node_reference.target_node.remove_child(node_reference.target_node.children[3])
            node_reference.target_node.remove_child(node_reference.target_node.children[3])

        node_reference.target_node.remove_key(node_reference.target_node.keys[2])
        node_reference.target_node.remove_key(node_reference.target_node.keys[2])

        if node_reference.father_node is not None:
            should_split_father = node_reference.father_node.should_split()

            if should_split_father:
                new_stack_trace = key_search_stack_trace.get_previous()
                self._split(new_stack_trace)

    def remove(self, key):
        key_search_stack_trace = self.find(key)
        key_search_result: TTFTreeSearchResult = key_search_stack_trace.get_last()

        if not key_search_result.match:
            print("Valor nao existe na arvore...")

        else:
            key_search_result.target_node.remove_key(key)
            # After removing the key, checks for necessary rebalancing
            if key_search_result.target_node.is_leaf:
                self._rebalance_leaf_node_key(key_search_stack_trace)
            else:
                self._rebalance_internal_node_key(key_search_stack_trace)

    def _rebalance_leaf_node_key(self, key_search_stack_trace: TTFTreeSearchStackTrace):
        search_result = key_search_stack_trace.get_last()
        leaf_node: TTFTreeNode = search_result.target_node

        # If the node suffers from underflow, performs necessary rotations
        if leaf_node.has_key_underflow() and leaf_node != self.root:
            self._transfer(key_search_stack_trace)

    def _rebalance_internal_node_key(self, key_search_stack_trace):
        last_search_result: TTFTreeSearchResult = key_search_stack_trace.get_last()
        internal_node: TTFTreeNode = last_search_result.target_node
        internal_node_key_index = last_search_result.target_key_index

        if internal_node.num_keys() == 0 and internal_node.num_children() == 1:
            self._transfer(key_search_stack_trace)

        else:
            imediate_predecessor_node = internal_node.children[internal_node_key_index].get_rightmost_child()
            imediate_predecessor_key = imediate_predecessor_node.get_last_key()
            stack_trace_for_predecessor = self.find(imediate_predecessor_key)

            internal_node.insert_key(imediate_predecessor_key, internal_node_key_index)

            imediate_predecessor_node.remove_key(imediate_predecessor_key)

            self._rebalance_leaf_node_key(stack_trace_for_predecessor)

    def _transfer(self, key_search_stack_trace):

        search_result: TTFTreeSearchResult = key_search_stack_trace.get_last()
        father_node: TTFTreeNode = search_result.father_node
        target_node: TTFTreeNode = search_result.target_node

        """
            By default, the target node borrows from its next right sibling
            however, if it is the the last child of its father, then there is no right sibling
            we solve this by borrowing from its next left sibling
            
            shift_child stands for the direction we must go to find the sibling
                1 if it is to the right
                -1 otherwise
            sibling_key_index is the index from where we will get the sibling's key
                0 if shift_child == 1, because we will get the lowest value
                -1 to get the greatest
        """
        if target_node == father_node.get_last_child():
            shift_child = -1
            sibling_key_index: int = -1
        else:
            shift_child = 1
            sibling_key_index: int = 0

        sibling_index = search_result.child_index + shift_child
        sibling_node: TTFTreeNode = father_node.children[sibling_index]

        inherited_key_index_shift = sibling_key_index  # if target node is the last child, the shift is -1, 0 otherwise
        inherited_key_index = search_result.child_index + inherited_key_index_shift
        key_from_father = father_node.keys[inherited_key_index]
        key_from_sibling = sibling_node.keys[sibling_key_index]

        target_node.insert_key(key_from_father, 0)
        father_node.remove_key(key_from_father)

        # if the sibling has only 1 child left, we must perform a merge instead of a full rotation
        if sibling_node.num_keys() < 2:
            father_node.merge_children(search_result.child_index, sibling_index)
            if father_node.has_key_underflow():
                has_all_root_children_been_merged = father_node == self.root and father_node.num_children() == 1
                if has_all_root_children_been_merged:
                    self.root = target_node
                else:
                    self._rebalance_internal_node_key(key_search_stack_trace.get_previous())

        else:
            father_node.insert_key(key_from_sibling, search_result.child_index)
            sibling_node.remove_key(key_from_sibling)

            # if the node is not leaf and the sibling can lend keys, and the node suffered from a
            # key underflow (since we are in this function...), then we must get not only the key
            # but the children "before" the key as well
            if not target_node.is_leaf:
                child_from_sibling = sibling_node.children[sibling_key_index]
                popped_from_sibling = sibling_node.remove_child(child_from_sibling)

                target_node_relative_position = sibling_index - search_result.child_index

                if target_node_relative_position == -1:
                    target_node.insert_child(popped_from_sibling, 0)
                else:
                    target_node.children.append(popped_from_sibling)

    def to_string(self):
        print(self.root)


# manual testing
def manual_insertion_test():
    tree = TTFTree()

    while True:
        print("Para sair digite 'e'")
        user_input = input("Para adicionar um valor na árvore: ")
        if user_input == 'e':
            break
        to_insert = int(user_input)
        tree.insert(to_insert)
        tree.to_string()
    return tree


# pre-built test 1

def pre_built_insertion_test_one():
    tree = TTFTree()
    for i in range(0, 500):
        tree.insert(i)
        tree.to_string()

    return tree


def pre_built_removal_test_one(tree: TTFTree):
    for i in range(0, 500):
        tree.remove(i)
        tree.to_string()

    return tree


# pre-built test 2

def pre_built_insertion_test_two():
    tree = TTFTree()
    for i in range(-20, 25):
        tree.insert(i)
        tree.to_string()
    return tree


def pre_built_removal_test_two(tree: TTFTree):
    for i in range(-20, 25):
        tree.remove(i)
        tree.to_string()

    return tree


def pre_built_insertion_test_three():
    tree = TTFTree()
    keys = [5, 10, 15, 18, 20, 25, 30, 35, 40, 45, 50, 55, 60, 65, 70, 75, 80]
    for key in keys:
        tree.insert(key)
        tree.to_string()
    return tree


def main():
    tree = pre_built_insertion_test_two()
    pre_built_removal_test_two(tree)


if __name__ == '__main__':
    main()
