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
        removed = self.children.remove(children)
        self.numChildren -= 1

        return removed
    
    def __str__(self, level=0):
        ret = "nivel da arvore " + str(level) + ": " + " \t"*level
        for key in self.keys:
            ret += str(key) + " "
        ret += "\n"
        for child in self.children:
            ret += child.__str__(level + 1)
        return ret


class TTFTreeSearchResult:
    def __init__(self, node : TTFTreeNode, childNode : TTFTreeNode, keyIndex, childNodeIndex, match : bool):
        self.node = node
        self.index = index
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
        return self._find(None, self.root, key)

    def _find(self, node, childNode, key):
        index = 0
        
        while (index < childNode.numKeys and key > childNode.keys[index]):
            index = index + 1
            
        
        if (index < childNode.numKeys and key == childNode.keys[index]):
            return TTFTreeSearchResult(node, childNode, index, index, True)
        elif (childNode.isLeaf == True):
            return TTFTreeSearchResult(node, childNode, index, index, False)
        else:
            return self._find(childNode, childNode.children[index], key)
    

    def insert(self, key):
        keySearchResult = self.find(key)
        print(keySearchResult.toString())

        if(keySearchResult.match):
            print("nicolas cagezinho ele")
            pass
        
        else:
            keySearchResult.node.insertKey(key, keySearchResult.index)

            shouldSplit = keySearchResult.node.maxKeys < keySearchResult.node.numKeys or keySearchResult.node.maxChildren < keySearchResult.node.numChildren
            if(shouldSplit):
                self._split(keySearchResult)

    def _split(self, nodeReference):
        #subtree root
        """ if(node == self.root)
            newRoot = self._newTreeNode(False)
        else:
            newRoot =  """
        if(nodeReference.node == self.root):


        else:

        newLeftChild = self._newTreeNode(node.isLeaf)
        newRightChild = self._newTreeNode(node.isLeaf)

        for key in node.keys:
            if(key < node.keys[2]):
                newLeftChild.insertKey(key, 3)
            elif(key > node.keys[2]):
                newRightChild.insertKey(key, 3)

        node.removeKey(node.keys[0])
        node.removeKey(node.keys[0])
        node.removeKey(node.keys[1])

        node.insertChild(newLeftChild, 0)
        node.insertChild(newRightChild, 1)

        node.isLeaf = False


    def toString(self):
        print(self.root)

def main():
    tree = TTFTree()
    while(1):
        toInsert = int(input("Insira o valor: "))
        tree.insert(toInsert)
        tree.toString()


if __name__ == '__main__':
    main()