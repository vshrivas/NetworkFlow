import sys

from .Label import Label

class LabelFile:
    numFiles = 0

    def __init__(self, createFile=True):
        LabelFile.numFiles += 1
        self.fileID = LabelFile.numFiles

		# create relationship file if it doesn't already exist
        self.fileName = "LabelFile{0}.store".format(self.fileID)
        try:
            labelFile = open(self.fileName, 'r+b')
        except FileNotFoundError:
            labelFile = open(self.fileName, 'wb')
            # write number of labels to first 3 bytes of label file
            labelFile.write((0).to_bytes(Label.labelIDByteLen,
                byteorder = sys.byteorder, signed=True))
        labelFile.close()

    def getFileName(self):
        return self.fileName

    def getNumLabels(self):
        labelFile = open(self.fileName, 'r+b')
        numLabels = int.from_bytes(labelFile.read(Label.labelIDByteLen), byteorder=sys.byteorder, signed=True)
        return numLabels

    # This method reads a given label based on labelID and returns a label object for it
    def readLabel(self, labelID):
        labelStore = open(self.fileName, 'rb')
        labelStartOffset = labelID * Label.storageSize + Label.labelIDByteLen

        labelStore.seek(labelStartOffset + Label.LABEL_ID_OFFSET)
        # Requires Python >= 3.2 for the function int.from_bytes
        labelID = int.from_bytes(labelStore.read(3), byteorder=sys.byteorder, signed=True)

        labelStore.seek(labelStartOffset + Label.LABEL_OFFSET)
        labelString = labelStore.read(Label.MAX_LABEL_SIZE).decode('utf8').rstrip(' ')

        labelStore.seek(labelStartOffset + Label.NEXT_LABEL_ID_OFFSET)
        nextLabelID = int.from_bytes(labelStore.read(3), byteorder=sys.byteorder, signed=True)

        label = Label(labelString, self, labelID, nextLabelID)
        return label
