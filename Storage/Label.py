# Storage
# Bytes 1-3: Label ID
# Bytes 4-7: Label
# Bytes 8-11: Next Label ID
class Label:
    LABEL_ID_OFFSET = 0
    LABEL_OFFSET = 3
    NEXT_LABEL_ID_OFFSET = 7

    storageSize = 11
    numLabels = 0

    def __init__(self, label, labelFile, labelID=None):
        if labelID is None:
            labelID = numLabels
            
        self.labelID = labelID

        self.label = label
        Label.numLabels += 1

        self.labelFile = labelFile

        self.startOffset = self.labelID * Label.storageSize

    def writeLabel(self, nextLabelID):
        # open label file
        storeFileName = self.labelFile.getFileName()
        storeFile = open(storeFileName, 'ab')

        # seek to location for label and write label ID
        storeFile.seek(self.startOffset)
        storeFile.write(bytearray(self.labelID))

        # write label
        storeFile.seek(self.startOffset + Label.LABEL_OFFSET)
        storeFile.write(bytearray(self.label))

        # write next label's ID
        storeFile.seek(self.startOffset + Label.NEXT_LABEL_ID_OFFSET)
        storeFile.write(bytearray(self.nextLabelID))

        
