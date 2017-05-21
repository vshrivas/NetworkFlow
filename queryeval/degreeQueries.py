from queue import Queue

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
