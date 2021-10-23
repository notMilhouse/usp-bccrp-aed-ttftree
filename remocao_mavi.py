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
        
        # search starts on the root, which is the childNode
        while (index < childNode.numKeys and key > childNode.keys[index]):
            index = index + 1
            
        # index goes from 0 to childNode.numkeys -1
        # if found. pathChoice is the index of the childNode, in the array children, in which the key was found
        if (index < childNode.numKeys and key == childNode.keys[index]):
            return TTFTreeSearchResult(node, childNode, index, pathChoice, True)
        # not found. the node in which we made the search is a leaf, therefore there is no other node to search into
        elif (childNode.isLeaf == True):
            return TTFTreeSearchResult(node, childNode, index, pathChoice, False)
        # not found. the node is not a leaf, search in its child, using index to search in the appropriate child
        else:
            return self._find(childNode, childNode.children[index], index, key)
    

    def insert(self, key):
        keySearchResult = self.find(key)

        if(keySearchResult.match):
            print("nicolas cagezinho ele")
            pass

        else:
            keySearchResult.childNode.insertKey(key, keySearchResult.keyIndex)

            shouldSplit = keySearchResult.childNode.maxKeys < keySearchResult.childNode.numKeys or keySearchResult.childNode.maxChildren < keySearchResult.childNode.numChildren
            if(shouldSplit):
                self._split(keySearchResult)

    def _split(self, nodeReference):

        targetNode = nodeReference.childNode
        fatherNode = nodeReference.node

        if(targetNode == self.root):
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
            fatherNode.insertKey(targetNode.keys[2], nodeReference.keyIndex)

            newNode = self._newTreeNode(targetNode.isLeaf)
            fatherNode.insertChild(newNode, nodeReference.childNodeIndex + 1)

            for index, key in enumerate(targetNode.keys):
                if (key > targetNode.keys[2]):
                    newNode.insertKey(key, nodeReference.keyIndex)

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

            fatherShouldSplit = fatherNode.maxKeys < fatherNode.numKeys or fatherNode.maxChildren < fatherNode.numChildren
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

    def remove(self,key):

        print('REMOVE, key = ',key)

        searchResult = self.find(key)

        if(searchResult.match):

            # imprimir o noh e seus elementos
            if(searchResult.node != None):
                print('search result: node -> ',searchResult.node.keys,'childNode -> ',searchResult.childNode.keys)
            else:
                print('search result: childNode -> ',searchResult.childNode.keys)

            # remover de folha
            if(searchResult.childNode.isLeaf):
                self.removeFromLeaf(searchResult) 

            # remover de raiz
            elif(searchResult.childNode == self.root):
                self.removeFromRoot(searchResult) 

            # remover do meio da arvore
            else:
                self.removeFromMiddle(searchResult)  #TODO FAZER ESSA FUNCAO
        else:
            print('Chave nao existe na arvore')

    def removeFromLeaf(self,searchResult : TTFTreeSearchResult):

        print('REMOVE FROM LEAF')

        # imprimir os elementos do noh 
        if(searchResult.node != None):
            print('search result: node -> ',searchResult.node.keys,'childNode -> ',searchResult.childNode.keys)
        else:
             print('search result: childNode -> ',searchResult.childNode.keys)

        if(searchResult.childNode.numKeys -1 >=1): # ainda consistente apos a remocao de 1 elemento
            keyToRemove = searchResult.childNode.keys[searchResult.keyIndex]
            searchResult.childNode.removeKey(keyToRemove)
            
        elif(searchResult.childNode.numKeys -1 == 0): # pai empresta chave, etc, slide 24
        
            self.transferKey(searchResult)  

    def removeFromRoot(self,searchResult : TTFTreeSearchResult):
        print('REMOVE FROM ROOT')

        # imprimir no

        if(searchResult.node != None):
            print('search result: node -> ',searchResult.node.keys,'childNode -> ',searchResult.childNode.keys)
        else:
             print('search result: childNode -> ',searchResult.childNode.keys)

        rootKey = searchResult.childNode.keys[searchResult.keyIndex]
        searchResult.childNode.removeKey(rootKey) # remove chave do root 
        
        #slide 40, de exemplo nos comentarios

        # root recebe chave do ultimo filho de seu filho -> QUAL FILHO??? acho que tem que ser o da esquerda mesmo, se nao a arvore fica desbalanceada, se pegar da direita, ainda que o menor, ja desbalancearia a arvore
        nodeWithChildDonator = searchResult.childNode.children[0] # acha o no pai do filho desejado (primeiro, c as menores chaves) 
        # [15 25]
        childDonator = nodeWithChildDonator.children[nodeWithChildDonator.numChildren-1] # achar no filho que doa chave 
        # [30]
        keyToTranfer = childDonator.keys[childDonator.numKeys -1] # pega a chave que vai transferir 
        # keyToTranfer = 30
        childDonator.removeKey(keyToTranfer) # remover a chave que será transferida
        searchResult.childNode.insertKey(keyToTranfer,4) # inserir a chave no nó avô  !!!
        if(childDonator.numKeys == 0): # se o no ficar vazio depois de doar chave, apagar ele
            nodeWithChildDonator.removeChild(nodeWithChildDonator.children[nodeWithChildDonator.numChildren-1])
        """

        de uma versao anterior

        infoToTranfer = TTFTreeSearchResult(nodeWithChildDonator, childDonator,nodeWithChildDonator.numKeys -1,0,True)
        infoToTranfer.node = nodeWithChildDonator
        infoToTranfer.childNode = childDonator
        infoToTranfer.childNodeIndex = 0
        infoToTranfer.keyIndex = nodeWithChildDonator.numKeys -1
        infoToTranfer.match = True
        # newSearchResult = self.find(nodeWithChildDonator.keys[nodeWithChildDonator.numKeys-1]) 
        self.transferKey(infoToTranfer)
        """
    
    def removeFromMiddle(self,searchResult : TTFTreeSearchResult): # nos slides ta sempre removendo de folha ou raiz
        print('REMOVE FROM MIDDLE')

        # imprimir no

        if(searchResult.node != None):
            print('search result: node -> ',searchResult.node.keys,'childNode -> ',searchResult.childNode.keys)
        else:
             print('search result: childNode -> ',searchResult.childNode.keys)

        # remove chave e o noh ainda fica balanceado: 1 key 2 children, 2 keys  3 children, 3 keys  4 children -> children - key =1
        if(searchResult.childNode.numChildren - searchResult.childNode.numKeys -1 == 1):
            print('remove e permanece balanceado')
            keyToRemove = searchResult.childNode.keys[searchResult.keyIndex]
            print('key to remove: ',keyToRemove)
            searchResult.childNode.removeKey(keyToRemove)
        
        # remove e o noh fica desbalanceado: fundir os nos filhos
        elif(searchResult.childNode.numChildren - searchResult.childNode.numKeys -1 != 1):
            keyToRemove = searchResult.childNode.keys[searchResult.keyIndex]
            searchResult.childNode.removeKey(keyToRemove)
            print('key to remove: ',keyToRemove)
            print('remove e e precisa fundir nos filhos')
            self.merge(searchResult)

        # remove chave e o noh fica vazio: slide 35 kind of thing, pega do pai, propaga, etc
        if(searchResult.childNode.numKeys-1 == 0):
            keyToRemove = searchResult.childNode.keys[searchResult.keyIndex]
            searchResult.childNode.removeKey(keyToRemove)
            print('key to remove: ',keyToRemove)
            print('remove e e precisa de node transferir para childNode')
            self.transferKeyToChild(searchResult) # node vai dar 1 chave pro childNode




    def transferKey(self,searchResult : TTFTreeSearchResult):
        print('TRANSFER KEY')

        #imprimir noh
        if(searchResult.node != None):
            print('search result: node -> ',searchResult.node.keys)
        if (searchResult.childNode != None):
            print('childNode -> ',searchResult.childNode.keys)

        # obter no pai de node antes de um possivel merge 
        newSearchResult = self.find(searchResult.node.keys[searchResult.node.numKeys-1])

        # imprimir resultado para verificar se makes sense
        if(newSearchResult.node != None):
            print('new search result: node -> ',newSearchResult.node.keys)
        if (newSearchResult.childNode != None):
            print('childNode -> ',newSearchResult.childNode.keys)
       
       # a operacao mesmo comeca aqui:

        # remover chave do childNode
        keyToRemove = searchResult.childNode.keys[searchResult.keyIndex]
        searchResult.childNode.removeKey(keyToRemove)
        
        # pegar chave do pai, transferir, apagar do pai -> slide 32
        keyToTranfer = searchResult.node.keys[searchResult.node.numKeys-1]
        searchResult.childNode.insertKey(keyToTranfer,4) # inserir no filho
        searchResult.node.removeKey(keyToTranfer) # remover do pai
        

        # verificar consistencia:

        # do no irmao -> pensar melhor nisso, realmente necessario? ou viajei? nao lembro de ter isso no slide

        # do no pai: node 

        if(searchResult.node.numKeys  == 0): # slide 35
            # envolver o pai de node nessa situação, por isso a importancia de newSearchResult
            # fazer o merge dos filhos de node: slide 35
            self.merge(searchResult)
            # transferir do pai de node pra ele: slide 36
            self.transferKeyToChild(newSearchResult) # propagacao de underflow  -> a ideia de automatizar isso aqui, acho que ta funcionando 

        elif(searchResult.node.numChildren - searchResult.node.numKeys != 1): # se ficar com qnt de filhos incoerente ah qnt de chaves
            self.merge(searchResult) # fundir os filhos de node, childNodeIndex e childNodeIndex+1

    def transferKeyToChild(self, searchResult):

        print('TRANSFER KEY TO CHILD')
        # obter no pai de node antes de um possivel merge 
        newSearchResult = self.find(searchResult.node.keys[searchResult.node.numKeys-1])

        # printar resultado
        if(newSearchResult.node != None):
            print('new search result: node -> ',newSearchResult.node.keys)
        if (newSearchResult.childNode != None):
            print('childNode -> ',newSearchResult.childNode.keys)


        # pegar chave do pai, transferir, apagar do pai -> slide 32
        keyToTranfer = searchResult.node.keys[searchResult.node.numKeys-1]
        searchResult.childNode.insertKey(keyToTranfer,4) # inserir no filho
        searchResult.node.removeKey(keyToTranfer) # remover do pai

        if(searchResult.node.numKeys  == 0): # slide 35
            # envolver o pai de node nessa situação
            # fazer o merge dos filhos de node: slide 35
            self.merge(searchResult)
            # transferir do pai de node pra ele: slide 36
            if(newSearchResult.childNode != self.root):
                self.transferKeyToChild(newSearchResult) # propagacao de underflow 
            # com excessao desse else, as duas funcoes de transferKey estao MT PARECIDAS, buscar uma forma de fazer soh 1
            else:
                # root recebe chave do ultimo filho de seu filho -> QUAL FILHO??? acho que tem que ser o da esquerda mesmo, se nao a arvore fica desbalanceada, se pegar da direita, ainda que o menor, ja desbalancearia a arvore
                print('node: ',searchResult.node.keys,' , child eh: ', searchResult.childNode.keys)
                nodeWithChildDonator = searchResult.node.children[0] # acha o no pai do filho desejado (primeiro, c as menores chaves) 
                print('nodeWithChildDonator: ',nodeWithChildDonator.keys)
                childDonator = nodeWithChildDonator.children[nodeWithChildDonator.numChildren-2] # achar no filho que doa chave
                print('childDonator: ',childDonator.keys) 
                keyToTranfer = childDonator.keys[childDonator.numKeys -1] # pega a chave que vai transferir 
                childDonator.removeKey(keyToTranfer) # remover a chave que será transferida
                if(childDonator.numKeys == 0 and childDonator.isLeaf): # folha sem chave -> apagar
                    nodeWithChildDonator.removeChild(nodeWithChildDonator.children[nodeWithChildDonator.numChildren-2])
                searchResult.node.insertKey(keyToTranfer,4) # inserir a chave no nó avô 
                if(childDonator.numKeys == 0): # se o no ficar vazio depois de doar chave, apagar ele
                    nodeWithChildDonator.removeChild(nodeWithChildDonator.children[nodeWithChildDonator.numChildren-1])

        elif(searchResult.node.numChildren - searchResult.node.numKeys != 1): # se ficar com qnt de filhos incoerente ah qnt de chaves
            self.merge(searchResult) # fundir os filhos de node, childNodeIndex e childNodeIndex+1


    def merge(self, searchResult : TTFTreeSearchResult):

        print('MERGE')

        # imprimir noh

        if(searchResult.node != None):
            print('search result: node -> ',searchResult.node.keys)
        if (searchResult.childNode != None):
            print('childNode -> ',searchResult.childNode.keys)
        

        nodeIndex = searchResult.childNodeIndex
        node1 = searchResult.node.children[nodeIndex-1]
        print('node1 = ',node1.keys)
        node2 = searchResult.node.children[nodeIndex]
        print('node2 = ',node2.keys)

        if node1.isLeaf: # slide 32  transferir as chaves


            for key in node2.keys: # transferir chaves de um nó para o outro
                node1.insertKey(key,4)
            
            searchResult.node.removeChild(searchResult.node.children[nodeIndex])

        else:
            for key in node2.keys: # transferir chaves de um nó para o outro
                node1.insertKey(key,4)
            
            for child in node2.children: # transferir filhos
                node1.insertChild(child,4)
            
        print('ao final -> node1 = ',node1.keys)
        print('node2 = ',node2.keys)

    def toString(self):
        print(self.root)

def main():
    tree = TTFTree()
    
    tree.insert(35)
    tree.insert(10)
    tree.insert(50)
    tree.insert(25)
    tree.insert(5)
    tree.insert(15)
    tree.insert(18)
    tree.insert(20)
    tree.insert(30)
    tree.insert(40)
    tree.insert(45)
    tree.insert(55)
    tree.toString()

    
    #remove from root ta ok, acho
    """
    tree.remove(35)
    tree.toString()
    tree.remove(30)
    tree.toString()
    tree.remove(20)
    tree.toString()
    """
    
    tree.remove(55)
    tree.toString()
    tree.remove(20) # remove from leaf -> ok
    tree.toString()
    tree.remove(25) # remove from middle -> virou uma zona
    tree.toString()
    tree.remove(40)
    tree.toString()
    tree.remove(45)
    tree.toString()
    tree.remove(50)
    tree.toString()
    
    
# de folha com keys sobrando -> deu certo
    

if __name__ == '__main__':
    main()