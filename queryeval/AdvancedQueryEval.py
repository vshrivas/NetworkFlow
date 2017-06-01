def getLabelIndex(label):
    return 0

def getNextNode(labelIndex):
    return 0

# TODO: create indexes on nodes and relationships based on label
# more specific indexes based on properties, etc. can be created later
# index should also store the average number of "connections" each item has
# this would be 2 for relationships, and the avg num of relationships for nodes

def advQueryEval(nodes, relationships, nodeFile, relationshipFile,
                        propFile, labelFile):
    """
    `nodes` should be a list of `DummyNode`s, and `relationships` should be
        a list of `DummyRelationship`s, such that the following pattern is to be
        matched:

        (node 1) -[relationship 1]-> (node 2) ... -[relationship n-1]-> (node n)

        Hence, len(nodes) must equal len(relationships) + 1.

        The return value is a set of tuples matching this description; that is,
        each tuple contains a `Node`, then a `Relationship`, then a `Node`, etc.
        All tuples, for now, must be of the same length, since we don't yet 
        support arbitrary-length relationship distances.
    """

    # need to make a list of the number of items in each category
    # list should have counts of items
    # need to find the type with least item
    """
    numRealNodes is of the format (index, numNodes), where index is the index of 
    the corresponding DummyNode in nodes. Currently, we are using the labels of 
    DummyNode as the different node types to consider. numNodes is the number of
    real nodes corresponding to the category of that DummyNode.
    """

    """ following should give us number of real nodes and real relationships in each category """
    """ where each dummy node or relationship is a category """
    # make dictionary {category: (list of nodeIDs to consider, avg num connections)}
    # make dictionary {category: (list of relIDs to consider, 2)}
    # for each dummy node in dummy nodes (each category):
        """ need to find nodes with all labels """
        # make variable for avg num connections for items this category
        # get number of labels
        # make dictionary {nodeID: numLabels}
        # for each label in dummy node labels
            # open label index
            # add avg number of connections for this label to var
            # add each node in index to dictionary, if not already there
            # increment label count for node
        """ select all nodes which have label count equal to number of labels """
        # for each entry in dictionary {nodeID: numLabels}
            # if numLabels = label count for dummy node
            # add nodeID list in dictionary {category: (list of nodeIDs to consider, avg num connections)}
        # divide var by number of labels to get avg num connections, and store in dictionary

    # repeat above block for each dummy relationship in dummy relationships

    """ cost = num items * avg num connections will serve as the heuristic for which category to consider first """
    # create list of viable nodes and viable relationships

    # while every node and rel category has not been considered:
        # iterate through "nodes/rels to consider" dictionaries to find category with lowest cost
        # minCostCategory = 0
        # for category in nodesToConsider:
            # calculate cost = num of nodeIDs to consider * avg num connections for category
            # if cost < cost of minCostCategory:
                # minCostCategory = this category
        # for category in relationshipsToConsider:
            # calculate cost = num of relIDs to consider * avg num connections for category (2)
            # if cost < cost of minCostCategory:
                # minCostCategory = this category

        # if the category is instanceof node:
            # for each node in category:
                # for each relationship of node:
                    """ finding viable relationships """
                    # foundLeft = false
                    # foundRight = false
                    # if rel category - 1 is visited:
                        # foundLeft = true
                    # if rel category is visited:
                        # foundRight = true
                    # if rel category - 1 has not been visited and relationship is of rel category - 1:
                        # if other node in relationship is of node category - 1:
                            # add relationship to list of left viable relationships (category - 1)
                            # add other node to list of viable nodes (category - 1)
                            # foundLeft = true
                    # if rel category has not been visited and relationship is of rel category:
                        # if other node in relationship is of node category + 1:
                            # add relationship to list of right viable relationships (category)
                            # add other node to list of viable nodes (category + 1)
                            # foundRight = true
                    # if foundLeft and foundRight:
                        # add this node to viable nodes (category)
            # remove this node category, and categories of left and right rels from nodesToConsider and relsToConsider
            # to mark these categories as visited

    
        # if the category is instanceof relationship:
            # for each relationship in category:
                # if one node is of category:
                    # if other node is of category + 1:
                        # add first node to viable nodes (category)
                        # add second node to viable nodes (category + 1)
                        # add this rel to viable rels (category)
            # remove this relationship category from relsToConsider to mark it as visited

    """ should now have all nodes and rels to make paths out of """
    # relationships can only connect 2 nodes
    # create dictionary with {nodeID: list of chains ending at node}
    # put nodes of category 1 in their own value lists

    # for category in rel categories:
        # for each rel in category:
            # check which node of rel is of category
            # for each branch ending at node of category:
                # attach rel and node of category + 1 (other node of rel) to branch
                # place branch in category + 1 node value list

    """ we expect all branches to end up in value lists of nodes in final category """

    # extract branches from value lists of nodes in final category

    # return branches









