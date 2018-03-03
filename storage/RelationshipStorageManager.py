class RelationshipStorageManager(StorageManager):
	def writeRelationships(relationships):
		# write relationships to relationship file
	    for relIndex in range(0, len(relationships)):
	        if DEBUG:
	            print("writing {0} relationship ".format(relIndex))
	        rel = relationships[relIndex]

	        # write first relationship
	        if relIndex == 0:
	            # A placeholder relationship in case there is no previous or next relationship
	            nullRelationship = Relationship(-1, -1, "", "",-1)
	            # no next relationship
	            if relIndex == len(relationships) - 1:
	                if DEBUG:
	                    print("only one relationship")
	                rel.writeRelationship(node, nullRelationship, nullRelationship)
	            # there is a next relationship
	            else:
	                nullRelationship = Relationship(-1, -1, "", "", -1)
	                rel.writeRelationship(node, nullRelationship, relationships[relIndex + 1])
	        # write last relationship
	        elif relIndex == len(relationships) - 1:
	            # A placeholder relationship in case there is no previous or next relationship
	            nullRelationship = Relationship(-1, -1, "", "", -1)
	            rel.writeRelationship(node, relationships[relIndex - 1], nullRelationship)
	        # write relationship that's not first or last relationship
	        else:
	            rel.writeRelationship(node, relationships[relIndex - 1],
	                relationships[relIndex + 1])

	# takes in a pageID and returns a file based on that 
	def openPageFile(pageID):
		pass

	def getRelationship(relId):
		pageID = relID[0]
        relIndex = relID[1]

        # find starting offset of relationship in relationship file
        relationshipStartOffset = relIndex * Relationship.storageSize + Relationship.relIDByteLen

        # open file relationship is stored in 
        relationshipStore = openPageFile(pageID)

		# find ID of first node in relationship
        relationshipStore.seek(relationshipStartOffset + Relationship.NODE1_ID_OFFSET)
        node1ID = int.from_bytes(relationshipStore.read(3), sys.byteorder, signed=True)

        # find ID of second node in relationship
        relationshipStore.seek(relationshipStartOffset + Relationship.NODE2_ID_OFFSET)
        node2ID = int.from_bytes(relationshipStore.read(3), sys.byteorder, signed=True)

        # read in type of relationship
        relationshipStore.seek(relationshipStartOffset + Relationship.RELATIONSHIP_TYPE_OFFSET)
        relType = relationshipStore.read(Relationship.MAX_TYPE_SIZE).decode("utf-8")
        relType = relType.rstrip(' ')

        if DEBUG:
            print('Node 1 id: {0}'.format(node1ID))
            print('Node 2 id: {0}'.format(node2ID))
            print('Relationship type: {0}'.format(relType))

        # create relationship and add to node
        rel = Relationship(node1ID, node2ID, relType, relationshipFile, relID)

	def getRelationshipChain(firstRelID):
		nextRelID = firstRelID

        if DEBUG:
            print("reading relationships")

        # while there is a next relationship
        while nextRelID != -1:
            if DEBUG:
                print(nextRelID)

            rel = getRelationship(nextRelID)

            #rel.relationshipID = nextRelID
            node.addRelationship(rel)

            # read in relationship properties
            # read in first property ID
            relationshipStore.seek(relationshipStartOffset + Relationship.PROPERTY_ID_OFFSET)
            firstRelPropID = int.from_bytes(relationshipStore.read(Property.propIDByteLen), sys.byteorder, signed=True)

            nextRelPropID = firstRelPropID
            if DEBUG:
                print ('Reading in properties for rel {0}...'.format(nextRelID))

			rel.addProperties(PropertyStorageManager.getPropertyChain())           

            # find next rel ID
            if nodeID == node1ID:
                relationshipStore.seek(relationshipStartOffset + Relationship.NODE1_NEXT_REL_ID_OFFSET)
                nextRelID = int.from_bytes(relationshipStore.read(4), sys.byteorder, signed=True)

            else:
                relationshipStore.seek(relationshipStartOffset + Relationship.NODE2_NEXT_REL_ID_OFFSET)
                nextRelID = int.from_bytes(relationshipStore.read(4), sys.byteorder, signed=True)
	
