__author__ = "Gabriel Carvalho Silva"
__credits__ = ["Gabriel Carvalho Silva", "Maria Vitória Ribeiro Mendes"]
__maintainer__ = "Gabriel Carvalho"
__email__ = "gabriel_carvalho@usp.br"

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

    def get_last_key(self):
        return self.keys[-1]

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
        removed = self.children.remove(child)
        return removed

    # information about the father_node should be encapsulated, so this method informs
    #   if a father_node should be split without giving access to its private information
    # tells if the father_node has valid amounts of keys and children
    def should_split(self):
        reached_max_keys = TTFTreeNode.max_keys < self.num_keys()
        reached_max_children = TTFTreeNode.max_children < self.num_children()
        should_split = reached_max_keys or reached_max_children
        return should_split

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
    def __init__(self, father_node: TTFTreeNode, target_node: TTFTreeNode, target_key_index, target_node_index, match):
        self.father_node = father_node
        self.target_node = target_node
        # where the key is or was expected to be
        self.target_key_index = target_key_index
        # the child index in the father father_node that refers to the father_node where the key is or was expected to be
        self.child_index = target_node_index
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

    def to_string(self):
        print(self.root)


# manual testing

def manual_test():
    tree = TTFTree()

    while True:
        print("Para sair digite 'e'")
        user_input = input("Para adicionar um valor na árvore: ")
        if user_input == 'e':
            break
        to_insert = int(user_input)
        tree.insert(to_insert)
        tree.to_string()


# pre-built test 1

def pre_built_test_one():
    tree = TTFTree()
    for i in range(0, 1000):
        tree.insert(i)
        tree.to_string()


# pre-built test 2

def pre_built_test_two():
    tree = TTFTree()
    for i in range(-20, 25):
        tree.insert(i)
        tree.to_string()


def main():
    print("Qual dos testes voce gostaria de fazer?")
    print("[1] - Teste manual")
    print("[2] - Teste pronto, inserindo valores na árvore no intervalo de [0, 999]")
    print("[3] - Teste pronto, inserindo valores na árvore no intervalo de [-20, 25]")
    print("Digite qualquer outro valor para sair...")

    choice = input("Sua escolha: ")

    if choice == 1:
        manual_test()
    elif choice == 2:
        pre_built_test_one()
    elif choice == 2:
        pre_built_test_two()
    else:
        print("Até mais!")


if __name__ == '__main__':
    main()
