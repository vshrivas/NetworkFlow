from queue import Queue

def breadthFirstSearch_(nodes, relationships, nodeFile, relationshipFile,
                        propFile, labelFile):
    """Perform a breadth-first-search and return patterns satisfying the input.

    `nodes` should be a list of `DummyNode`s, and `relationships` should be
    a list of `DummyRelationship`s, such that the following pattern is to be
    matched:

    (node 1) -[relationship 1]-> (node 2) ... -[relationship n-1]-> (node n)

    Hence, len(nodes) must equal len(relationships) + 1.

    The return value is a queue of tuples matching this description; that is,
    each tuple contains a `Node`, then a `Relationship`, then a `Node`, etc.
    All tuples, for now, must be of the same length, since we don't yet support
    arbitrary-length relationship distances.
    """
    # Figure out which node to start with in the pattern. This is a nontrivial
    # problem; logically, we should start with the most-specific node or
    # relationship, then work our way outwards from there. However, right now
    # we just naively choose the first node in the list.
    start = findBestElement(nodes, relationships)

    # Find start in the storage layer
    # Base case 1: start is a relationship
        # Fix this so it is sandwiched between two nodes.
        # Find all the nodes attached to the relationship that match all
        # specifications in the input lists.
    # Base case 2: start is a node

    # Push chain(s, plural if base case 1, single if base case 2) to queue

    # Pop a chain off the queue
    # IH: chain looks like (n) -[]-> ... -[]-> (m) of any length (include (n))
    # For leftmost node in chain (first element in the list)
    # IF leftmost node is NOT node 1:
        # Look at relationships emanating from this node
        # Look at DummyRelationships emanating from the corresponding DummyNode
            # Note that this means we need a mapping between dummy<-->real
            # The mapping could be a hash, or it could be index-based (order)
        # Find all relationships matching Dummy specs; attach leftwards.
            # If none found, continue to next chain.
        # For each found relationship, get all real nodes associated.
        # Find the DummyNodes that should match specs with those real nodes.
        # Make all possible chains leftward and push all. Done.
    # ELSE IF rightmost node is NOT node n:
        # Same thing, but rightwards.
    # ELSE IF leftmost node is 1, and rightmost is n:
        # Do nothing? Add to "good" queue?
    # ELSE
        # Do nothing? (Wasn't long enough, so it won't get returned)



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
