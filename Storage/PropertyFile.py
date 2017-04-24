class PropertyFile:
	numFiles = 0

	def __init__(self):
		PropertyFile.numFiles += 1
		self.fileID = PropertyFile.numFiles
		
		# create node file
		self.fileName = "PropertyFile{0}".format(self.fileID)
		nodeFile = open(self.fileName, 'w')
		nodeFile.close()

	def getFileName(self):
		return self.fileName
