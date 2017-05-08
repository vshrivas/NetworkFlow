import sys

from Label import Label

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
    def readLabel(self, labelID):
        labelStore = open(self.fileName, 'rb')
        labelStartOffset = labelID * Label.storageSize
        
        labelStore.seek(labelStartOffset + Label.LABEL_ID_OFFSET)
        # Requires Python >= 3.2 for the function int.from_bytes
        labelID = int.from_bytes(labelStore.read(3), byteorder=sys.byteorder, signed=True)

        labelStore.seek(labelStartOffset + Label.LABEL_OFFSET)
        labelString = labelStore.read(4).decode('utf8')

        labelStore.seek(labelStartOffset + Label.NEXT_LABEL_ID_OFFSET)
        nextLabelID = int.from_bytes(labelStore.read(3), byteorder=sys.byteorder, signed=True)

        label = Label(labelString, self, labelID, nextLabelID)
        return label
