from queue import Queue


# conditions is a list of tuples of the form (relationship type, type of other 
	# node in relationship)
# returns a queue of nodes that fit the conditions of the query
def breadthFirstSearch(rootNode, conditions, nodeFile, relationshipFile, propFile, labelFile):
	print("starting breatdth first...")
	visitedNodeIDs = []
	# queue will hold all nodes for a particular depth
	nodeQueue = Queue()
	nodeQueue.put(rootNode)

	for conditionTuple in conditions:
		# conditions for nodes selected in this level
		relType = conditionTuple[0]
		print("relationship type: {0}".format(relType))
		relEndNodeType = conditionTuple[1]
		print("relationship end node type: {0}".format(relEndNodeType))
		# create a new queue to store nodes for this level
		nextNodeQueue = Queue()

		# while all nodes from previous level have not been considered
		while(not nodeQueue.empty()):
			node = nodeQueue.get()
			# mark node as visited
			visitedNodeIDs.append(node.getID())
			print("node in queue props:")
			for prop in node.properties:
				print("key: {0}".format(prop.key))
				print("value: {0}".format(prop.value))
			# get relationships from node
			rels = node.getRelationships()

			# check each relationship of node
			for rel in rels:
				#TODO: need to add labels/types to relationships
				# if relationship is of type necessary
				print("rel is of type: {0}".format(rel.getRelType()))
				print("rel type needed: {0}".format(relType))
				print(len(rel.getRelType()))
				print(len(relType))
				if rel.getRelType().rstrip(' ') == relType:
				#if True:
					# select the other node in the relationship
					otherNodeID = rel.getOtherNodeID(node.getID())
					otherNode = nodeFile.readNode(otherNodeID, relationshipFile, propFile, labelFile)
					# node has not been visited yet
					if otherNodeID not in visitedNodeIDs:
						# if an end node type is specified 
						if relEndNodeType != "":
							# check if any of the labels of otherNode match 
							# relEndNodeType
							if relEndNodeType in otherNode.getLabels():
								nextNodeQueue.put(otherNode)
								print("put node in queue")
						# otherNode can be of any type
						else:
							nextNodeQueue.put(otherNode)
							print("put node in queue")


		nodeQueue = nextNodeQueue

	return nodeQueue
