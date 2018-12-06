class Tree(object):

    def __init__(self, attribute=None, value=None):
        self.attribute = attribute
        self.value = value
        self.parent = None
        self.children = []

    def __contains__(self, other):
        for child in self.getChildren():
            if child == other:
                return True
        return False

    def __repr__(self):
        return str(self.attribute)+":"+str(self.value)

    def __eq__(self, other):
        assert isinstance(other, Tree), "Can only compare with objects of same type"
        if other.attribute == self.attribute:
            return True
        return False

    def __hash__(self):
        return hash(str(self.attribute) + str(self.value))

    def hasChild(self):
        if self.children:
            return True
        return False

    def isLeafNode(self):
        if not self.children:
            return True
        return False

    def addChild(self, child):
        assert isinstance(child, Tree), "Child should be of type %r" % type(self)
        child.parent = self
        self.children.append(child)
        return self.children[-1]

    def getChildren(self):
        return self.children

    def getChild(self, childIndex):
        return self.children[childIndex]

    def addChildren(self, children):
        assert isinstance(children, list), \
        "Children should be of type list found %r" % type(children)
        assert all(isinstance(child, Tree) for child in children), \
        "Children should be a list of Tree, found a list of %r" %type(children[0])
        for child in children:
            child.parent = self
        self.children.extend(children)

    def childIndex(self, child):
        for idx, chi in enumerate(self.children):
            if chi == child:
                return idx
        return -1

    def getAllNodes(self, aslink=False):
        assert self.isSinglePath(), "Works only for single path trees"
        tree = self
        nodes = []
        while not tree.isLeafNode():
            if tree.attribute is not None:
                if aslink:
                    nodes.append(tree)
                else:
                    nodes.append(tree.attribute)
            tree = tree.children[0]
        if aslink:
            nodes.append(tree)
        else:
            nodes.append((tree.attribute, tree.value))
        return nodes

    def getAllNodeValues(self):
        assert self.isSinglePath(), "Works only for single path trees"
        tree = self
        nodes = []
        while not tree.isLeafNode():
            if tree.attribute is not None:
                nodes.append(tree.attribute)
            tree = tree.children[0]
        nodes.append(tree.attribute)
        return nodes


    def isSinglePath(self):
        if self.isLeafNode():
            return True
        if len(self.children) > 1:
            return False
        return self.children[0].isSinglePath()

    # def mergeTree(self, tree, header_table=None,recur=False):
    #     if self == tree:
    #         for child in tree.children:
    #             if child in self:
    #                 id = self.childIndex(child)
    #                 self_child = self.getChild(id)
    #                 if header_table is not None:
    #                     if child.item not in header_table:
    #                         header_table[child.item] = Node(child, None)
    #                     # else:
    #                     #     header_table[child.item].modify(Node(self_child,None),child)
    #                 self_child.support += 1
    #                 self_child.mergeTree(child,header_table,recur=True)
    #             else:
    #                 if header_table is not None:
    #                     node = tree
    #                     nodes = tree.getAllNodes(aslink=True)
    #                     if recur:
    #                         nodes.pop(0)
    #                     for node in nodes:
    #                         if node.item not in header_table:
    #                             header_table[node.item] = Node(node, None)
    #                         else:
    #                             header_table[node.item].append(Node(node,None))
    #                 self.addChild(child)
