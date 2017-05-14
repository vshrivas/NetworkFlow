import Queue

# conditions is a list of tuples of the form (relationship type, other node in
	# relationship)
# returns a queue of nodes that fit the conditions
def breadthfirstSearch(rootNode, conditions):
	# queue will hold all nodes for a particular depth
	nodeQueue = Queue()
	nodeQueue.put(rootNode)

	for conditionTuple in conditions:
		relType = conditionTuple[0]
		relEndNodeType = conditionTuple[1]
		nextNodeQueue = Queue()

		while(!nodeQueue.empty()):
			node = nodeQueue.get()
			rels = node.getRelationships()

			for rel in rels:
				#TODO: need to add labels/types to relationships
				if rel.getType() == relType:
					otherNode = rel.getOtherNode(node.getID())

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
