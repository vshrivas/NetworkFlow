from Node import Node
from NodePage import NodePage
from Property import Property
from Relationship import Relationship
from Label import Label
from NodeFile import NodeFile
from BufferManager import BufferManager
from RelationshipStorageManager import RelationshipStorageManager
from DataPage import DataPage
import sys, struct, os

# has metadata keeping track of number of node files
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


    # returns node, given nodeID
    def readNode(nodeID):
        pageID = nodeID[0]          # pageID[0] = 0, pageID[1] = pageIndex
        nodeIndex = nodeID[1]

        pageIndex = pageID[1]       # which page node is in, page IDs are unique across all files

        fileID = pageIndex / NodeFile.MAX_PAGES
        # use buffer manager to retrieve page from memory
        # will load page into memory if wasn't there

        print('getting node page for reading')
        nodePage = BufferManager.getNodePage(pageIndex, NodeFile(int(fileID)))

        nodePage.pageLock.acquire()

        node = nodePage.readNode(nodeIndex)

        firstRelID = node.firstRelID

        nodeRelationships = RelationshipStorageManager.getRelationshipChain(firstRelID, nodeIndex)
        '''nodeProperties = PropertyStorageManager.getPropChain(firstPropID)
        nodeLabels = LabelStorageManager.getLabelChain(firstLabelID)'''

        #print('node has {0} relationships'.format(len(nodeRelationships)))
        
        for rel in nodeRelationships:
            node.addRelationship(rel)
        #node.addProperties(nodeProperties)
        #node.addLabels(nodeLabels)

        nodePage.pageLock.release()

        return node

    # takes in a node object 
    def writeNode(node, create):
        """Writes this node to the node's node file according to the storage 
        format given in the class description and writes this node's relationships, 
        properties, and labels to the node's relationship file, property file, and 
        label file, respectively.
        """
        '''if DEBUG:
            print("properties in node")
            for prop in node.properties:
                print(prop.getID())

            print("labels in node:")
            for label in node.labels:
                print(label.getLabelID())

            print("writing node...")'''

        nodeID = node.getID()
        pageID = nodeID[0]          # pageID[0] = 0, pageID[1] = pageIndex

        pageIndex = pageID[1]       # which page node is in, page IDs are unique across all files

        fileID = pageIndex / NodeFile.MAX_PAGES

        print('getting node page for writing')
        nodePage = BufferManager.getNodePage(pageIndex, NodeFile(int(fileID)))

        nodePage.pageLock.acquire()

        if create:
            nodePage.numEntries += 1

        nodePage.writeNode(node, create)

        '''if DEBUG:
            print("writing relationships to relationship file ...")'''

        for rel in node.relationships:
            RelationshipStorageManager.writeRelationship(rel, False)
        
        '''if DEBUG:
            print("writing properties to property file ...")'''

        for prop in node.properties:
            PropertyStorageManager.writeProperty(prop, False)

        '''if DEBUG:
            print("writing labels to property file ...")'''

        for label in node.labels:
            LabelStorageManager.writeLabel(label, False)

        nodePage.pageLock.release()

        return node

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

        '''nodeFile = NodeFile(0)
        if nodeFile.numPages == 0:
            print('creating new page')
            nodeFile.createPage()

        print('getting node page for creation')
        nodePage = BufferManager.getNodePage(0, nodeFile)

        node = Node(nodeFile, nodePage, [[0, 0], nodePage.numEntries])
        print('creating node {0}'.format(nodePage.numEntries))

        NodeStorageManager.writeNode(node, True)

        return node'''

        node = Node(nodeFile, nodePage, [nodePage.pageID, nodePage.numEntries])
        
        print('creating node {0} in page {1}'.format(nodePage.numEntries, nodePage.pageID[1]))

        NodeStorageManager.writeNode(node, True)

        return node