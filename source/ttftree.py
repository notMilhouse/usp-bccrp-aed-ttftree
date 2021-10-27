class TTFTreeNode:
    max_keys = 3
    max_children = 4

    def __init__(self, is_leaf):
        self.keys = []
        self.children = []
        self.is_leaf = is_leaf

    def num_keys(self):
        return len(self.keys)

    def num_children(self):
        return len(self.children)

    def is_last_child(self, child):
        return child == self.children[-1]

    def get_last_key(self):
        return self.keys[-1]

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

    def __str__(self, level=0):
        content = "nivel {}: ".format(level) + "\t" * level
        for key in self.keys:
            content += str(key) + " "
        content += "\n"
        for child in self.children:
            content += child.__str__(level + 1)
        return content

    def should_split(self):
        reached_max_keys = TTFTreeNode.max_keys < self.num_keys()
        reached_max_children = TTFTreeNode.max_children < self.num_children()
        should_split = reached_max_keys or reached_max_children
        return should_split


# the target node may be the node where the key was found, or the node where the key was expected to be
class TTFTreeSearchResult:
    def __init__(self, father_node: TTFTreeNode, target_node: TTFTreeNode, target_key_index, target_node_index, match):
        self.father_node = father_node
        self.target_node = target_node
        self.target_key_index = target_key_index
        self.target_node_index = target_node_index
        self.match = match

    def to_string(self):
        print("Indice: {}\nMatch: {}".format(self.target_key_index, self.match))


class TTFTreeSearchStackTrace:
    def __init__(self, trace_list=None):
        if trace_list is None:
            trace_list = []
        self.log = trace_list

    def add_log(self, search_result):
        self.log.append(search_result)

    def get_last(self):
        return self.log[-1]

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

    def _find(self, node, child_node, path_choice, key, trace_find: TTFTreeSearchStackTrace):
        index = 0

        while index < child_node.num_keys() and key > child_node.keys[index]:
            index = index + 1

        if index < child_node.num_keys() and key == child_node.keys[index]:
            trace_find.add_log(TTFTreeSearchResult(node, child_node, index, path_choice, True))
            return trace_find
        elif child_node.is_leaf:
            trace_find.add_log(TTFTreeSearchResult(node, child_node, index, path_choice, False))
            return trace_find
        else:
            trace_find.add_log(TTFTreeSearchResult(node, child_node, index, path_choice, False))
            return self._find(child_node, child_node.children[index], index, key, trace_find)

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

            subtree_root_node.insert_child(node_reference.target_node, node_reference.target_node_index)

            self.root = subtree_root_node

        else:
            subtree_root_node = node_reference.father_node
            new_sibling_node = TTFTreeNode(node_reference.target_node.is_leaf)

        subtree_root_node.insert_child(new_sibling_node, node_reference.target_node_index + 1)

        median_key = node_reference.target_node.keys[2]
        subtree_root_node.insert_key(median_key, node_reference.target_node_index)
        # target_node_index because it is from where the key came

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
