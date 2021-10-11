import snoop
import copy

class TTFTreeNode:
    def __init__(self, isLeaf, treeDegree):
        self.keys = [None]
        self.numKeys = 0
        self.maxKeys = 2 * treeDegree - 1

        self.children = [None]
        self.numChildren = 0
        self.maxChildren = 2 * treeDegree

        self.isLeaf = isLeaf

    
    def insertKey(self, key, index):
        self.keys.insert(index, key)
    
    def removeKey(self, key):
        removed = self.keys.remove(key)

        return removed

    def hasKey(self, key):
        return key in self.keys   
    @snoop
    def insertChild(self, children, index):
        self.children.insert(index, children)
    
    def removeChild(self, children):
        removed = self.children.remove(children)

        return removed
    
    def __str__(self, level=0):
        ret = "nivel da arvore " + str(level) + ": " + " \t"*level
        for key in self.keys[1:]:
            ret += str(key) + " "
        ret += "\n"
        for child in self.children[1:]:
            ret += child.__str__(level + 1)
        return ret


class TTFTreeSearchResult:
    def __init__(self, node : TTFTreeNode, index, match : bool):
        self.node = node
        self.index = index
        self.match = match

class TTFTree:
    def _newTreeNode(self, isLeaf):
        return TTFTreeNode(isLeaf, self.degree)

    def __init__(self):
        self.degree = 2
        self.root = self._newTreeNode(True)
    
    def find(self, key):
        return self._find(self.root, key)

    def _find(self, node, key):
        index = 1
        
        while (index <= node.numKeys and key > node.keys[index]):
            index = index + 1
            
        
        if (index <= node.numKeys and key == node.keys[index]):
            return TTFTreeSearchResult(node, index, True)
        elif (node.isLeaf == True):
            return TTFTreeSearchResult(node, index, False)
        else:
            return self._find(node.children[index], key)
    @snoop
    def _split(self, node, childNode, i):
        newChild = self._newTreeNode(childNode.isLeaf)
        newChild.numKeys = self.degree - 1

        self.toString()
        print("split")

        for j in range(1, self.degree - 1):
            keyToTransfer = childNode.keys[j + self.degree]
            newChild.insertKey(keyToTransfer, j)
        
        if (childNode.isLeaf == False):
            for j in range(1, self.degree):
                childToTransfer = childNode.children[j + self.degree]
                newChild.insertChild(childToTransfer, j)

        print("numero de chaves do filho", childNode.numKeys)
        childNode.numKeys = self.degree - 1
        print("numero de chaves do filho", childNode.numKeys)
        for j in range(node.numKeys + 1, i + 1, -1):
            childToTransfer = node.children[j]
            node.insertChild(childToTransfer, j + 1)
        
        node.insertChild(newChild, i + 1)

        for j in range(node.numKeys, i, -1):
            node.insertKey(node.keys[j], j + 1)   
        
        node.insertKey(childNode.keys[self.degree + 1], i)
        node.numKeys = node.numKeys + 1

        self.toString()

    def _insertNonFull(self, node, key):
        self.toString()
        print("non full")
        i = node.numKeys
        if(node.isLeaf == True):
            while(i >= 1 and key < node.keys[i]):
                node.insertKey(node.keys[i], i + 1)
                
                i = i - 1
            
            node.insertKey(key, i + 1)
            node.numKeys = node.numKeys + 1
        else:
            while(i >= 1 and key < node.keys[i]):
                i = i - 1
            i = i + 1

            if(node.children[i].numKeys == node.maxKeys):
                self._split(node, node.children[i], i)
                if(key > node.keys[i]):
                    i = i + 1
            self._insertNonFull(node.children[i], key)

        self.toString()

    @snoop
    def _insert(self, key):
        self.toString()
        print("insert normal")
        r = self.root
        if(r.numKeys == r.maxKeys):
            newNode = self._newTreeNode(False)
            self.root = newNode
            newNode.numKeys = 0
            newNode.insertChild(r, 1)


            self._split(newNode, newNode.children[1], 1)
            self._insertNonFull(newNode, key)
        else:
            self._insertNonFull(r, key)

        self.toString()



    def insertKey(self, key):
        keySearchResult = self.find(key)

        if(keySearchResult.match):
            print("nicolas cagezinho ele")
            pass
        
        else:
            self._insert(key)

    def toString(self):
        print(self.root)

def main():
    tree = TTFTree()
    while(1):
        toInsert = input("Insira o valor: ")
        tree.insertKey(toInsert)
        tree.toString()


if __name__ == '__main__':
    main()