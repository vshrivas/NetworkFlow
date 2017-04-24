import sys

class LabelFile:
    numFiles = 0

    def __init__(self):
        LabelFile.numFiles += 1
        self.fileID = LabelFile.numFiles

		# create relationship file
        self.fileName = "LabelFile{0}".format(self.fileID)
        relFile = open(self.fileName, 'wb')
        relFile.close()

    def getFileName(self):
        return self.fileName

    # This method reads a given label based on labelID and returns a label object for it
    def readLabel(self, labelID, labelFile):
        nodeStore = open(self.fileName, 'rb')
        nodeStartOffset = labelID * Label.storageSize
        
        nodeStore.seek(nodeStartOffset)
        # Requires Python >= 3.2 for the function int.from_bytes
        labelID = int.from_bytes(nodeStore.read(3), byteorder=sys.byteorder, signed=True)

        nodeStore.seek(nodeStartOffset + Label.LABEL_OFFSET)
        labelString = nodeStore.read(4).decode("utf-8")

        nodeStore.seek(nodeStartOffset + Label.NEXT_LABEL_ID_OFFSET)
        nextLabelID = int.from_bytes(nodeStore.read(3), byteorder=sys.byteorder, signed=True)

        label = Label(labelID, labelString, nextLabelID)
        return label
