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
        
        if os.path.exists(os.path.join(self.dir, self.fileName)):
            labelFile = open(os.path.join(self.dir, self.fileName), 'r+b')
        else:
            labelFile = open(os.path.join(self.dir, self.fileName), 'wb')
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

    def readLabel(self, labelID):
        """Reads label corresponding to label ID and returns a label object for label."""
        labelStore = open(self.filePath, 'rb')
        # Starting offset for label 
        labelStartOffset = labelID * Label.storageSize + Label.labelIDByteLen

        # Read label ID
        labelStore.seek(labelStartOffset + Label.LABEL_ID_OFFSET)
        # Requires Python >= 3.2 for the function int.from_bytes
        labelID = int.from_bytes(labelStore.read(3), byteorder=sys.byteorder, signed=True)

        # Read label string
        labelStore.seek(labelStartOffset + Label.LABEL_OFFSET)
        # Remove padding from label string
        labelString = labelStore.read(Label.MAX_LABEL_SIZE).decode('utf8').rstrip(' ')

        # Read next label ID
        labelStore.seek(labelStartOffset + Label.NEXT_LABEL_ID_OFFSET)
        nextLabelID = int.from_bytes(labelStore.read(3), byteorder=sys.byteorder, signed=True)

        label = Label(labelString, self, labelID, nextLabelID)
        return label
