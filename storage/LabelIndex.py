""" 
Storage
Bytes 1-100: Label string
Bytes 101-103: number of nodes
Bytes 104-109: average number of connections (double)
Bytes 110-...: IDs of nodes in index (3 bytes each)
"""
import sys

class LabelIndex:
    # offsets from start of index
    LABEL_STRING_OFFSET = 0
    NUM_NODES_OFFSET = 100
    NUM_CONNECTIONS_OFFSET = 103
    NODE_IDS_OFFSET = 109

    numConnectionsByteLen = 6
    nodeIDByteLen = 3

    def __init__(self, labelStr):
        self.labelStr = labelStr
        # create index file if it doesn't already exist
        self.fileName = "{0}.labelindex".format(self.labelStr)

        # open index file
        try:
            indexFile = open(self.fileName, 'r+b')

        except FileNotFoundError:
            indexFile = open(self.fileName, 'wb')
            # label string
            indexFile.write(bytearray(self.labelStr, "utf8"))
            # write number of nodes to next 3 bytes of index file
            indexFile.write((0).to_bytes(self.nodeIDByteLen,
                byteorder = sys.byteorder, signed=True))
            # write number of nodes to next 3 bytes of index file
            indexFile.write((0).to_bytes(self.nodeIDByteLen,
                byteorder = sys.byteorder, signed=True))
        indexFile.close()

    def addNode(self, nodeID):
        # increment number of nodes
        indexFile = open(self.fileName, 'r+b') # open node index
        indexFile.seek(self.NUM_NODES_OFFSET)
        numNodes = int.from_bytes(indexFile.read(self.nodeIDByteLen), sys.byteorder, signed=True)
        indexFile.write((numNodes + 1).to_bytes(self.nodeIDByteLen,
            byteorder = sys.byteorder, signed=True))

        # update average number of connections (avg num * num nodes + num connections new node) / (num nodes + 1)
        indexFile.seek(self.NUM_CONNECTIONS_OFFSET)
        avgNumConnections = int.from_bytes(indexFile.read(self.numConnectionsByteLen), sys.byteorder, signed=True)
        newAvgConnections = (int) ((avgNumConnections * numNodes) / (numNodes + 1))
        indexFile.write((newAvgConnections).to_bytes(self.numConnectionsByteLen,
            byteorder = sys.byteorder, signed=True))

        # write ID of new node to end of index
        indexFile.seek(self.NODE_IDS_OFFSET + self.nodeIDByteLen * numNodes)
        indexFile.write((nodeID).to_bytes(self.nodeIDByteLen,
            byteorder = sys.byteorder, signed=True))

    def getNumConnections(self):
        indexFile = open(self.fileName, 'r+b') # open node index
        avgNumConnections = int.from_bytes(indexFile.read(self.numConnectionsByteLen), sys.byteorder, signed=True)
        return avgNumConnections

    def getItems(self):
        nodeIDs = []

        indexFile = open(self.fileName, 'r+b') # open node index

        indexFile.seek(self.NUM_NODES_OFFSET)
        numNodes = int.from_bytes(indexFile.read(self.nodeIDByteLen), sys.byteorder, signed=True)

        for i in range(0, numNodes):
            startIndex = i * self.nodeIDByteLen
            indexFile.seek(startIndex)
            nodeID = int.from_bytes(indexFile.read(self.nodeIDByteLen), sys.byteorder, signed=True)
            nodeIDs.append(nodeID)

        return nodeIDs














