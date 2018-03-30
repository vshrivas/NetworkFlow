from .Node import Node
from .NodePage import NodePage
from .Property import Property
from .Relationship import Relationship
from .Label import Label
import sys, struct, os

# has metadata keeping track of number of node files
class NodeStorageManager(StorageManager):
	numNodeFiles = 0
	directory = "nodestore"

	def __init__(self):
		# open node storage meta data file
		# read number of node files 
		self.fileName = "metadata"
		self.filePath = os.path.join(NodeStorageManager.directory, self.fileName)

		if os.path.exists(self.filePath):
            metadataFile = open(self.filePath, 'r+b')
            numNodeFiles = int.from_bytes(metadataFile.read(Node.nodeIDByteLen), sys.byteorder, signed=True)

        else:
            metadataFile = open(self.filePath, 'wb')
            # write number of node files to first 3 bytes of node storage metadata file
            metadataFile.write((0).to_bytes(Node.nodeIDByteLen,
                byteorder = sys.byteorder, signed=True))

        if numNodeFiles == 0:
        	NodeFile(0)


	# returns node, given nodeID
	def readNode(nodeID):
		pageID = nodeID[0] 			# pageID[0] = 0, pageID[1] = pageIndex
		nodeIndex = nodeID[1]

		pageIndex = pageID[1]		# which page node is in, page IDs are unique across all files

		# use buffer manager to retrieve page from memory
		# will load page into memory if wasn't there
        nodePage = BufferManager.getNodePage(pageIndex, self)
        return nodePage.readNode(nodeIndex)

	# takes in a node object 
	def writeNode(node):
        """Writes this node to the node's node file according to the storage 
        format given in the class description and writes this node's relationships, 
        properties, and labels to the node's relationship file, property file, and 
        label file, respectively.
        """
        if DEBUG:
            print("properties in node")
            for prop in node.properties:
                print(prop.getID())

            print("labels in node:")
            for label in node.labels:
                print(label.getLabelID())

            print("writing node...")

        nodeID = node.getNodeID()
        pageID = nodeID[0] 			# pageID[0] = 0, pageID[1] = pageIndex

		pageIndex = pageID[1]		# which page node is in, page IDs are unique across all files

		nodePage = BufferManager.getNodePage(pageIndex, self)

		nodePage.writeNode(node)

        if DEBUG:
            print("writing relationships to relationship file ...")

        for rel in node.relationships:
        	RelationshipStoreManager.writeRelationship(rel)
        
        if DEBUG:
            print("writing properties to property file ...")

        for prop in node.properties:
        	PropertyStoreManager.writeProperty(prop)

        if DEBUG:
            print("writing labels to property file ...")

        for label in node.labels:
        	LabelStoreManager.writeLabel(label)

	def createNode():
		nodePage = BufferManager.getNodePage(0, self)

		nodeFile = NodeFile(0)
		node = Node(nodeFile, nodePage, nodePage.numEntries)

		nodePage.numEntries += 1

		writeNode(node)