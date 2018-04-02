from .RelationshipFile import RelationshipFile
from .Relationship import Relationship
from .BufferManager import BufferManager
from .Node import Node
from .Property import Property
from .DataPage import DataPage
from .LockManager import LockManager
import threading
import sys, struct, os

''' RelationshipStorageManager is responsible for handling the top level methods for creating, reading,
and writing relationships. Creates new relationship pages and files when necessary. Has a meta data file
to keep track of number of relationship file. '''
class RelationshipStorageManager():
    directory = "relstore"

    numRelFiles = 0

    def __init__(self):
        # open relationship storage meta data file
        self.fileName = "metadata"
        self.filePath = os.path.join(RelationshipStorageManager.directory, self.fileName)

        # file exists, read number of relationship files 
        if os.path.exists(self.filePath):
            metadataFile = open(self.filePath, 'r+b')
            RelationshipStorageManager.numRelFiles = int.from_bytes(metadataFile.read(Relationship.relIDByteLen), sys.byteorder, signed=True)

        else:
            # rel store directory does not exist, make it
            if not os.path.exists(self.directory):
                os.makedirs(RelationshipStorageManager.directory)

            # create and open metadata file    
            metadataFile = open(self.filePath, 'wb')
            # write number of rel files 
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

    ''' Takes in a relationship ID and returns the corresponding relationship by reading it from the DB '''
    def readRelationship(relID):
        # get relationship and page indexes
        pageID = relID[0]
        relIndex = relID[1]
        pageIndex = pageID[1]

        # get file ID
        fileID = int(pageIndex / RelationshipFile.MAX_PAGES)

        # use buffer manager to retrieve page from memory
        # will load page into memory if wasn't there
        relationshipPage = BufferManager.getRelationshipPage(pageIndex, RelationshipFile(fileID))

        # thread is waiting on lock
        threading.currentThread().waiting = relationshipPage
        # check for deadlock
        if LockManager.detectRWDeadlock(threading.currentThread(), threading.currentThread()):
            raise Exception('Deadlock detected!')
        # acquire lock
        relationshipPage.pageLock.acquire_read()
        threading.currentThread().waiting = None
        LockManager.makePageOwner(threading.currentThread(), relationshipPage)

        rel = relationshipPage.readRelationship(relIndex)

        # release lock
        relationshipPage.pageLock.release_read()
        LockManager.removePageOwner(threading.currentThread(), relationshipPage)
        return rel

    ''' Takes in a relationship and either creates a new rel, or replaces the one with this ID '''
    def writeRelationship(rel, create):
        # get relationship and page indexes
        relID = rel.getID()
        pageID = relID[0]           # pageID[0] = 0, pageID[1] = pageIndex
        pageIndex = pageID[1]       

        # get page ID
        fileID = int(pageIndex / RelationshipFile.MAX_PAGES)

        relPage = BufferManager.getRelationshipPage(pageIndex, RelationshipFile(fileID))

        threading.currentThread().waiting = relPage
        # check for deadlock
        if LockManager.detectRWDeadlock(threading.currentThread(), threading.currentThread()):
            raise Exception('Deadlock detected!')

        # acquire lock
        relPage.pageLock.acquire_write()
        threading.currentThread().waiting = None
        LockManager.makePageOwner(threading.currentThread(), relPage)

        if create:
            relPage.numEntries += 1

        relPage.writeRelationship(rel, create)

        # release lock
        relPage.pageLock.release_write()
        LockManager.removePageOwner(threading.currentThread(), relPage)
        return rel

    ''' Takes in both nodes of relationship and relationship type, creates the relationship in the DB '''
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

        # make relationship
        relID = [relPage.pageID, relPage.numEntries]

        rel = Relationship(relID, node0.getID(), node1.getID(),
            [[1,0],-1], [[1,0],-1], [[1,0],-1], [[1,0],-1], type, [[2,0],-1], relFile)

        print('creating relationship {0} in page {1}'.format(relPage.numEntries, relPage.pageID[1]))

        RelationshipStorageManager.writeRelationship(rel, True)

        return rel

    ''' Takes in first relationship ID for a given node and finds full chain of relationships for node'''
    def getRelationshipChain(firstRelID, nodeIndex):
        relationshipChain = []

        nextRelID = firstRelID

        print('first rel ID for node is {0}'.format(firstRelID))

        # while there is a next relationship
        while nextRelID[1] != -1:
            print('inside get rel chain loop')

            # read relationship
            rel = RelationshipStorageManager.readRelationship(nextRelID)        

            # find next rel ID
            if nodeIndex == rel.firstNodeID[1]:
                nextRelID = rel.node1NextRelID

            else:
                nextRelID = rel.node2NextRelID

            relationshipChain.append(rel)

        return relationshipChain