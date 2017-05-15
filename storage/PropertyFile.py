class PropertyFile:
    numFiles = 0

    def __init__(self, createFile=True):
        PropertyFile.numFiles += 1
        self.fileID = PropertyFile.numFiles

        # create property file if it doesn't already exist
        self.fileName = "datastore/PropertyFile{0}.store".format(self.fileID)
        try:
            propertyFile = open(self.fileName, 'r+b')
        except FileNotFoundError:
            propertyFile = open(self.fileName, 'wb')
        propertyFile.close()

    def getFileName(self):
        return self.fileName
