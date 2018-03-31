from Node import Node
from Property import Property
from Relationship import Relationship
from Label import Label
from NodePage import NodePage
import sys, struct, os

DEBUG = False

class NodeFile(object):

    """NodeFile class: representation of node file, which stores info about all
    nodes. A NodeFile object can read nodes from the backing node file and stores 
    the current number of nodes.
    """

    # number of node files
    #numFiles = 0
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

    def createPage(self):
        NodePage(self.numPages, self, True)
        self.numPages += 1
            
        nodeFile = open(self.filePath, 'r+b')
        nodeFile.write((self.numPages).to_bytes(self.NUMPAGES_SIZE,
                byteorder = sys.byteorder, signed=True))

        nodeFile.close()

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

    '''def readNode(pageID, nodeID):
        

    def writeNode(node):
        pageID = node.nodeID[0]          # pageID[0] = 0, pageID[1] = pageIndex
        nodePage = BufferManager.getNodePage(pageID, self)

        nodePage.writeNode(node)

    def createNode():
        # check if last page has space
        # if not, create 

    # checks if file has space
    # if so, returns page with space
    # else returns None
    def hasSpace():
        # index of last page
        lastPageIndex = self.numPages - 1
        startLastPage = PAGES_OFFSET + DataPage.MAX_PAGE_SIZE * lastPageIndex

        # read number of nodes in last page
        file = open(self.filePath, 'rb')
        file.seek(startLastPage)
        numNodes = int.from_bytes(file.read(Node.nodeIDByteLen), byteorder=sys.byteorder, signed=True)

        # page isn't full
        if (numNodes < (DataPage.MAX_PAGE_SIZE/ Node.storageSize)):
            lastPage = BufferManager.getNodePage(lastPageIndex)
        # page is full
        else:
            # file is full
            if lastPageIndex == DataFile.MAX_FILE_PAGES - 1:
                return None
            # make a new page
            else:
                newPage = NodePage(lastPageIndex + 1)
                return newPage'''












