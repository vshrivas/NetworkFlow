# Class: Property

# Storage: 
# Bytes 1-4: Property ID
# Bytes 5-8: Key
# Bytes 9-12: Value
# Bytes 13-16: Next Property ID
import sys

class Property:
    PROPERTY_ID_OFFSET = 0
    KEY_OFFSET = 4
    VALUE_OFFSET = 8
    NEXT_PROPERTY_ID_OFFSET = 12

    storageSize = 16
    numProperties = 0

    propIDByteSize = 4

    def __init__(self, key, value, propertyFile, propertyID=numProperties):
        # Note: For reading properties from files, we assume keys and values to be ints.
        # TODO: Support reading keys and values of other types
        self.key = key
        self.value = value

        self.propertyID = propertyID
        Property.numProperties += 1

        self.propertyFile = propertyFile

        self.startOffset = self.propertyID * Property.storageSize

    def getKey(self):
        return self.key

    def getValue(self):
        return self.value

    def getPropertyFile(self):
        return self.propertyFile

    def getID(self):
        return self.propertyID

    def writeProperty(self, nextProp):
        # open property file
        storeFileName = self.getPropertyFile().getFileName()
        storeFile = open(storeFileName, 'ab')

        # write property id
        storeFile.seek(self.startOffset + Property.PROPERTY_ID_OFFSET)
        storeFile.write(self.propertyID.to_bytes(Property.propIDByteSize, 
                byteorder = sys.byteorder, signed = True))

        # write key
        storeFile.seek(self.startOffset + Property.KEY_OFFSET)
        storeFile.write(bytearray(self.key, 'utf8'))

        # write value
        storeFile.seek(self.startOffset + Property.VALUE_OFFSET)
        storeFile.write(bytearray(self.value, 'utf8'))

        # write next property id
        storeFile.seek(self.startOffset + Property.NEXT_PROPERTY_ID_OFFSET)
        print("next property has index:{0}".format(nextProp.getID()))
        storeFile.write(nextProp.getID().to_bytes(Property.propIDByteSize, 
                byteorder = sys.byteorder, signed = True))



