from RelationshipFile import RelationshipFile
from Relationship import Relationship
from BufferManager import BufferManager
from Node import Node
from Property import Property

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

        fileID = int(pageIndex / RelationshipFile.MAX_PAGES)

        # use buffer manager to retrieve page from memory
        # will load page into memory if wasn't there
        relationshipPage = BufferManager.getRelationshipPage(pageIndex, RelationshipFile(fileID))
        rel = relationshipPage.readRelationship(relIndex)

        '''properties = getPropertyChain(rel.propertyID)

        rel.properties = properties'''

        return rel

    def writeRelationship(rel, create):
        relID = rel.getID()
        pageID = relID[0]           # pageID[0] = 0, pageID[1] = pageIndex

        pageIndex = pageID[1]       # which page node is in, page IDs are unique across all files

        fileID = int(pageIndex / RelationshipFile.MAX_PAGES)

        relPage = BufferManager.getRelationshipPage(pageIndex, RelationshipFile(fileID))

        if create:
            relPage.numEntries += 1

        relPage.writeRelationship(rel, create)

        '''for prop in node.properties:
            PropertyStoreManager.writeProperty(prop)'''

    def createRelationship(node0, node1, type):
        relFile = RelationshipFile(0)

        if relFile.numPages == 0:
            relFile.createPage()

        print('getting rel page for creation')
        relPage = BufferManager.getRelationshipPage(0, relFile)

        relID = [[1, 0], relPage.numEntries]

        rel = Relationship(relID, node0.getID(), node1.getID(),
            [[1,0],-1], [[1,0],-1], [[1,0],-1], [[1,0],-1], type, [[2,0],-1], relFile)

        print('creating relationship {0}'.format(relPage.numEntries))

        RelationshipStorageManager.writeRelationship(rel, True)

        return rel

    def getRelationshipChain(firstRelID, nodeIndex):
        relationshipChain = []

        nextRelID = firstRelID

        print('first rel ID for node is {0}'.format(firstRelID))

        '''if DEBUG:
            print("reading relationships")'''

        # while there is a next relationship
        while nextRelID[1] != -1:
            '''if DEBUG:
                print(nextRelID)'''
            print('inside get rel chain loop')
            rel = RelationshipStorageManager.readRelationship(nextRelID)        

            # find next rel ID
            if nodeIndex == rel.firstNodeID[1]:
                nextRelID = rel.node1NextRelID

            else:
                nextRelID = rel.node2NextRelID

            relationshipChain.append(rel)

        return relationshipChain


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

    
