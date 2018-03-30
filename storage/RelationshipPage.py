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
	def readPageData(self):
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
	def readRelationshipData(self, relationshipIndex):
		# open relationship file
		filePath = ((DataFile) self.file).getFilePath()
		relationshipStore = open(filePath, 'rb')

		# offset from start of file to start of node
		relationshipStartOffset = self.pageStart + DATA_OFFSET + relationshipIndex * Relationship.storageSize

		# find ID of relationship, technically should be index
		relationshipStore.seek(relationshipStartOffset + Relationship.RELATIONSHIP_ID_OFFSET)
		relID = int.from_bytes(relationshipStore.read(Relationship.relIDByteLen), sys.byteorder, signed=True)

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

        relationshipStore.seek(relationshipStartOffset + Relationship.PROPERTY_ID_OFFSET)
       	propertyID = int.from_bytes(relationshipStore.read(Property.propIDByteLen), sys.byteorder, signed=True)

        # create relationship and add to node
        rel = Relationship(relID, node1ID, node2ID, relType, node1NextRelID, node1PrevRelID,
        		node2NextRelID, node2PrevRelID, propertyID, datafile)

        return rel

    def readRelationship(self, relationshipIndex):
    	return relationshipData[relationshipIndex]

    def writeRelationship(self, rel):
    	relID = rel.getID()

        relIndex = relID[1]
        relationshipData[relIndex] = rel

    def writePageData(self):
    	filePath = ((RelationshipFile) self.datafile).getFilePath()
		relFile = open(filePath, 'rb')

    	for rel in relationshipData:
    		writeRelationshipData(rel, relFile)

    def writeRelationshipData(self, rel, relationshipStore):
    	# offset from start of file to start of node
		relationshipStartOffset = self.pageStart + DATA_OFFSET + relationshipIndex * Relationship.storageSize

		# write ID of relationship, technically should be index
		relationshipStore.seek(relationshipStartOffset + Relationship.RELATIONSHIP_ID_OFFSET)
		relationshipStore.write(rel.getID().to_bytes(Relationship.relIDByteLen, 
            byteorder = sys.byteorder, signed=True))

		# write ID of first node in relationship
        relationshipStore.seek(relationshipStartOffset + Relationship.NODE1_ID_OFFSET)
        relationshipStore.write(rel.firstNodeID.to_bytes(Node.nodeIDByteLen, 
            byteorder = sys.byteorder, signed=True))

        # write ID of second node in relationship
        relationshipStore.seek(relationshipStartOffset + Relationship.NODE2_ID_OFFSET)
        relationshipStore.write(rel.secondNodeID.to_bytes(Node.nodeIDByteLen, 
            byteorder = sys.byteorder, signed=True))

        # write ID of next rel for node1 in relationship
        relationshipStore.seek(relationshipStartOffset + Relationship.NODE1_NEXT_REL_ID_OFFSET)
        relationshipStore.write(rel.node1NextRelID.to_bytes(Relationship.relIDByteLen, 
            byteorder = sys.byteorder, signed=True))

        # write ID of prev rel for node1 in relationship
        relationshipStore.seek(relationshipStartOffset + Relationship.NODE1_PREV_REL_ID_OFFSET)
        relationshipStore.write(rel.node1PrevRelID.to_bytes(Relationship.relIDByteLen, 
            byteorder = sys.byteorder, signed=True))

        # write ID of next rel for node2 in relationship
        relationshipStore.seek(relationshipStartOffset + Relationship.NODE2_NEXT_REL_ID_OFFSET)
        relationshipStore.write(rel.node2NextRelID.to_bytes(Relationship.relIDByteLen, 
            byteorder = sys.byteorder, signed=True))

        # write ID of prev rel for node2 in relationship
        relationshipStore.seek(relationshipStartOffset + Relationship.NODE2_PREV_REL_ID_OFFSET)
        relationshipStore.write(rel.node2PrevRelID.to_bytes(Relationship.relIDByteLen, 
            byteorder = sys.byteorder, signed=True))

        # write type of relationship
        relationshipStore.seek(relationshipStartOffset + Relationship.RELATIONSHIP_TYPE_OFFSET)
        # type is not of max size
        if(sys.getsizeof(rel.type) != Relationship.MAX_TYPE_SIZE):
            # pad relationship type string up to max size
            while len(rel.type.encode('utf-8')) != Relationship.MAX_TYPE_SIZE:
                rel.type += ' '

        relationshipStore.write(bytearray(rel.type, 'utf8'))
        # strip out additional whitespace used for padding from type
        rel.type = rel.type.rstrip(' ')

        # write first property ID
        relationshipStore.seek(relationshipStartOffset + Relationship.PROPERTY_ID_OFFSET)
        relationshipStore.write(rel.propertyID.to_bytes(Property.propIDByteLen, 
            byteorder = sys.byteorder, signed=True))


	'''def OLDwriteRelationshipData(self, node, prevRel, nextRel):
        """Write relationship to relationship file for specified node and relationship's 
        properties to property file.

        Arguments:
        node: node relationship being written for
        prevRel: previous relationship for specified node
        nextRel: next relationship for specified node
        """
        # open relationship file
        if DEBUG:
            print(self.relationshipFile)
        storeFilePath = self.relationshipFile.getFilePath()
        storeFile = open(storeFilePath, 'r+b')

        # seek to location for relationship
        storeFile.seek(self.startOffset)

        # write relationship ID
        storeFile.write(self.relationshipID.to_bytes(Relationship.relIDByteLen, 
            byteorder = sys.byteorder, signed=True))
        if DEBUG:
            print("wrote relationship id")

        # write node 1 id
        storeFile.seek(self.startOffset + Relationship.NODE1_ID_OFFSET)
        storeFile.write(self.firstNodeID.to_bytes(3, 
            byteorder = sys.byteorder, signed=True))
        if DEBUG:
            print("wrote first node id")

        # write node 2 id
        storeFile.seek(self.startOffset + Relationship.NODE2_ID_OFFSET)
        storeFile.write(self.secondNodeID.to_bytes(3, 
            byteorder = sys.byteorder, signed=True))
        if DEBUG:
            print("wrote second node id")

        # find which node relationship is being written for and write next and previous 
        # relationship IDs appropriately
        if node.getID() == self.firstNodeID:
            if DEBUG:
                print("writing relationship for first node")

            storeFile.seek(self.startOffset + Relationship.NODE1_NEXT_REL_ID_OFFSET)
            storeFile.write(nextRel.getID().to_bytes(Relationship.relIDByteLen, 
                byteorder = sys.byteorder, signed=True))

            storeFile.seek(self.startOffset + Relationship.NODE1_PREV_REL_ID_OFFSET)
            storeFile.write(prevRel.getID().to_bytes(Relationship.relIDByteLen, 
                byteorder = sys.byteorder, signed=True))

        else:
            if DEBUG:
                print("writing relationship for second node")
            storeFile.seek(self.startOffset + Relationship.NODE2_NEXT_REL_ID_OFFSET)
            storeFile.write(nextRel.getID().to_bytes(Relationship.relIDByteLen, 
                byteorder = sys.byteorder, signed = True))

            storeFile.seek(self.startOffset + Relationship.NODE2_PREV_REL_ID_OFFSET)
            storeFile.write(prevRel.getID().to_bytes(Relationship.relIDByteLen, 
                byteorder = sys.byteorder, signed = True))

        # write relationship type
        if DEBUG:
            print("writing relationship type")
        storeFile.seek(self.startOffset + Relationship.RELATIONSHIP_TYPE_OFFSET)

        # type is not of max size
        if(sys.getsizeof(self.type) != self.MAX_TYPE_SIZE):
            # pad relationship type string up to max size
            while len(self.type.encode('utf-8')) != self.MAX_TYPE_SIZE:
                self.type += ' '

        storeFile.write(bytearray(self.type, 'utf8'))
        # strip out additional whitespace used for padding from type
        self.type = self.type.rstrip(' ')

        # write first property ID
        storeFile.seek(self.startOffset + Relationship.PROPERTY_ID_OFFSET)

        # if no properties write -1 for first ID
        if len(self.properties) == 0:
            firstProp = -1
            storeFile.write((-1).to_bytes(Property.propIDByteLen,
                byteorder = sys.byteorder, signed=True))
            if DEBUG:
                print("wrote first property ID: -1")
        # otherwise write id of first property
        else:
            firstProp = self.properties[0]
            storeFile.write(firstProp.getID().to_bytes(Property.propIDByteLen,
                byteorder = sys.byteorder, signed=True))
            if DEBUG:
                print("wrote first property ID: {0}". format(firstProp.getID()))


        # write properties to property file
        if DEBUG:
            print("writing properties to property file ...")

        # write properties to property file
        for propIndex in range(0, len(self.properties)):
            prop = self.properties[propIndex]
            if DEBUG:
                print("writing {0} property ".format(prop.getID()))

            # case of no next property
            if propIndex == len(self.properties) - 1:
                if DEBUG:
                    print("no next property")
                # A placeholder property since there is no next property
                nullProperty = Property("", "", "", -1)
                prop.writeProperty(nullProperty)
            # case of next property
            else:
                prop.writeProperty(self.properties[propIndex + 1])'''
