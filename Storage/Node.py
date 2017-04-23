# Node class: stores data

# Storage: Nodes will be stored as fixed size records which are 9 bytes in 
# length.
# Bytes 1-3: Node ID
# Byte 4: In-use flag (1 for in-use, 0 for not)
# Bytes 5-8: ID of first relationship connected to node
# Bytes 9-11: ID of first property (key-value pair) for node
# Bytes 12-14: points to label store for node
# Byte 15: flags  
class Node:
	NODE_ID_OFFSET = 0
	IN_USE_FLAG_OFFSET = 3 
	REL_ID_OFFSET = 4
	PROPERTY_ID_OFFSET = 8
	LABEL_STORE_PTR_OFFSET = 11
	FLAGS_OFFSET = 14

	storageSize = 15
	numNodes = 0

	def _init_(self, nodeFile):
		# relationships is the list of relationships this node is in 
		self.relationships = []
		# key-value pairs or properties stored within node
		# e.g. name: Jane
		self.properties = {}
		# labels indicate the type of a node, a node can have multiple labels
		# e.g. person, bank account, id
		self.labels = []

		self.nodeID = numNodes
		# increment number of nodes 
		numNodes += 1

		self.nodeFile = nodeFile

		self.startOffset = self.nodeID * Node.storageSize

	# This method adds a node with a relationship to this node's adj list
	def addRelationship(rel):
			self.relationship.append(rel)

	# This method adds data to a node 
	def addData(key, value):
		self.properties[key] = value

	# This method adds labels to a node
	def addLabels(nodeLabel):
		self.labels.append(nodeLabel)

	def getID():
		return self.nodeID

	def getRelationships():
		return self.relationships

	def getData():
		return self.data

	def getLabels():
		return self.labels

	# This method writes this node to the given node file
	def writeNode():
		# open node file
		storeFileName = self.nodeFile.getFileName()
		storeFile = open(storeFileName, 'w')

		# move nodeID * storageSize bytes into nodeFile to get to start of node
		storeFile.seek(self.nodeID * Node.storageSize)
		storeFile.write(self.nodeID)

		# write in-use flag
		storeFile.seek(self.startOffset + IN_USE_FLAG_OFFSET)
		storeFile.write(1)

		# write first rel ID
		storeFile.seek(self.startOffset + REL_ID_OFFSET)
		firstRel = self.relationships[0]
		storeFile.write(firstRel.getID())

		#TODO: write first property ID

		# write relationships to relationship file
		for relIndex in range(0, len(self.relationships)):
			rel = self.relationships[relIndex]
			if relIndex == 0:
				rel.writeRelationship(self, "", self.relationships[relIndex + 1])
			elif relIndex == len(self.relationships) - 1:
				rel.writeRelationship(self, self.relationships[relIndex - 1], "")
			else:
				rel.writeRelationship(self, self.relationships[relIndex - 1], 
					self.relationships[relIndex + 1])

		














