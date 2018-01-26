class NodePage(DataPage):
	ENTRY_SIZE = Node.storageSize

	def __init__(self, pageID, datafile):
		super().__init__(pageID, datafile)

	def readNode(self, nodeID):
		# returns IDs of first relationship, property, and label
		# get list of relationships
			# will need to get properties for each relationship
			
		# get list of properties
		# get list of labels