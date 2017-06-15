from queue import Queue
from storage.DummyNode import DummyNode
from storage.DummyRelationship import DummyRelationship
from storage.LabelIndex import LabelIndex

def findBestElement(nodes, relationships):
    # For now, this function chooses the dummy node or dummy relationship with
    # the most labels 
    # Later, it'll use heuristics to choose
    # the "most specific" node to start a query with to minimize time the
    # storage-layer search takes.
    return (nodes[0], 0)

""" This function should find the real nodes which match up with the given dummy
node. """
def locateNodes(dummyNode, nodeFile, relationshipFile, propFile, labelFile):
    # TODO: should this go in a different file?
    """ look at nodes in each label of category """
    numNodeLabels = {} # dictionary tracks number of labels a given node has
    numCategoryLabels = len(dummyNode.getLabels()) # get number of labels in this category

    for lbl in dummyNode.getLabels():
        # open label index
        lblIndex = LabelIndex(lbl)
        # add each node in index to dictionary, if not already there
        # increment label count for node
        lblNodes = lblIndex.getItems()
        for nodeID in lblNodes:
            if nodeID not in numNodeLabels:
                numNodeLabels[nodeID] = 1
            else:
                numNodeLabels[nodeID] += 1

    categoryNodes = [] # list of nodes to consider for this category
    for nodeID in numNodeLabels.keys():
        # node has all labels of category
        if numNodeLabels[nodeID] == numCategoryLabels:
            categoryNodes.append(nodeID)

    for nodeID in categoryNodes[:]:
        node = nodeFile.readNode(nodeID, relationshipFile, propFile, labelFile)
        nodeList.append(node)
        # dummyNode.getProperties() should return a list of key-value pairs (represented
        # as tuples) corresponding to the properties the dummyNode should have.
        for prop in dummyNode.getProperties():
            key = prop[0]
            value = prop[1]
            foundProperty = False
            for property in node.getProperties():
                if property.key == key and property.value == value:
                    foundProperty = True
                    break
            if foundProperty == False:
                categoryNodes.remove(nodeID)
                break
            
    return categoryNodes

""" This function should find the real relationships which match up with the given dummy
relationship. """
def locateRelationships(relationship):
    # Not yet implemented, should be very similar to locateNodes
    return False

def breadthFirstSearch_(nodes, relationships, nodeFile, relationshipFile,
                        propFile, labelFile):
    """Perform a breadth-first-search and return patterns satisfying the input.

    `nodes` should be a list of `DummyNode`s, and `relationships` should be
    a list of `DummyRelationship`s, such that the following pattern is to be
    matched:

    (node 1) -[relationship 1]-> (node 2) ... -[relationship n-1]-> (node n)

    Hence, len(nodes) must equal len(relationships) + 1.

    The return value is a set of tuples matching this description; that is,
    each tuple contains a `Node`, then a `Relationship`, then a `Node`, etc.
    All tuples, for now, must be of the same length, since we don't yet support
    arbitrary-length relationship distances.
    """
    # Figure out which node to start with in the pattern. This is a nontrivial
    # problem; logically, we should start with the most-specific node or
    # relationship, then work our way outwards from there. However, right now
    # we just naively choose the first node in the list. We need the index of
    # `start` into its parent list (nodes or relationships), too.
    (start, start_idx) = findBestElement(nodes, relationships)

    # The first step is to find `start` in the storage layer. Unfortunately,
    # without any sort of indexing, this is a long step, requiring a linear
    # search to find it. Not to mention the fact that there may be multiple
    # appropriate elements in the database!
    chainQueue = Queue() # TODO: enforce the max-size, since we know it?
    if isinstance(start, DummyRelationship):
        realStart = locateRelationships(start)
        [chainQueue.put((rel, start_idx)) for rel in realStart]
    elif isinstance(start, DummyNode):
        realStart = locateNodes(start, nodeFile, relationshipFile, propFile, labelFile) 
        [chainQueue.put(((node, start_idx))) for node in realStart]
    else:
        # TODO: Perhaps replace this with some sort of error reporting.
        return chainQueue

    # Now that we have our nodes/relationships to start with, we can start the
    # process of coming up with "chains". We introduce the term "chain" to mean
    # a tuple consisting of alternating `Node`s and `Relationship`s.
    # Unfortunately, we must also associated with each `Node`/`Relationship` its
    # index into the input `nodes` and `relationships` list. This is in order to
    # associate Elements with DummyElements. An example chain:
    #                   ((node1, 0), (rel1, 0), (node2, 1))
    # We will build up, starting with `start`, a Queue of these chains, until
    # all the chains match all the input criteria.
    goodChains = set([])
    while not chainQueue.empty():
        chain = chainQueue.get()

        # First, we'll try to extend the chain to the left. We don't, however,
        # need to do this if the first element in the chain is (node1, 0),
        # because then the chain starts with the right element.
        if not (isinstance(chain[0][0], Node) and chain[0][1] == 0):
            # The leftmost element is either a relationship or a node.
            if isinstance(chain[0][0], Node):
                # We'll extend the chain via all its possible relationships
                # that match with the input specifications.
                (currNode, currIdx) = chain[0]
                relationshipGoal = relationships[currIdx - 1] # -[rel (n-1)]-> (node n) ...
                rels = curr_node.getRelationships()
                goodRels = []
                for rel in rels:
                    # We only want relationships that match all specifications.
                    # TODO: fix the properties equality, if incorrect
                    if rel.getRelType() == relationshipGoal.label and rel.getProperties() == relationshipGoal.properties:
                       goodRels.append(rel)
                for goodRel in goodRels:
                    # Form a new chain. Tuple addition syntax is weird.
                    newChain = ((goodRel, currIdx - 1),) + chain
                    chainQueue.put(newChain)
            else: # Relationship
                # We'll extend the chain to the left via all the possible
                # nodes that can attach to that relationships that match
                # the input specifications.
                (currRel, currIdx) = chain[0]
                nodeGoal = nodes[currIdx] # node n -[rel n]-> ...
                otherNodeID = currRel.getOtherNodeID(chain[1][0].getID())
                otherNode = nodeFile.readNode(otherNodeID, relationshipFile,
                                              propFile, labelFile)
                if set(otherNode.getLabels()) == set(nodeGoal.labels) and \
                    otherNode.getProperties() == nodeGoal.properties:
                        # It's good!
                        newChain = ((otherNode, currIdx),) + chain
                        chainQueue.put(newChain)
        # OK, we didn't need to extend the chain to the left; how about the
        # right? We don't need to do this if the last element in the chain
        # is the last input node...
        elif not (isinstance(chain[-1][0], Node) and chain[-1][1] == len(nodes) - 1):
            pass
        # We didn't need to extend in either direction! Certainly this is a
        # chain worth returning.
        else:
            goodChains.add(chain)
    return goodChains

# root node is node to start search from
# conditions are query constraints to be applied at each level of search
# conditions is a list of tuples of the form
    # (relationship type, type of other node in relationship, node wanted)
    # node wanted = 0 for node closer to root, 1 for node further from root
# returns a queue of nodes that fit the conditions of the query
def breadthFirstSearch(rootNode, conditions, nodeFile, relationshipFile, propFile, labelFile):
    print("starting breadth first search with root node: {0}...".format(rootNode.getID()))

    # list of node ids that have already been visited in search
    visitedNodeIDs = []

    # queue will hold all nodes for a particular depth of search tree
    nodeQueue = Queue()
    # start with only root node in queue
    nodeQueue.put(rootNode)

    # for each condition
    for conditionTuple in conditions:
        relType = conditionTuple[0] # type of relationship wanted
        print("relationship type: {0}".format(relType))

        relEndNodeType = conditionTuple[1] # type of end node wanted
        print("relationship end node type: {0}".format(relEndNodeType))

        wantedNode = conditionTuple[2] # closer or further node wanted
        print("relationship end node wanted: {0}".format(wantedNode))

        # create a new queue to store nodes for this level
        nextNodeQueue = Queue()

        # while all nodes from previous level have not been considered
        while(not nodeQueue.empty()):
            node = nodeQueue.get()

            # add node to list of visited nodes
            visitedNodeIDs.append(node.getID())

            print("props of node in queue:")
            for prop in node.properties:
                print("key: {0}".format(prop.key))
                print("value: {0}".format(prop.value))

            rels = node.getRelationships()

            # check each relationship of node
            for rel in rels:
                # if relationship is of type necessary
                print("rel is of type: {0}".format(rel.getRelType()))
                print("rel type needed: {0}".format(relType))

                if rel.getRelType() == relType:
                    # select the other node in the relationship
                    otherNodeID = rel.getOtherNodeID(node.getID())
                    otherNode = nodeFile.readNode(otherNodeID, relationshipFile, propFile, labelFile)

                    # node has not been visited yet
                    if otherNodeID not in visitedNodeIDs:
                        # end node type is specified
                        if relEndNodeType != "":
                            print("rel end node type is: {0}".format(relEndNodeType))

                            # check if any of the labels of end node match relEndNodeType
                            for lbl in otherNode.getLabels():
                                print("node lbl: {0}".format(lbl.getLabelStr()))
                                # label matches end node type
                                if (lbl.getLabelStr() == relEndNodeType):
                                    # wanted end node
                                    if(wantedNode == 1):
                                        nextNodeQueue.put(otherNode)
                                    # wanted start node
                                    else:
                                        nextNodeQueue.put(node)
                                    print("put node in queue")

                        # end node can be of any type
                        else:
                            # wanted end node
                            if(wantedNode == 1):
                                nextNodeQueue.put(otherNode)
                            # wanted start node
                            else:
                                nextNodeQueue.put(node)
                            print("put node in queue")


        nodeQueue = nextNodeQueue

    return nodeQueue
