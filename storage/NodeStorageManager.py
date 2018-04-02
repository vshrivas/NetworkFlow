from .Node import Node
from .NodePage import NodePage
from .Property import Property
from .Relationship import Relationship
from .Label import Label
from .NodeFile import NodeFile
from .BufferManager import BufferManager
from .RelationshipStorageManager import RelationshipStorageManager
from .DataPage import DataPage
from .LockManager import LockManager
import threading
import sys, struct, os

''' NodeStorageManager is responsible for handling the top level methods for creating, reading,
and writing of node. Creates new node pages and files when necessary. Has a meta data file
to keep track of number of node files. '''
class NodeStorageManager():
    numNodeFiles = 0
    directory = "nodestore"

    DEBUG = False

    def __init__(self):
        # open node storage meta data file
        # read number of node files 
        self.fileName = "metadata"
        self.filePath = os.path.join(NodeStorageManager.directory, self.fileName)

        # storage manager metadata file exists
        if os.path.exists(self.filePath):
            metadataFile = open(self.filePath, 'r+b')
            NodeStorageManager.numNodeFiles = int.from_bytes(metadataFile.read(Node.nodeIDByteLen), sys.byteorder, signed=True)

        # storage manager metadata file does not exist
        else:
            # node store directory does not exist, make it
            if not os.path.exists(self.directory):
                os.makedirs(NodeStorageManager.directory)

            # open metadata file    
            metadataFile = open(self.filePath, 'wb')
            # write number of node files to first 3 bytes of node storage metadata file
            metadataFile.write((0).to_bytes(Node.nodeIDByteLen,
                byteorder = sys.byteorder, signed=True))

        # there are no node files
        if NodeStorageManager.numNodeFiles == 0:
            # make a new one 
            NodeFile(0)
            NodeStorageManager.numNodeFiles += 1

            metadataFile = open(self.filePath, 'r+b')
            metadataFile.write((NodeStorageManager.numNodeFiles).to_bytes(Node.nodeIDByteLen,
                byteorder = sys.byteorder, signed=True))


    # Takes in nodeID, read corresponding node from DB and returns
    def readNode(nodeID):
        pageID = nodeID[0]          # pageID[0] = 0, pageID[1] = pageIndex
        nodeIndex = nodeID[1]

        pageIndex = pageID[1]       # which page node is in, page IDs are unique across all files

        fileID = pageIndex / NodeFile.MAX_PAGES
       
        # use buffer manager to retrieve page from memory
        # will load page into memory if wasn't there
        print('getting node page for reading')
        nodePage = BufferManager.getNodePage(pageIndex, NodeFile(int(fileID)))

        # check for potential deadlock
        threading.currentThread().waiting = nodePage
        if LockManager.detectRWDeadlock(threading.currentThread(), threading.currentThread()):
            raise Exception('Deadlock detected!')

        # acquire read lock
        nodePage.pageLock.acquire_read()
        threading.currentThread().waiting = None
        LockManager.makePageOwner(threading.currentThread(), nodePage)

        node = nodePage.readNode(nodeIndex)

        firstRelID = node.firstRelID

        # get chain of relationships for node
        nodeRelationships = RelationshipStorageManager.getRelationshipChain(firstRelID, nodeIndex)
        
        for rel in nodeRelationships:
            node.addRelationship(rel)

        # release lock
        nodePage.pageLock.release_read()
        LockManager.removePageOwner(threading.currentThread(), nodePage)
        return node

    # takes in a node object to write or create, and returns when done 
    def writeNode(node, create):
        nodeID = node.getID()
        pageID = nodeID[0]          # pageID[0] = 0, pageID[1] = pageIndex

        pageIndex = pageID[1]       # which page node is in, page IDs are unique across all files

        fileID = pageIndex / NodeFile.MAX_PAGES

        print('getting node page for writing')

        # get page from buffer
        nodePage = BufferManager.getNodePage(pageIndex, NodeFile(int(fileID)))

        # check for deadlock
        threading.currentThread().waiting = nodePage
        if LockManager.detectRWDeadlock(threading.currentThread(), threading.currentThread()):
            raise Exception('Deadlock detected!')

        # acquire write lock
        nodePage.pageLock.acquire_write()
        threading.currentThread().waiting = None
        LockManager.makePageOwner(threading.currentThread(), nodePage)

        if create:
            nodePage.numEntries += 1

        nodePage.writeNode(node, create)

        # write rels, props, and labels of node to their files
        for rel in node.relationships:
            RelationshipStorageManager.writeRelationship(rel, False)

        for prop in node.properties:
            PropertyStorageManager.writeProperty(prop, False)

        for label in node.labels:
            LabelStorageManager.writeLabel(label, False)

        nodePage.pageLock.release_write()
        LockManager.removePageOwner(threading.currentThread(), nodePage)

        return node

    # creates a new node and returns it
    def createNode():
        print('***creating node****')

        # get node file
        lastFileID = NodeStorageManager.numNodeFiles - 1
        lastFile = NodeFile(lastFileID)

        if lastFile.numPages == 0:
            lastFile.createPage()

        # get last node page
        lastPage = BufferManager.getNodePage(lastFile.numPages - 1, lastFile)
        
        nodePage = lastPage
        nodeFile = lastFile

        # if last page is full
        if lastPage.numEntries == DataPage.MAX_PAGE_ENTRIES:
            # if file is at max pages
            if lastFile.numPages == NodeFile.MAX_PAGES:
                # make a new file
                newLastFile = NodeFile(lastFileID + 1)
                NodeStorageManager.numNodeFiles += 1

                metadataFile = open(self.filePath, 'r+b')
                metadataFile.write((NodeStorageManager.numNodeFiles).to_bytes(Node.nodeIDByteLen,
                byteorder = sys.byteorder, signed=True))

                nodeFile = newLastFile

                # make a new page in the file
                newLastFile.createPage()
                nodePage = BufferManager.getNodePage(newLastFile.numPages - 1, newLastFile)

            # else make new page
            else:
                lastFile.createPage()
                nodePage = BufferManager.getNodePage(lastFile.numPages - 1, lastFile)

        # create node object
        node = Node(nodeFile, nodePage, [nodePage.pageID, nodePage.numEntries])
        
        print('creating node {0} in page {1}'.format(nodePage.numEntries, nodePage.pageID[1]))

        # write node object
        NodeStorageManager.writeNode(node, True)

        return node