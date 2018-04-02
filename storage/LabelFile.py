import sys, os

from .Label import Label
from .LabelPage import LabelPage

class LabelFile:

    """LabelFile class: representation of label file, which stores info about all
    labels.
    """
    MAX_PAGES = 10
    NUMPAGES_OFFSET = 0
    PAGES_OFFSET = 100

    NUMPAGES_SIZE = 100

    directory = "labelstore"

    def __init__(self, fileID):
        """Constructor for LabelFile, which creates the backing file if necessary. """
        self.fileID = fileID

        # create relationship file if it doesn't already exist
        self.fileName = "LabelFile{0}.store".format(self.fileID)
        self.filePath = os.path.join(self.directory, self.fileName)

        self.numPages = 0
        
        if os.path.exists(self.filePath):
            print('label file exists')
            labelFile = open(self.filePath, 'rb')
            self.numPages = int.from_bytes(labelFile.read(self.NUMPAGES_SIZE), sys.byteorder, signed=True)
            print('has {0} pages'.format(self.numPages))
        else:
            print('creating new label file')
            if not os.path.exists(self.directory):
                os.makedirs(self.directory)
            labelFile = open(self.filePath, 'wb')
            # write number of pages to first 3 bytes of node file
            labelFile.write((0).to_bytes(self.NUMPAGES_SIZE,
                byteorder = sys.byteorder, signed=True))

        labelFile.close()

    def createPage(self):
        labelPage = LabelPage(self.numPages, self, True)
        self.numPages += 1
            
        labelFile = open(self.filePath, 'r+b')
        labelFile.write((self.numPages).to_bytes(self.NUMPAGES_SIZE,
                byteorder = sys.byteorder, signed=True))

        labelFile.close()

        return labelPage

    def getFileName(self):
        """Returns name of backing file."""
        return self.fileName

    def getNumLabels(self):
        """Returns number of labels."""
        labelFile = open(self.filePath, 'r+b')
        numLabels = int.from_bytes(labelFile.read(Label.labelIDByteLen), byteorder=sys.byteorder, signed=True)
        return numLabels

    def getFilePath(self):
        return self.filePath
