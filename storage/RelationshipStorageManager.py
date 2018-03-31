class RelationshipStorageManager():
    nodeFiles = []
    directory = "relstore"

    numRelFiles = 0

    def __init__(self):
        # open relationship storage meta data file
        # read number of relationship files 
        self.fileName = "metadata"
        self.filePath = os.path.join(RelationshipStorageManager.directory, self.fileName)

        if os.path.exists(self.filePath):
            metadataFile = open(self.filePath, 'r+b')
            numRelFiles = int.from_bytes(metadataFile.read(Relationship.relIDByteLen), sys.byteorder, signed=True)

        else:
            metadataFile = open(self.filePath, 'wb')
            # write number of rel files to first 3 bytes of rel storage metadata file
            metadataFile.write((0).to_bytes(Relationship.relIDByteLen,
                byteorder = sys.byteorder, signed=True))

        if numRelFiles == 0:
            RelationshipFile(0)

    def readRelationship(relID):
        pageID = relID[0]
        relIndex = relID[1]

        pageIndex = pageID[1]

        # use buffer manager to retrieve page from memory
        # will load page into memory if wasn't there
        relationshipPage = BufferManager.getRelationshipPage(pageIndex, self)
        rel = relationshipPage.readRelationship(nodeIndex)

        properties = getPropertyChain(rel.propertyID)

        rel.properties = properties

        return rel

    def writeRelationship(rel):
        relID = rel.getRelID()
        pageID = relID[0]           # pageID[0] = 0, pageID[1] = pageIndex

        pageIndex = pageID[1]       # which page node is in, page IDs are unique across all files

        relPage = BufferManager.getRelationshipPage(pageIndex, self)

        relPage.writeRelationship(rel)

        if DEBUG:
            print("writing properties to property pages ...")

        for prop in node.properties:
            PropertyStoreManager.writeProperty(prop)

    def createRelationship():
        nodeFile = NodeFile(0)
        print('getting node page for creation')
        nodePage = BufferManager.getNodePage(0, nodeFile)

        node = Node(nodeFile, nodePage, [[0, 0], nodePage.numEntries])
        print('creating node {0}'.format(nodePage.numEntries))

        NodeStorageManager.writeNode(node, True)

        return node

    def getRelationshipChain(firstRelID, nodeIndex):
        nextRelID = firstRelID

        '''if DEBUG:
            print("reading relationships")'''

        # while there is a next relationship
        while nextRelID[1] != -1:
            '''if DEBUG:
                print(nextRelID)'''

            rel = RelationshipStorageManager.readRelationship(nextRelID)

            #rel.relationshipID = nextRelID
            node.addRelationship(rel)         

            # find next rel ID
            if nodeIndex == node1ID[1]:
                nextRelID = rel.node1NextRelID

            else:
                nextRelID = rel.node2NextRelID


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

    
