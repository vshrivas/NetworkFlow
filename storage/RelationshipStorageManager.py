from RelationshipFile import RelationshipFile
from Relationship import Relationship
from BufferManager import BufferManager
from Node import Node
from Property import Property
from DataPage import DataPage
import sys, struct, os

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
            RelationshipStorageManager.numRelFiles = int.from_bytes(metadataFile.read(Relationship.relIDByteLen), sys.byteorder, signed=True)

        else:
            # rel store directory does not exist, make it
            if not os.path.exists(self.directory):
                os.makedirs(RelationshipStorageManager.directory)

            # open metadata file    
            metadataFile = open(self.filePath, 'wb')
            # write number of rel files to first 3 bytes of rel storage metadata file
            metadataFile.write((0).to_bytes(Relationship.relIDByteLen,
                byteorder = sys.byteorder, signed=True))

        # there are no rel files
        if RelationshipStorageManager.numRelFiles == 0:
            # make a new one 
            RelationshipFile(0)
            RelationshipStorageManager.numRelFiles += 1

            metadataFile = open(self.filePath, 'r+b')
            metadataFile.write((RelationshipStorageManager.numRelFiles).to_bytes(Relationship.relIDByteLen,
                byteorder = sys.byteorder, signed=True))

    def readRelationship(relID):
        pageID = relID[0]
        relIndex = relID[1]

        pageIndex = pageID[1]

        fileID = int(pageIndex / RelationshipFile.MAX_PAGES)

        # use buffer manager to retrieve page from memory
        # will load page into memory if wasn't there
        relationshipPage = BufferManager.getRelationshipPage(pageIndex, RelationshipFile(fileID))

        relationshipPage.pageLock.acquire_read()

        rel = relationshipPage.readRelationship(relIndex)

        '''properties = getPropertyChain(rel.propertyID)

        rel.properties = properties'''

        relationshipPage.pageLock.release_read()

        return rel

    def writeRelationship(rel, create):
        relID = rel.getID()
        pageID = relID[0]           # pageID[0] = 0, pageID[1] = pageIndex

        pageIndex = pageID[1]       # which page node is in, page IDs are unique across all files

        fileID = int(pageIndex / RelationshipFile.MAX_PAGES)

        relPage = BufferManager.getRelationshipPage(pageIndex, RelationshipFile(fileID))

        relPage.pageLock.acquire_write()

        if create:
            relPage.numEntries += 1

        relPage.writeRelationship(rel, create)

        relPage.pageLock.release_write()

        '''for prop in node.properties:
            PropertyStoreManager.writeProperty(prop)'''
        return rel

    def createRelationship(node0, node1, type):
        # get rel file
        lastFileID = RelationshipStorageManager.numRelFiles - 1
        lastFile = RelationshipFile(lastFileID)

        if lastFile.numPages == 0:
            lastFile.createPage()

        # get last rel page
        lastPage = BufferManager.getRelationshipPage(lastFile.numPages - 1, lastFile)
        
        relPage = lastPage
        relFile = lastFile

        # if last page is full
        if lastPage.numEntries == DataPage.MAX_PAGE_ENTRIES:
            # if file is at max pages
            if lastFile.numPages == RelationshipFile.MAX_PAGES:
                # make a new file
                newLastFile = RelationshipFile(lastFileID + 1)
                RelationshipStorageManager.numRelFiles += 1

                metadataFile = open(self.filePath, 'r+b')
                metadataFile.write((RelationshipStorageManager.numNodeFiles).to_bytes(Relationship.relIDByteLen,
                byteorder = sys.byteorder, signed=True))

                relFile = newLastFile

                # make a new page in the file
                newLastFile.createPage()
                relPage = BufferManager.getRelationshipPage(newLastFile.numPages - 1, newLastFile)

            # else make new page
            else:
                lastFile.createPage()
                relPage = BufferManager.getRelationshipPage(lastFile.numPages - 1, lastFile)
        '''relFile = RelationshipFile(0)

        if relFile.numPages == 0:
            relFile.createPage()

        print('getting rel page for creation')
        relPage = BufferManager.getRelationshipPage(0, relFile)

        relID = [[1, 0], relPage.numEntries]

        rel = Relationship(relID, node0.getID(), node1.getID(),
            [[1,0],-1], [[1,0],-1], [[1,0],-1], [[1,0],-1], type, [[2,0],-1], relFile)

        print('creating relationship {0}'.format(relPage.numEntries))

        RelationshipStorageManager.writeRelationship(rel, True)

        return rel'''

        relID = [relPage.pageID, relPage.numEntries]

        rel = Relationship(relID, node0.getID(), node1.getID(),
            [[1,0],-1], [[1,0],-1], [[1,0],-1], [[1,0],-1], type, [[2,0],-1], relFile)

        print('creating relationship {0} in page {1}'.format(relPage.numEntries, relPage.pageID[1]))

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

    
