class NodeFile:
	numFiles = 0

	def _init_(self):
		numFiles += 1
		self.fileID = numFiles
		
		# create node file
		self.fileName = "NodeFile{0}".format(self.fileID)
		nodeFile = open(self.fileName, 'w')
		nodeFile.close()

	def getFileName(self):
		return self.fileName

	# This method reads a given node based on nodeID and returns a node object for it
	def readNode(self, nodeID, relationshipFile, propertyFile, labelFile):
		node = Node(self)

		nodeStore = open(self.fileName, 'r')
		nodeStartOffset = nodeID * Node.storageSize

		# TODO: refactor some of reading relationships and properties into those classes

		# find all relationships
		# read first rel ID
		nodeFile.seek(nodeStartOffset + Node.REL_ID_OFFSET)
		firstRelID = nodeFile.read(4)

		relationshipStore = open(relationshipFile.getFileName(), 'r')
		nextRelID = firstRelID

		# while there is a next relationship
		while(nextRelID != -1):
			relationshipStartOffset = nextRelID * Relationship.storageSize

			# find ID of first node in relationship
			relationshipStore.seek(relationshipStartOffset + NODE1_ID_OFFSET)
			node1ID = relationshipStore.read(3)

			# find ID of second node in relationship
			relationshipStore.seek(relationshipStartOffset + NODE2_ID_OFFSET)
			node2ID = relationshipStore.read(3)

			# create relationship and add to node
			rel = Relationship(node1ID, node2ID, relationshipFile)
			node.addRelationship(rel)

			# find next rel ID
			if nodeID == node1ID:
				relationshipStore.seek(relationshipStartOffset + NODE1_NEXT_REL_ID_OFFSET)
				nextRelID = relationshipStore.read(4)
			else:
				relationshipStore.seek(relationshipStartOffset + NODE2_NEXT_REL_ID_OFFSET)
				nextRelID = relationshipStore.read(4)


		# read first property ID
		nodeFile.seek(startOffset + Node.PROPERTY_ID_OFFSET)
		firstPropID = nodeFile.read(4)

		propertyStore = open(propertyFile.getFileName(), 'r')
		nextPropID = firstPropID

		while(nextPropID != -1):
			propertyStartOffset = nextPropID * Property.storageSize

			# find key
			propertyStore.seek(propertyStartOffset + KEY_OFFSET)
			key = propertyStore.read(4)

			# find value
			propertyStore.seek(propertyStartOffset + VALUE_OFFSET)
			value = propertyStore.read(4)

			# create property and add to node
			prop = Property(key, value, propertyFile)
			node.addProperty(prop)

			# find next property id
			propertyStore.seek(propertyStartOffset + NEXT_PROPERTY_ID_OFFSET)
			nextPropID = propertyStore.read(4)

        # read first label id
        nodeFile.seek(startOffset + Node.LABEL_STORE_PTR_OFFSET)
        firstLabelID = nodeFile.read(3)
        nextLabelID = firstLabelID

        while(nextLabelID != -1)
            # read label and add it to node
            labelStartOffset = nextLabelID * Label.storageSize
            labelFile.seek(labelStartOffset)
            label = labelFile.readLabel(nextLabelID)
            node.addLabel(label)

            # find next label id
            labelFile.seek(labelStartOffset + Label.NEXT_LABEL_ID_OFFSET)
            nextLabelID = labelFile.read(3)

		return node











		
