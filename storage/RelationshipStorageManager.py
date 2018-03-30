class RelationshipStorageManager(StorageManager):
	nodeFiles = []
	metaDataPath = "datastore"
	def __init__(self):
		# open node storage meta data file
		# read number of node files 
		# create file objects for each of the node files, and make a list of these

	def readRelationship(relId):
		pageID = relID[0]
        relIndex = relID[1]

        pageIndex = pageID[1]

        # use buffer manager to retrieve page from memory
		# will load page into memory if wasn't there
        relationshipPage = BufferManager.getRelationshipPage(pageIndex, self)
        return relationshipPage.readRelationship(nodeIndex)

    def writeRelationship(rel):
    	reID = rel.getRelID()
        pageID = relID[0] 			# pageID[0] = 0, pageID[1] = pageIndex

		pageIndex = relID[1]		# which page node is in, page IDs are unique across all files

		relPage = BufferManager.getRelationshipPage(pageIndex, self)

		relPage.writeRelationship(rel)

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


    # triggers writes for every page of these relationships
    '''def writeRelationships(relationships):
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
	                relationships[relIndex + 1])'''

	
