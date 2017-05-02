import sys

# Storage
# Bytes 1-3: Label ID
# Bytes 4-7: Label
# Bytes 8-10: Next Label ID

class Label:
    LABEL_ID_OFFSET = 0
    LABEL_OFFSET = 3
    NEXT_LABEL_ID_OFFSET = 7

    storageSize = 10
    numLabels = 0

    def __init__(self, label, labelFile, labelID=None, nextLabelID=-1):
        if labelID is None:
            labelID = Label.numLabels
        self.labelID = labelID
        Label.numLabels += 1

        self.label = label

        self.labelFile = labelFile

        self.startOffset = self.labelID * Label.storageSize
        self.nextLabelID = nextLabelID

    def getLabelID():
        return self.labelID

    def writeLabel(self, nextLabelID):
        # open label file
        storeFileName = self.labelFile.getFileName()
        storeFile = open(storeFileName, 'ab')

        # seek to location for label and write label ID
        storeFile.seek(self.startOffset)
        storeFile.write(self.labelID.to_bytes(3, 
            byteorder = sys.byteorder, signed=True))

        # write label
        storeFile.seek(self.startOffset + Label.LABEL_OFFSET)
        storeFile.write(bytearray(self.label, "utf8"))

        # write next label's ID
        storeFile.seek(self.startOffset + Label.NEXT_LABEL_ID_OFFSET)

        print("writing next label id: {0}".format(nextLabelID))
        storeFile.write(nextLabelID.to_bytes(3, 
            byteorder = sys.byteorder, signed=True))


        
