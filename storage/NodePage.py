class NodePage(DataPage):
	ENTRY_SIZE = Node.storageSize

	# constructor for NodePage
	# takes in 
	# pageIndex: index of page (unique across nodeFiles)
	# datafile: nodeFile containing page
	def __init__(self, pageIndex, datafile):
		# 0 indicates that this is a node page
		pageID = [0, pageIndex]
		super().__init__(pageID, datafile)

		self.nodeData = []  # list of node objects the page contains
		# read in all page data
		readPageData()

	def readPageData():
		filePath = ((DataFile) self.file).getFilePath()
		nodeFile = open(filePath, 'rb')

		# read in number of entries
		nodeFile.seek(self.pageStart + NUM_ENTRIES_OFFSET)
		self.numEntries = int.from_bytes(nodeFile.read(DataPage.NUM_ENTRIES_SIZE), sys.byteorder, signed=True)

		# read in owner of page
		nodeFile.seek(self.pageStart + OWNER_ID_OFFSET)
		self.ownerID = int.from_bytes(nodeFile.read(DataPage.OWNER_ID_SIZE), sys.byteorder, signed=True)

		# read in all data items
		for nodeIndex in range(0, self.numEntries):
			node = readNodeData(nodeIndex)
			nodeData.append(node)

	def readNode(self, nodeIndex):
		return nodeData[nodeIndex]

	# reads in node from page in file, using nodeIndex 
	# used when loading page data into memory
	# takes in nodeIndex
	# returns node
	def readNodeData(self, nodeIndex):
		filePath = ((NodeFile) self.file).getFilePath()
		nodeFile = open(filePath, 'rb')

		nodeStartOffset = self.pageStart + DATA_OFFSET + nodeIndex * Node.storageSize
		
		# read first rel ID, first property ID, first label ID
        nodeFile.seek(nodeStartOffset + Node.REL_ID_OFFSET)
        firstRelID = int.from_bytes(nodeFile.read(Node.nodeIDByteLen), sys.byteorder, signed=True)

        nodeFile.seek(nodeStartOffset + Node.PROPERTY_ID_OFFSET)
        firstPropID = int.from_bytes(nodeFile.read(Property.propIDByteLen), sys.byteorder, signed=True)

		nodeFile.seek(nodeStartOffset + Node.LABEL_ID_OFFSET)
		firstLabelID = int.from_bytes(nodeFile.read(Label.labelIDByteLen), sys.byteorder, signed=True)

        nodeAttributes = [firstRelID, firstPropID, firstLabelID]

        nodeRelationships = RelationshipStoreManager.getRelChain(firstRelID)
		nodeProperties = PropertyStoreManager.getPropChain(firstPropID)
		nodeLabels = LabelStoreManager.getLabelChain(firstLabelID)

		node = Node(datafile, pageID, nodeIndex)
		node.addRelationships(nodeRelationships)
		node.addProperties(nodeProperties)
		node.addLabels(nodeLabels)

		return node

	# syncs node data to disk
    def writeNode(self, node):
		# open node file
        storeFilePath = ((NodeFile) self.file).getFilePath()
        storeFile = open(storeFilePath, 'r+b')

        if DEBUG:
            print("opened store file: {0}". format(storeFileName))

        # start of page offset
        startPage = pageIndex * DataPage.MAX_PAGE_SIZE

        # write node id
        storeFile.seek(self.startPage + node.startOffset + Node.NODE_ID_OFFSET)
        storeFile.write((node.nodeID).to_bytes(Node.nodeIDByteLen,
            byteorder = sys.byteorder, signed=True))

        if DEBUG:
            print("wrote node ID: {0}". format(node.nodeID))

        # write in-use flag
        storeFile.seek(self.startPage + node.startOffset + Node.IN_USE_FLAG_OFFSET)
        storeFile.write((1).to_bytes(1, byteorder = sys.byteorder, signed=True))

        if DEBUG:
            print("wrote in-use flag: {0}". format(1))

        # write first relationship ID
        storeFile.seek(self.startPage + node.startOffset + Node.REL_ID_OFFSET)
        # if there are no relationships, write -1 as first relationship ID
        if len(node.relationships) == 0:
            firstRel = -1
            storeFile.write((-1).to_bytes(Relationship.relIDByteLen,
                byteorder = sys.byteorder, signed=True))
            if DEBUG:
                print("wrote first rel ID: -1")
        # otherwise, write first relationship ID
        else:
            firstRel = node.relationships[0]
            storeFile.write(firstRel.getID().to_bytes(Relationship.relIDByteLen,
                byteorder = sys.byteorder, signed=True))
            if DEBUG:
                print("wrote first rel ID: {0}". format(firstRel.getID()))

        # write first property ID
        storeFile.seek(self.startPage + node.startOffset + Node.PROPERTY_ID_OFFSET)
        # if there are no properties, write -1 as first property ID
        if len(node.properties) == 0:
            firstProp = -1
            storeFile.write((-1).to_bytes(Property.propIDByteLen,
                byteorder = sys.byteorder, signed=True))
            if DEBUG:
                print("wrote first property ID: -1")
        # otherwise, write first property ID
        else:
            firstProp = node.properties[0]
            storeFile.write(firstProp.getID().to_bytes(Property.propIDByteLen,
                byteorder = sys.byteorder, signed=True))
            if DEBUG:
                print("wrote first property ID: {0}". format(firstProp.getID()))

        # write first label ID
        storeFile.seek(self.startPage + node.startOffset + Node.LABEL_ID_OFFSET)
        # if there are no labels, write -1 as first label ID
        if len(node.labels) == 0:
            storeFile.write((-1).to_bytes(Label.LABEL_OFFSET,
                byteorder = sys.byteorder, signed=True))
        # otherwise, write first label ID
        else:
            firstLabel = node.labels[0]
            storeFile.write(firstLabel.getLabelID().to_bytes(Label.LABEL_OFFSET,
                byteorder = sys.byteorder, signed=True))

    def createNode():
    	# create a new node object
    	newNode = Node()
