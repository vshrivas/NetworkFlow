def getLabelIndex(label):
    pass

def getNextNode(labelIndex):
    pass

def getNodeFromID(nodeID):
    pass

def getRelFromID(relID):
    pass

# TODO: create indexes on nodes and relationships based on label
# more specific indexes based on properties, etc. can be created later
# index should also store the average number of "connections" each item has
# this would be 2 for relationships, and the avg num of relationships for nodes

def advQueryEval(dummyNodes, dummyRelationships, nodeFile, relationshipFile,
                        propFile, labelFile):
    """
    `dummyNodes is a dictionary of {category: dummyNode}, and similarly
    dummyRelationships is a dictionary of {category: dummyRelationships}, 
    such that the following pattern is to be matched. 
    Paths must always start and end with a node:

    (node 1) -[relationship 1]-> (node 2) ... -[relationship n-1]-> (node n)

    Hence, len(nodes) must equal len(relationships) + 1.

    The return value is a list of paths, consisting of nodes and relationships
    which fulfill this pattern.
    """

    """
    Currently, we are using the labels of DummyNode and DummyRelationship
    as the different node types to consider. Each DummyNode or DummyRelationship
    is a category. 
    """

    """ The following will give us the real nodes and relationships in each category. 
    We will read the nodeID/relIDs, as well as the average number of connections
    for each label from the label indexes. For categories with multiple labels 
    select nodes present in all label indexes, and average out the average number
    of connections across all indexes. """
    
    nodesToConsider = {} # dictionary of {category: [list of nodeIDs to consider, avg num connections]}
    relsToConsider = {} # dictionary of {category: list of relIDs to consider}

    for category in dummyNodes.keys(): # each dummyNode is a category
        """ real nodes with all labels are the nodes in this category """
        dummyNode = dummyNodes[category]
        avgNumConnections = 0.0 # avg num connections for items this category
        numCategoryLabels = len(dummyNode.getLabels()) # get number of labels in this category
        numNodeLabels = {} # dictionary tracks number of labels a given node has
        """ look at nodes in each label of category """
        for lbl in dummyNode.getLabels():
             # open label index
            lblIndex = openLabelIndex(lbl)
            # add avg number of connections for this label to var
            numLabelConnections = getNumConnections(lblIndex) # average number of connections of items in this category
            avgNumConnections += numLabelConnections
            # add each node in index to dictionary, if not already there
            # increment label count for node
            lblNodes = getItems(lblIndex)
            for nodeID in lblNodes:
                if nodeID not in numNodeLabels:
                    numNodeLabels[nodeID] = 1
                else:
                    numNodeLabels[nodeID] += 1
            
        """ Add all nodes which have label count equal to number of labels to 
        nodesToConsider, since these are the nodes which fit the category. """
        # for each entry in dictionary {nodeID: numLabels}
        nodesToConsider[category] = []
        categoryNodes = [] # list of nodes to consider for this category
        for nodeID in numNodeLabels.keys():
            # node has all labels of category
            if numNodeLabels[nodeID] == numCategoryLabels:
                categoryNodes.append(nodeID)
        # add nodes to consider for category and avg number of connections to dictionary
        nodesToConsider[category].append(categoryNodes)
        avgNumConnections /= numCategoryLabels
        nodesToConsider.append(avgNumConnections)

    for category in dummyRelationships.keys(): # each dummyNode is a category
        """ real relationships with all labels are the relationships in this category """
        dummyRel = dummyRelationships[category]
        numCategoryLabels = len(dummyRel.getLabels()) # get number of labels in this category
        numRelLabels = {} # dictionary tracks number of labels a given rel has
        """ look at rels in each label of category """
        for lbl in dummyRel.getLabels():
             # open label index
            lblIndex = openLabelIndex(lbl)
            # add each rel in index to dictionary, if not already there
            # increment label count for rel
            lblRels = getItems(lblIndex)
            for relID in lblRels:
                if relID not in numRelLabels:
                    numRelLabels[relID] = 1
                else:
                    numRelLabels[relID] += 1
            
        """ Add all rels which have label count equal to number of labels to 
        relsToConsider, since these are the rels which fit the category. """
        relsToConsider[category] = []
        categoryRels = [] # list of rels to consider for this category
        for relID in numRelLabels.keys():
            # rel has all labels of category
            if numNodeLabels[relID] == numCategoryLabels:
                categoryRels.append(relID)
        # add rels to consider for category and avg number of connections to dictionary
        relsToConsider[category].append(categoryRels)

    """ cost = num items * avg num connections will serve as the heuristic for which category to consider first """

    """ At each iteration, go through all node and relationship categories, and
    find the category with the lowest exploration cost. If this category is a
    dummyNode, find all viable nodes in category, viable rels in category - 1,
    viable rels in category, nodes to consider in category + 1, and nodes to
    consider in category - 1. If the category is an instance of dummyRelationship,
    find all viable relationships in category, nodes to consider in category, and
    nodes to consider in category + 1. """
    viableNodes = {} # dictionary {category: [viableNodes]}
    viableRels = {} # dictionary {category: [viableRels]}

    # while every node and rel category has not been considered
    while len(nodesToConsider) != 0 or len(relsToConsider) != 0:
        """ iterate through nodes/rels to consider dictionaries to find category with lowest cost """
        minCostCategoryNode = 0
        minCostCategoryRel = 0

        for category in nodesToConsider.keys():
            numNodes = len(nodesToConsider[category][0])
            avgNumConnections = nodesToConsider[category][1]
            cost = numNodes * avgNumConnections # calculate category cost
            if cost < minCostCategoryNode:
                minCostCategoryNode  = category

        for category in relsToConsider.keys():
            # calculate cost = num of relIDs to consider * avg num connections for category (2)
            numRels = len(relsToConsider[category][0])
            avgNumConnections = 2
            cost = numRels * avgNumConnections
            if cost < minCostCategoryRel:
                minCostCategoryRel = category

        minNodeCost = len(nodesToConsider[minCostCategoryNode][0]) * nodesToConsider[minCostCategoryNode][1]
        minRelCost = len(relsToConsider[minCostCategoryRel][0]) * relsToConsider[minCostCategoryRel][1]

        """ Node category has the lowest exploration cost. """
        if minNodeCost < minRelCost:
            category = minCostCategoryNode

            viableRels[category - 1] = []
            viableRels[category] = []
            viableNodes[category] = [] 

            leftNodesToConsider = [] # category - 1 nodes to consider
            rightNodesToConsider = [] # category + 1 nodes to consider
            leftViableRels = [] # category - 1 rels to consider
            rightViableRels = [] # category rels to consider

            for nodeID in nodesToConsider[minCostCategoryNode][0]: # for each node in category
                node = getNodeFromID(nodeID)
                for rel in node.getRelationships(): # for each relationship of node
                    otherNodeID = rel.getOtherNodeID(nodeID)
                    otherNode = getNodeFromID(otherNodeID)

                    """ finding viable relationships """
                    foundLeft = False
                    foundRight = False

                    """ Rel category - 1 has been visited. Left rels have been explored. """
                    if category - 1 not in relsToConsider.keys(): 
                        foundLeft = True 
                    """ Rel category has been visited. Right rels have been explored. """
                    if category not in relsToConsider.keys():
                        foundRight = True

                    """ Rel category - 1 (left rels) has not been visited and rel is of this category """
                    #TODO: add match rel function to dummyRelationship
                    if category - 1 in relsToConsider.keys() and dummyRelationships[category - 1].matchRel(rel):
                        """ other node in rel is of node category - 1"""
                        if dummyNodes[category - 1].matchNode(otherNode): 
                            leftViableRels.append(rel) # add relationship to list of left viable relationships (category - 1)
                            leftNodesToConsider.append(otherNode) # add other node to list of left nodes to consider (category - 1)
                            foundLeft = True # found at least one left relationship

                    # if rel category has not been visited and relationship is of rel category:
                    """ Rel category (right rels) has not been visited and rel is of this category """
                    if category in relsToConsider.keys() and dummyRelationships[category].match(rel):
                        """ other node in rel is of node category + 1"""
                        if dummyNodes[category + 1].matchNode(otherNode): 
                            rightViableRels.append(rel) # add relationship to list of right viable relationships (category)
                            rightNodesToConsider.append(otherNode) # add other node to list of right nodes (category + 1)
                            foundRight = True

                    """ this node is only viable if the path exists to the left and right of it"""
                    if foundLeft and foundRight:
                        viableNodes[category].append(node) # add this node to viable nodes (category)
                        """ left and right rels can only be viable if the current node is viable """
                        """ if added immediately, list of viable nodes/rels would have some nonviable items"""
                        viableRels[category - 1].extend(leftViableRels) # add list of left viable rels to list of viable rels
                        viableRels[category].extend(rightViableRels) # add list of right viable rels to list of viable rels

                        nodesToConsider[category - 1][0] = leftNodesToConsider # update left nodes to consider
                        nodesToConsider[category][0] = rightNodesToConsider # update right nodes to consider
                        
            # if nothing in viable nodes for this category, return immediately since no path can exist
            if len(viableNodes[category]) == 0:
                return []
            """ remove this node category, and categories of left and right rels 
            from nodesToConsider and relsToConsider to mark these categories as visited """
            nodesToConsider.pop(category, None) # pop this category of nodes from nodes to consider
            relsToConsider.pop(category - 1, None) # pop left rels from rels to consider
            relsToConsider.pop(category, None) # pop right rels from rels to consider
    
        # if the category is instanceof relationship:
        """ Relationship category has the lowest exploration cost. """
        else:
            # clear out nodes to consider for categories category and category + 1
            # since we will be updating that based on these relationships
            # for each relationship in category:
            leftNodesToConsider = [] # category nodes to consider
            rightNodesToConsider = [] # category + 1 nodes to consider  

            for relID in relsToConsider[minCostCategoryRel][0]:
                rel = getRelFromID(relID)

                firstNode = getNodeFromID(rel.getFirstNodeID()) # first node in rel
                secondNode = getNodeFromID(rel.getSecondNodeID()) # second node in rel

                """ if left and right nodes of rel match category requirements """
                if dummyNodes[category].matchNode(firstNode): # first node is of type category 
                    if dummyNodes[category + 1].matchNode(secondNode): # second node is of type category + 1
                        leftNodesToConsider.append(firstNode) # add to left nodes (category) to consider
                        rightNodesToConsider.append(secondNode) # add to right nodes (category + 1) to consider
                        viableRels[category].append(rel)

                if dummyNodes[category].matchNode(secondNode): # second node is of type category 
                    if dummyNodes[category + 1].matchNode(firstNode): # first node is of type category + 1
                        leftNodesToConsider.append(secondNode) # add to left nodes (category) to consider
                        rightNodesToConsider.append(firstNode) # add to right nodes (category + 1) to consider
                        viableRels[category].append(rel)

                nodesToConsider[category][0] = leftNodesToConsider # update left nodes (category) to consider
                nodesToConsider[category + 1][0] = rightNodesToConsider # update right nodes (category + 1) to consider

            # if no viable relationships of this category, return immediately since no path can exist
            if len(viableRels[category]) == 0:
                return []
            # remove this relationship category from relsToConsider to mark it as visited
            relsToConsider.pop(category, None)

    """ Should now have all nodes and rels to make paths out of. """

    """ Relationships can only connect 2 nodes so use them to generate path chains.
    We create a dictionary of nodeIDs and all branches ending at that node. We 
    iterate through all of the relationship categories, and go through each of 
    the relationships in a given category. We use the relationship to determine
    which of its node is from the previous node category and which is from the 
    next. We append the relationship and the next node to all of the branches
    ending at the previous node, and place these new branches in the next node
    value list of the dictionary. At the end all complete result branches will
    end up in the value lists of nodes in the final category. """
    pathChains = {} # dictionary with {nodeID: list of chains ending at node}
                    # chains are lists of nodes and relationships

    # put nodes of category 1 in their own value lists
    for viableNode in viableNodes[1]:
        pathChains[viableNode.getID()] = [viableNode.getID()]

    for category in viableRels.keys(): # for category in rel categories
        for rel in viableRels[category]: # for each rel in category
            # check which node of rel is of category
            firstNode = getNodeFromID(rel.getFirstNodeID()) # first node in rel
            secondNode = getNodeFromID(rel.getSecondNodeID()) # second node in rel

            # find which node in rel is the left node and which is the right node
            oldEndNode = firstNode
            newEndNode = secondNode
            if dummyNodes[category].matchNode(secondNode):
                oldEndNode = secondNode
                newEndNode = firstNode

            # for each branch ending at this node:
            for branch in pathChains[oldEndNode.getID()]:
                # attach this rel and node of category + 1 (other node of rel) to branch
                branch.extend(rel)
                branch.extend(newEndNode)
                # place branch in category + 1 node value list
                if newEndNode.getID() in pathChains.keys():
                    pathChains[newEndNode.getID()].append(branch)
                else:
                    pathChains[newEndNode.getID()] = [branch]

    """ We expect all branches to end up in value lists of nodes in final category. """

    resultBranches = []
    finalNodeCategory = max(viableNodes.keys())

    for node in viableNodes[finalNodeCategory]: # extract branches from value lists of nodes in final category
        resultBranches.extend(pathChains[node.getID()])

    # return branches
    return resultBranches