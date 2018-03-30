from Node import Node
from NodePage import NodePage
from Property import Property
from Relationship import Relationship
from Label import Label
from NodeFile import NodeFile
from BufferManager import BufferManager
import sys, struct, os

# has metadata keeping track of number of node files
class NodeStorageManager():
    numNodeFiles = 0
    directory = "nodestore"

    DEBUG = False

    def __init__(self):
        # open node storage meta data file
        # read number of node files 
        self.fileName = "nodestore_metadata"
        self.filePath = os.path.join(NodeStorageManager.directory, self.fileName)

        # storage manager metadata file exists
        if os.path.exists(self.filePath):
            metadataFile = open(self.filePath, 'r+b')
            numNodeFiles = int.from_bytes(metadataFile.read(Node.nodeIDByteLen), sys.byteorder, signed=True)

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

        if NodeStorageManager.numNodeFiles == 0:
            NodeFile(0)
            NodeStorageManager.numNodeFiles += 1

            metadataFile = open(self.filePath, 'wb')
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
        nodePage = BufferManager.getNodePage(pageIndex, NodeFile(fileID))
        return nodePage.readNode(nodeIndex)

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

        nodePage = BufferManager.getNodePage(pageIndex, NodeFile(fileID))

        if create:
            nodePage.numEntries += 1

        nodePage.writeNode(node, create)

        '''if DEBUG:
            print("writing relationships to relationship file ...")'''

        for rel in node.relationships:
            RelationshipStoreManager.writeRelationship(rel)
        
        '''if DEBUG:
            print("writing properties to property file ...")'''

        for prop in node.properties:
            PropertyStoreManager.writeProperty(prop)

        '''if DEBUG:
            print("writing labels to property file ...")'''

        for label in node.labels:
            LabelStoreManager.writeLabel(label)

    def createNode():
        nodeFile = NodeFile(0)

        nodePage = BufferManager.getNodePage(0, nodeFile)

        node = Node(nodeFile, nodePage, [[0, 0], nodePage.numEntries])

        NodeStorageManager.writeNode(node, True)

        return node