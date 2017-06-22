""" 
Storage
Bytes 1-100: Label string
Bytes 101-103: number of nodes
Bytes 104-109: average number of connections (double)
Bytes 110-...: IDs of nodes in index (3 bytes each)
"""
import sys, os

# label indexes have node IDs of nodes which have the given label
class LabelIndex:
    # offsets from start of index
    LABEL_STRING_OFFSET = 0
    NUM_NODES_OFFSET = 100
    NUM_CONNECTIONS_OFFSET = 103
    NODE_IDS_OFFSET = 109

    numConnectionsByteLen = 6
    nodeIDByteLen = 3

    def __init__(self, labelStr):
        self.labelStr = labelStr.strip()
        # create index file if it doesn't already exist
        self.fileName = "{0}.labelindex".format(self.labelStr)
        self.dir = "datafiles"
        self.filePath = os.path.join(self.dir, self.fileName)

        # open index file
        if os.path.exists(self.filePath):
            indexFile = open(self.filePath, 'r+b')
            print("opened label index for {0}".format(self.labelStr))

        else:
            print("created label index for {0}".format(self.labelStr))
            indexFile = open(self.filePath, 'wb')
            # label string
            indexFile.write(bytearray(self.labelStr, "utf8"))
            # write number of nodes to next 3 bytes of index file
            indexFile.write((0).to_bytes(self.nodeIDByteLen,
                byteorder = sys.byteorder, signed=True))
            # write number of nodes to next 3 bytes of index file
            indexFile.write((0).to_bytes(self.nodeIDByteLen,
                byteorder = sys.byteorder, signed=True))
        indexFile.close()

    # this function adds a node id to the given index
    def addNode(self, nodeID):
        # increment number of nodes
        print("adding node to index")
        indexFile = open(self.filePath, 'r+b') # open node index
        indexFile.seek(self.NUM_NODES_OFFSET)
        numNodes = int.from_bytes(indexFile.read(self.nodeIDByteLen), sys.byteorder, signed=True)
        print("{0} nodes in index rn".format(numNodes))

        indexFile.seek(self.NUM_NODES_OFFSET)
        indexFile.write((numNodes + 1).to_bytes(self.nodeIDByteLen,
            byteorder = sys.byteorder, signed=True))

        indexFile.seek(self.NUM_NODES_OFFSET)
        newNumNodes = int.from_bytes(indexFile.read(self.nodeIDByteLen), sys.byteorder, signed=True)
        print("{0} nodes in index after".format(newNumNodes))

        # update average number of connections (avg num * num nodes + num connections new node) / (num nodes + 1)
        indexFile.seek(self.NUM_CONNECTIONS_OFFSET)
        avgNumConnections = int.from_bytes(indexFile.read(self.numConnectionsByteLen), sys.byteorder, signed=True)

        indexFile.seek(self.NUM_CONNECTIONS_OFFSET)
        newAvgConnections = (int) ((avgNumConnections * numNodes) / (numNodes + 1))
        indexFile.write((newAvgConnections).to_bytes(self.numConnectionsByteLen,
            byteorder = sys.byteorder, signed=True))

        # write ID of new node to end of index
        indexFile.seek(self.NODE_IDS_OFFSET + self.nodeIDByteLen * numNodes)
        indexFile.write((nodeID).to_bytes(self.nodeIDByteLen,
            byteorder = sys.byteorder, signed=True))
        indexFile.seek(self.NODE_IDS_OFFSET + self.nodeIDByteLen * numNodes)
        nodeIDWritten = int.from_bytes(indexFile.read(self.nodeIDByteLen), sys.byteorder, signed=True)
        print("writing {0} ID to index".format(nodeIDWritten))

    # this function finds the number of average connections (relationships) the node has
    def getNumConnections(self):
        indexFile = open(self.filePath, 'r+b') # open node index
        avgNumConnections = int.from_bytes(indexFile.read(self.numConnectionsByteLen), sys.byteorder, signed=True)
        return avgNumConnections

    # this function gets a list of the ids of all nodes in this index
    def getItems(self):
        nodeIDs = []

        indexFile = open(self.filePath, 'r+b') # open node index

        indexFile.seek(self.NUM_NODES_OFFSET)
        numNodes = int.from_bytes(indexFile.read(self.nodeIDByteLen), sys.byteorder, signed=True)

        print("{0} items in index".format(numNodes))

        # get ids
        for i in range(0, numNodes):
            startIndex = self.NODE_IDS_OFFSET + i * self.nodeIDByteLen
            indexFile.seek(startIndex)
            nodeID = int.from_bytes(indexFile.read(self.nodeIDByteLen), sys.byteorder, signed=True)
            nodeIDs.append(nodeID)

        return nodeIDs














