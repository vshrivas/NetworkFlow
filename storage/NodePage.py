from Node import Node
from Property import Property
from Relationship import Relationship
from Label import Label
from DataPage import DataPage
import sys, struct, os

class NodePage(DataPage):
    ENTRY_SIZE = Node.storageSize
    PAGES_OFFSET = 100

    # constructor for NodePage
    # takes in 
    # pageIndex: index of page (unique across nodeFiles)
    # datafile: nodeFile containing page
    def __init__(self, pageIndex, datafile, create):
        # 0 indicates that this is a node page
        pageID = [0, pageIndex]
        super().__init__(pageID, datafile)

        self.nodeData = []  # list of node objects the page contains

        self.pageStart = self.getPageIndex() * (self.MAX_PAGE_ENTRIES * Node.storageSize) + self.PAGES_OFFSET

        if create == False:
          # read in all page data
            self.readPageData()
        else:
            self.writePageData()

    def readPageData(self):
        filePath = (self.file).getFilePath()
        nodeFile = open(filePath, 'rb')

        print('reading file {0}'.format(filePath))

        # read in number of entries
        nodeFile.seek(self.pageStart + DataPage.NUM_ENTRIES_OFFSET)
        self.numEntries = int.from_bytes(nodeFile.read(DataPage.NUM_ENTRIES_SIZE), sys.byteorder, signed=True)
        print('reading num entries as {0} at {1}'.format(self.numEntries, (self.pageStart + DataPage.NUM_ENTRIES_OFFSET)))

        # read in owner of page
        nodeFile.seek(self.pageStart + DataPage.OWNER_ID_OFFSET)
        self.ownerID = int.from_bytes(nodeFile.read(DataPage.OWNER_ID_SIZE), sys.byteorder, signed=True)
        print('reading owner ID as {0} at {1}'.format(self.ownerID, (self.pageStart + DataPage.OWNER_ID_OFFSET)))

        # read in all data items
        for nodeIndex in range(0, self.numEntries):
            node = self.readNodeData(nodeIndex)
            self.nodeData.append(node)

        nodeFile.close()

    def readNode(self, nodeIndex):
        return self.nodeData[nodeIndex]

    # reads in node from page in file, using nodeIndex 
    # used when loading page data into memory
    # takes in nodeIndex
    # returns node
    def readNodeData(self, nodeIndex):
        filePath = (self.file).getFilePath()
        nodeFile = open(filePath, 'rb')

        nodeStartOffset = self.pageStart + self.DATA_OFFSET + nodeIndex * Node.storageSize
        
        # read first rel ID, first property ID, first label ID
        nodeFile.seek(nodeStartOffset + Node.REL_ID_OFFSET)
        firstRelID = int.from_bytes(nodeFile.read(Node.nodeIDByteLen), sys.byteorder, signed=True)

        nodeFile.seek(nodeStartOffset + Node.PROPERTY_ID_OFFSET)
        firstPropID = int.from_bytes(nodeFile.read(Property.propIDByteLen), sys.byteorder, signed=True)

        nodeFile.seek(nodeStartOffset + Node.LABEL_ID_OFFSET)
        firstLabelID = int.from_bytes(nodeFile.read(Label.labelIDByteLen), sys.byteorder, signed=True)

        nodeAttributes = [firstRelID, firstPropID, firstLabelID]

        node = Node(self.file, self, [self.pageID, nodeIndex])

        return node

    # called by node storage manager
    # sets the node as the new node in node data
    # then calls writeNode to sync page data to disk
    def writeNode(self, node, create):
        nodeID = node.getID()

        nodeIndex = nodeID[1]

        if create:
            self.nodeData.append(node)
        else:
            self.nodeData[nodeIndex] = node

        self.writePageData()

    # syncs all page data to disk
    def writePageData(self):
        filePath = (self.file).getFilePath()
        nodeFile = open(filePath, 'r+b')

        print('writing file {0}'.format(filePath))
        print('writing page data...')

        # write number of entries
        nodeFile.seek(self.pageStart + DataPage.NUM_ENTRIES_OFFSET)

        print('writing num entries as {0} at {1}'.format(self.numEntries, self.pageStart + DataPage.NUM_ENTRIES_OFFSET))
        nodeFile.write((self.numEntries).to_bytes(DataPage.NUM_ENTRIES_SIZE,
            byteorder = sys.byteorder, signed=True))

        # write owner ID
        nodeFile.seek(self.pageStart + DataPage.OWNER_ID_OFFSET)

        print('writing owner ID as {0} at {1}'.format(self.ownerID, (self.pageStart + DataPage.OWNER_ID_OFFSET)))
        nodeFile.write((self.ownerID).to_bytes(DataPage.OWNER_ID_SIZE,
            byteorder = sys.byteorder, signed=True))

        print('writing all nodes...')
        for node in self.nodeData:
            print('writing node {0}'.format(node.getID()[1]))
            self.writeNodeData(node.getID()[1], nodeFile)

        nodeFile.close()

    # syncs node data to disk
    def writeNodeData(self, nodeIndex, storeFile):
        node = self.nodeData[nodeIndex]

        #if DEBUG:
            #print("opened store file: {0}". format(storeFileName))

        nodeStartOffset = self.pageStart + DataPage.DATA_OFFSET + nodeIndex * Node.storageSize

        # write node id
        storeFile.seek(nodeStartOffset + Node.NODE_ID_OFFSET)
        storeFile.write((node.nodeID[1]).to_bytes(Node.nodeIDByteLen,
            byteorder = sys.byteorder, signed=True))

        #if DEBUG:
            #print("wrote node ID: {0}". format(node.nodeID))

        # write in-use flag
        storeFile.seek(nodeStartOffset + Node.IN_USE_FLAG_OFFSET)
        storeFile.write((1).to_bytes(1, byteorder = sys.byteorder, signed=True))

        #if DEBUG:
            #print("wrote in-use flag: {0}". format(1))

        # write first relationship ID
        storeFile.seek(nodeStartOffset + Node.REL_ID_OFFSET)
        # if there are no relationships, write -1 as first relationship ID
        if len(node.relationships) == 0:
            firstRel = -1
            storeFile.write((-1).to_bytes(Relationship.relIDByteLen,
                byteorder = sys.byteorder, signed=True))
            #if DEBUG:
                #print("wrote first rel ID: -1")
        # otherwise, write first relationship ID
        else:
            firstRel = node.relationships[0]
            storeFile.write(firstRel.getID().to_bytes(Relationship.relIDByteLen,
                byteorder = sys.byteorder, signed=True))
            #if DEBUG:
                #print("wrote first rel ID: {0}". format(firstRel.getID()))

        # write first property ID
        storeFile.seek(nodeStartOffset + Node.PROPERTY_ID_OFFSET)
        # if there are no properties, write -1 as first property ID
        if len(node.properties) == 0:
            firstProp = -1
            storeFile.write((-1).to_bytes(Property.propIDByteLen,
                byteorder = sys.byteorder, signed=True))
            #if DEBUG:
                #print("wrote first property ID: -1")
        # otherwise, write first property ID
        else:
            firstProp = node.properties[0]
            storeFile.write(firstProp.getID().to_bytes(Property.propIDByteLen,
                byteorder = sys.byteorder, signed=True))
            #if DEBUG:
                #print("wrote first property ID: {0}". format(firstProp.getID()))

        # write first label ID
        storeFile.seek(nodeStartOffset + Node.LABEL_ID_OFFSET)
        # if there are no labels, write -1 as first label ID
        if len(node.labels) == 0:
            storeFile.write((-1).to_bytes(Label.LABEL_OFFSET,
                byteorder = sys.byteorder, signed=True))
        # otherwise, write first label ID
        else:
            firstLabel = node.labels[0]
            storeFile.write(firstLabel.getLabelID().to_bytes(Label.LABEL_OFFSET,
                byteorder = sys.byteorder, signed=True))

    def createNode(self):
        # create a new node object
        newNode = Node()
