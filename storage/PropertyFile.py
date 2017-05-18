from .Property import Property
import sys

class PropertyFile:
    numFiles = 0

    def __init__(self, createFile=True):
        PropertyFile.numFiles += 1
        self.fileID = PropertyFile.numFiles

        # create property file if it doesn't already exist
        self.fileName = "PropertyFile{0}.store".format(self.fileID)
        try:
            propertyFile = open(self.fileName, 'r+b')
        except FileNotFoundError:
            propertyFile = open(self.fileName, 'wb')
            # write number of properties to first 4 bytes of property file
            propertyFile.write((0).to_bytes(Property.propIDByteLen,
                byteorder = sys.byteorder, signed=True))
        propertyFile.close()

    def getFileName(self):
        return self.fileName

    def getNumProperties(self):
        propertyFile = open(self.fileName, 'r+b')
        numProperties = int.from_bytes(propertyFile.read(Property.propIDByteLen), byteorder=sys.byteorder, signed=True)
        return numProperties
