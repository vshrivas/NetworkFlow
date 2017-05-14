import Queue

# conditions is a list of tuples of the form (relationship type, other node in
	# relationship)
# returns a queue of nodes that fit the conditions of the query
def breadthfirstSearch(rootNode, conditions):
	# queue will hold all nodes for a particular depth
	nodeQueue = Queue()
	nodeQueue.put(rootNode)

	for conditionTuple in conditions:
		# conditions for nodes selected in this level
		relType = conditionTuple[0]
		relEndNodeType = conditionTuple[1]
		# create a new queue to store nodes for this level
		nextNodeQueue = Queue()

		# while all nodes from previous level have not been considered
		while(!nodeQueue.empty()):
			node = nodeQueue.get()
			# get relationships from node
			rels = node.getRelationships()

			# check each relationship of node
			for rel in rels:
				#TODO: need to add labels/types to relationships
				# if relationship is of type necessary
				if rel.getType() == relType:
					# select the other node in the relationship
					otherNode = rel.getOtherNode(node.getID())

					# if an end node type is specified 
					if relEndNodeType != "":
						# check if any of the labels of otherNode match 
						# relEndNodeType
						if relEndNodeType in otherNode.getLabels():
							nextNodeQueue.put(otherNode)
					# otherNode can be of any type
					else:
						nextNodeQueue.put(otherNode)


		nodeQueue = nextNodeQueue

	return nodeQueue
