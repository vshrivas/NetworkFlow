class PropertyFile:
	numFiles = 0

	def _init_(self):
		numFiles += 1
		self.fileID = numFiles
		
		# create node file
		self.fileName = "PropertyFile{0}".format(self.fileID)
		nodeFile = open(self.fileName, 'w')
		nodeFile.close()

	def getFileName():
		return self.fileName
