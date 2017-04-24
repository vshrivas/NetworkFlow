class LabelFile:
    numFiles = 0

	def _init_(self):
		numFiles += 1
		self.fileID = numFiles

		# create relationship file
		self.fileName = "LabelFile{0}".format(self.fileID)
		relFile = open(self.fileName, 'w')
		relFile.close()

	def getFileName(self):
		return self.fileName

    # This method reads a given label based on labelID and returns a label object for it
    def readLabel(self, labelID, labelFile):
        nodeStore = open(self.fileName, 'r')
		nodeStartOffset = labelID * Label.storageSize
        
        nodeStore.seek(nodeStartOffset)
        labelID = nodeStore.read(3)

        nodeStore.seek(nodeStartOffset + Label.LABEL_OFFSET)
        labelString = nodeStore.read(4)

        nodeStore.seek(nodeStartOffset + Label.NEXT_LABEL_ID_OFFSET)
        nextLabelID = nodeStore.read(3)

        label = Label(labelID, labelString, nextLabelID)
        return label
