class RelationshipPage(DataPage):
	def __init__(self, pageIndex, datafile):
		# 1 indicates that this is a relationship page
		pageID = [1, pageIndex]
		super().__init__(pageID, datafile)

		self.relationshipData = []  # list of relationship objects the page contains
		# read in all page data
		readPageData()

	# reads in all of the relationship objects stored in this page
	# stores them in self.relationshipData
	def readPageData():
		# open relationship file
		filePath = ((DataFile) self.file).getFilePath()
		relationshipFile = open(filePath, 'rb')

		# read in number of entries
		relationshipFile.seek(self.pageStart + NUM_ENTRIES_OFFSET)
		self.numEntries = int.from_bytes(relationshipFile.read(DataPage.NUM_ENTRIES_SIZE), sys.byteorder, signed=True)

		# read in owner of page
		relationshipFile.seek(self.pageStart + OWNER_ID_OFFSET)
		self.ownerID = int.from_bytes(relationshipFile.read(DataPage.OWNER_ID_SIZE), sys.byteorder, signed=True)

		# read in all data items
		for relationshipIndex in range(0, self.numEntries):
			relationship = readRelationshipData(relationshipIndex)
			relationshipData.append(relationship)

	# returns relationship from relationshipIndex
	# used while reading in page data
	def readRelationshipData(relationshipIndex):
		# open relationship file
		filePath = ((DataFile) self.file).getFilePath()
		relationshipStore = open(filePath, 'rb')

		# offset from start of file to start of node
		relationshipStartOffset = self.pageStart + DATA_OFFSET + relationshipIndex * Relationship.storageSize

		# find ID of first node in relationship
        relationshipStore.seek(relationshipStartOffset + Relationship.NODE1_ID_OFFSET)
        node1ID = int.from_bytes(relationshipStore.read(Node.nodeIDByteLen), sys.byteorder, signed=True)

        # find ID of second node in relationship
        relationshipStore.seek(relationshipStartOffset + Relationship.NODE2_ID_OFFSET)
        node2ID = int.from_bytes(relationshipStore.read(Node.nodeIDByteLen), sys.byteorder, signed=True)

        # find ID of next rel for node1 in relationship
        relationshipStore.seek(relationshipStartOffset + Relationship.NODE1_NEXT_REL_ID_OFFSET)
        node1NextRelID = int.from_bytes(relationshipStore.read(Relationship.relIDByteLen), sys.byteorder, signed=True)

        # find ID of prev rel for node1 in relationship
        relationshipStore.seek(relationshipStartOffset + Relationship.NODE1_PREV_REL_ID_OFFSET)
        node1PrevRelID = int.from_bytes(relationshipStore.read(Relationship.relIDByteLen), sys.byteorder, signed=True)

        # find ID of next rel for node2 in relationship
        relationshipStore.seek(relationshipStartOffset + Relationship.NODE2_NEXT_REL_ID_OFFSET)
        node2NextRelID = int.from_bytes(relationshipStore.read(Relationship.relIDByteLen), sys.byteorder, signed=True)

        # find ID of prev rel for node2 in relationship
        relationshipStore.seek(relationshipStartOffset + Relationship.NODE2_PREV_REL_ID_OFFSET)
        node2PrevRelID = int.from_bytes(relationshipStore.read(Relationship.relIDByteLen), sys.byteorder, signed=True)

        # read in type of relationship
        relationshipStore.seek(relationshipStartOffset + Relationship.RELATIONSHIP_TYPE_OFFSET)
        relType = relationshipStore.read(Relationship.MAX_TYPE_SIZE).decode("utf-8")
        relType = relType.rstrip(' ')

        if DEBUG:
            print('Node 1 id: {0}'.format(node1ID))
            print('Node 2 id: {0}'.format(node2ID))
            print('Relationship type: {0}'.format(relType))

        # create relationship and add to node
        rel = Relationship(relID, node1ID, node2ID, relType, node1NextRelID, node1PrevRelID,
        		node2NextRelID, node2PrevRelID, datafile)

        return rel

    def readRelationship(self, relationshipIndex):
    	return relationshipData[relationshipIndex]

	def writeRelationship():