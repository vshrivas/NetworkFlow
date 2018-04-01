import sys, os

from .Label import Label

class LabelFile:

    """LabelFile class: representation of label file, which stores info about all
    labels.
    """

    numFiles = 0

    def __init__(self, createFile=True):
        """Constructor for LabelFile, which creates the backing file if necessary. """
        LabelFile.numFiles += 1
        self.fileID = LabelFile.numFiles

		# create relationship file if it doesn't already exist
        self.fileName = "LabelFile{0}.store".format(self.fileID)
        self.dir = "datafiles"
        self.filePath = os.path.join(self.dir, self.fileName)
        
        if os.path.exists(self.filePath):
            labelFile = open(self.filePath, 'r+b')
        else:
            labelFile = open(self.filePath, 'wb')
            # write number of labels to first 3 bytes of label file
            labelFile.write((0).to_bytes(Label.labelIDByteLen,
                byteorder = sys.byteorder, signed=True))
        labelFile.close()

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
