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


class TTFTreeSearchResult:
    def __init__(self, father_node: TTFTreeNode, target_node: TTFTreeNode, target_key_index, target_node_index, match):
        self.father_node = father_node
        self.target_node = target_node
        self.target_key_index = target_key_index
        self.target_node_index = target_node_index
        self.match = match

    def to_string(self):
        print("Indice: {}\nMatch: {}".format(self.target_key_index, self.match))


class TTFTree:

    def __init__(self):
        self.root = TTFTreeNode(True)

    def find(self, key):
        return self._find(None, self.root, 0, key)

    def _find(self, node, child_node, path_choice, key):
        index = 0

        while index < child_node.num_keys() and key > child_node.keys[index]:
            index = index + 1

        if index < child_node.num_keys() and key == child_node.keys[index]:
            return TTFTreeSearchResult(node, child_node, index, path_choice, True)
        elif child_node.is_leaf:
            return TTFTreeSearchResult(node, child_node, index, path_choice, False)
        else:
            return self._find(child_node, child_node.children[index], index, key)

    def insert(self, key):
        key_search_result = self.find(key)

        if key_search_result.match:
            print("Valor ja existe na arvore...")

        else:
            key_search_result.target_node.insert_key(key, key_search_result.target_key_index)

            should_split = key_search_result.target_node.should_split()

            if should_split:
                self._split(key_search_result)

    def _split(self, node_reference: TTFTreeSearchResult):
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
        subtree_root_node.insert_key(median_key, node_reference.target_key_index)

        for key in node_reference.target_node.keys:
            if key > median_key:
                new_sibling_node.insert_key(key, 3)

        if not node_reference.target_node.is_leaf:
            for index in range(0, node_reference.target_node.num_keys()):
                if node_reference.target_node.keys[index] > median_key:
                    new_sibling_node.insert_child(node_reference.target_node.children[index], index)
            new_sibling_node.insert_child(node_reference.target_node.children[4], index)
            node_reference.target_node.remove_child(node_reference.target_node.children[3])
            node_reference.target_node.remove_child(node_reference.target_node.children[3])

        node_reference.target_node.remove_key(node_reference.target_node.keys[2])
        node_reference.target_node.remove_key(node_reference.target_node.keys[2])

        if node_reference.father_node is not None:
            should_split_father = node_reference.father_node.should_split()

            if should_split_father:
                new_reference = self.find(median_key)
                self._split(new_reference)

    def to_string(self):
        print(self.root)

def main():
    tree = TTFTree()
    while(1):
        toInsert = int(input("Insira o valor: "))
        tree.insert(toInsert)
        tree.to_string()

#TODO find a way to get rid of the find function to split father node, bc that's quite inefficient


if __name__ == '__main__':
    main()
