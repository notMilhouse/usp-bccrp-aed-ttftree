import snoop
import copy


class TTFTreeNode:
    def __init__(self, isLeaf, treeDegree):
        self.keys = []
        self.numKeys = 0
        self.maxKeys = 2 * treeDegree - 1

        self.children = []
        self.numChildren = 0
        self.maxChildren = 2 * treeDegree

        self.isLeaf = isLeaf

    def insertKey(self, key, index):
        self.keys.insert(index, key)
        self.keys.sort()
        self.numKeys += 1

    def updateKey(self, key, index):
        self.keys[index] = key

    def removeKey(self, key):
        removed = self.keys.remove(key)
        self.numKeys -= 1

        return removed

    def hasKey(self, key):
        return key in self.keys

    def insertChild(self, child, index):
        self.children.insert(index, child)
        self.numChildren += 1

    def updateChild(self, child, index):
        self.children[index] = child

    def removeChild(self, child):
        removed = self.children.remove(child)
        self.numChildren -= 1

        return removed

    def __str__(self, level=0):
        ret = "nivel da arvore " + str(level) + ": " + " \t" * level
        for key in self.keys:
            ret += str(key) + " "
        ret += "\n"
        for child in self.children:
            ret += child.__str__(level + 1)
        return ret


class TTFTreeSearchResult:
    def __init__(self, node: TTFTreeNode, childNode: TTFTreeNode, keyIndex, childNodeIndex, match: bool):
        self.node = node
        self.childNode = childNode
        self.keyIndex = keyIndex
        self.childNodeIndex = childNodeIndex
        self.match = match

    def toString(self):
        print("Indice: {}\nMatch: {}".format(self.index, self.match))


class TTFTree:
    def _newTreeNode(self, isLeaf):
        return TTFTreeNode(isLeaf, self.degree)

    def __init__(self):
        self.degree = 2
        self.root = self._newTreeNode(True)

    def find(self, key):
        return self._find(None, self.root, 0, key)

    def _find(self, node, childNode, pathChoice, key):
        index = 0

        while (index < childNode.num_keys and key > childNode.keys[index]):
            index = index + 1

        if (index < childNode.num_keys and key == childNode.keys[index]):
            return TTFTreeSearchResult(node, childNode, index, pathChoice, True)
        elif (childNode.isLeaf == True):
            return TTFTreeSearchResult(node, childNode, index, pathChoice, False)
        else:
            return self._find(childNode, childNode.children[index], index, key)

    def insert(self, key):
        keySearchResult = self.find(key)

        if (keySearchResult.match):
            print("nicolas cagezinho ele")
            pass

        else:
            keySearchResult.childNode.insertKey(key, keySearchResult.keyIndex)

            shouldSplit = keySearchResult.childNode.maxKeys < keySearchResult.childNode.numKeys or keySearchResult.childNode.maxChildren < keySearchResult.childNode.numChildren
            if (shouldSplit):
                self._split(keySearchResult)

    def _split(self, nodeReference):

        targetNode = nodeReference.target_node
        fatherNode = nodeReference.father_node

        if (targetNode == self.root):
            newLeftChild = self._newTreeNode(targetNode.isLeaf)
            newRightChild = self._newTreeNode(targetNode.isLeaf)

            for key in targetNode.keys:
                if (key < targetNode.keys[2]):
                    newLeftChild.insertKey(key, 3)
                elif (key > targetNode.keys[2]):
                    newRightChild.insertKey(key, 3)

            targetNode.removeKey(targetNode.keys[0])
            targetNode.removeKey(targetNode.keys[0])
            targetNode.removeKey(targetNode.keys[1])

            targetNode.insertChild(newLeftChild, 0)
            targetNode.insertChild(newRightChild, 1)

            targetNode.isLeaf = False

        else:
            fatherNode.insertKey(targetNode.keys[2], nodeReference.target_key_index)

            newNode = self._newTreeNode(targetNode.isLeaf)
            fatherNode.insertChild(newNode, nodeReference.childNodeIndex + 1)

            for index, key in enumerate(targetNode.keys):
                if (key > targetNode.keys[2]):
                    newNode.insertKey(key, nodeReference.target_key_index)

            if (not targetNode.isLeaf):
                for index, key in enumerate(targetNode.keys):
                    if (key > targetNode.keys[2]):
                        newNode.insertChild(targetNode.children[index], index)
                lastChild = len(targetNode.children) - 1
                newNode.insertChild(targetNode.children[lastChild], 4)

            targetNode.removeKey(targetNode.keys[2])
            targetNode.removeKey(targetNode.keys[2])

            if (targetNode.isLeaf == False):
                targetNode.removeChild(targetNode.children[3])
                targetNode.removeChild(targetNode.children[3])

            fatherShouldSplit = fatherNode.maxKeys < fatherNode.num_keys or fatherNode.maxChildren < fatherNode.numChildren
            if (fatherShouldSplit):
                self._splitFather(fatherNode)

    def _splitFather(self, node):
        insertedKey = node.keys[2]

        if (node != self.root):
            reference = self.find(insertedKey)
            self._split(reference)
            return None

        newLeftChild = self._newTreeNode(False)
        newRightChild = self._newTreeNode(False)

        for index, key in enumerate(node.keys):
            if (key < insertedKey):
                newLeftChild.insertKey(key, index)
                newLeftChild.insertChild(node.children[index], index)
            elif (key > insertedKey):
                newRightChild.insertKey(key, index)
                newRightChild.insertChild(node.children[index], index)
        newLeftChild.insertChild(node.children[2], 4)
        lastChild = len(node.children) - 1
        newRightChild.insertChild(node.children[lastChild], 3)

        node.removeKey(node.keys[0])
        node.removeKey(node.keys[0])
        node.removeKey(node.keys[1])

        node.children = [newLeftChild, newRightChild]
        node.numChildren = 2

    def toString(self):
        print(self.root)


def main():
    tree = TTFTree()
    for i in range(0, 1000):
        tree.insert(i)
        tree.toString()


if __name__ == '__main__':
    main()