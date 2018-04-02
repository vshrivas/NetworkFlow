from .Node import Node
from .Property import Property
from .Relationship import Relationship
from .Label import Label
from .NodePage import NodePage
import sys, struct, os

DEBUG = False

class NodeFile(object):

    """NodeFile class: representation of node file, which stores info about all
    nodes. A NodeFile object can read nodes from the backing node file and stores 
    the number of pages.
    """

    MAX_PAGES = 10
    NUMPAGES_OFFSET = 0
    PAGES_OFFSET = 100

    NUMPAGES_SIZE = 100

    directory = "nodestore"

    def __init__(self, fileID):
        """Constructor for NodeFile, which creates the backing file if necessary. """
        self.fileID = fileID

        # create node file if it doesn't already exist
        self.fileName = "NodeFile{0}.store".format(self.fileID)
        self.filePath = os.path.join(self.directory, self.fileName)

        self.numPages = 0

        if os.path.exists(self.filePath):
            print('node file exists')
            nodeFile = open(self.filePath, 'rb')
            self.numPages = int.from_bytes(nodeFile.read(self.NUMPAGES_SIZE), sys.byteorder, signed=True)
            print('has {0} pages'.format(self.numPages))
        else:
            print('creating new node file')
            if not os.path.exists(self.directory):
                os.makedirs(self.directory)
            nodeFile = open(self.filePath, 'wb')
            # write number of pages to first 3 bytes of node file
            nodeFile.write((0).to_bytes(self.NUMPAGES_SIZE,
                byteorder = sys.byteorder, signed=True))

        nodeFile.close()

    # creates a new node page
    def createPage(self):
        nodePage = NodePage(self.numPages, self, True)
        self.numPages += 1
            
        nodeFile = open(self.filePath, 'r+b')
        nodeFile.write((self.numPages).to_bytes(self.NUMPAGES_SIZE,
                byteorder = sys.byteorder, signed=True))

        nodeFile.close()

        return nodePage

    def getFileName(self):
        """Return file name of backing file."""
        return self.fileName

    def getFilePath(self):
        return self.filePath

    def getNumNodes(self):
        """Return number of nodes."""
        nodeFile = open(self.filePath, 'r+b')
        numNodes = int.from_bytes(nodeFile.read(Node.nodeIDByteLen), byteorder=sys.byteorder, signed=True)
        return numNodes



