class LabelPage(DataPage):
	def __init__(self, pageIndex, datafile):
		# 3 indicates that this is a property page
		pageID = [3, pageIndex]
		super().__init__(pageID, datafile)

		self.labelData = []  # list of label objects the page contains
		# read in all page data
		readPageData()

	# reads in all of the label objects stored in this page
	# stores them in self.labelData
	def readPageData(self):
		# open property file
		filePath = ((DataFile) self.file).getFilePath()
		labelFile = open(filePath, 'rb')

		# read in number of entries
		labelFile.seek(self.pageStart + NUM_ENTRIES_OFFSET)
		self.numEntries = int.from_bytes(labelFile.read(DataPage.NUM_ENTRIES_SIZE), sys.byteorder, signed=True)

		# read in owner of page
		labelFile.seek(self.pageStart + OWNER_ID_OFFSET)
		self.ownerID = int.from_bytes(labelFile.read(DataPage.OWNER_ID_SIZE), sys.byteorder, signed=True)

		# read in all data items
		for labelIndex in range(0, self.numEntries):
			label = readPropertyData(labelIndex)
			labelData.append(label)


	def readLabelData(self, labelID):
        """Reads label corresponding to label ID and returns a label object for label."""
        labelStore = open(self.filePath, 'rb')
        # Starting offset for label 
        labelStartOffset = self.pageStart + DATA_OFFSET + labelID * Label.storageSize

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

        label = Label(labelString, datafile, labelID, nextLabelID)
        return label


    def readLabel(self, labelIndex):
    	return labelData[labelIndex]