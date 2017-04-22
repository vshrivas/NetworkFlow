# Node class: stores data

# Storage: Nodes will be stored as fixed size records which are 9 bytes in 
# length.
# Bytes 1-3: Node ID
# Byte 4: In-use flag
# Bytes 5-8: ID of first relationship connected to node
# Bytes 9-11: ID of first property (key-value pair) for node
# Bytes 12-14: points to label store for node
# Byte 15: flags  
class Node:
	storageSize = 15
	numNodes = 0

	def _init_(self):
		# relationships is the list of relationships this node is in 
		self.relationships = []
		# key-value pairs or properties stored within node
		# e.g. name: Jane
		self.data = {}
		# labels indicate the type of a node, a node can have multiple labels
		# e.g. person, bank account, id
		self.labels = []
		# increment number of nodes 
		numNodes += 1
		self.nodeID = numNodes

	# This method adds a node with a relationship to this node's adj list
	def addRelationship(rel):
		self.relationship.append(rel)

	# This method adds data to a node 
	def addData(key, value):
		self.data[key] = value

	# This method adds labels to a node
	def addLabels(nodeLabel):
		self.labels.append(nodeLabel)

	# This method writes this node to the given dbFile and dbPage
	def storeNode(nodePage):
		# write node in nodePage
		# move ID * storageSize bytes into nodePage






