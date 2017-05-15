# Class: Property

# Storage: 
# Bytes 1-4: Property ID
# Bytes 5-104: Key
# Bytes 105-204: Value
# Bytes 205-208: Next Property ID
import sys

class Property:
    PROPERTY_ID_OFFSET = 0
    KEY_OFFSET = 4
    VALUE_OFFSET = 104
    NEXT_PROPERTY_ID_OFFSET = 204
    MAX_KEY_SIZE = 100
    MAX_VALUE_SIZE = 100

    storageSize = 208
    numProperties = 0
    propIDByteSize = 4

    def __init__(self, key, value, propertyFile, propertyID=None):
        # Note: For reading properties from files, we assume keys and values to be ints.
        # TODO: Support reading keys and values of other types
        if propertyID is None:
            propertyID = Property.numProperties
            
        self.key = key
        self.value = value

        self.propertyID = propertyID

        if propertyID != -1:
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
        print() 

        # open property file
        storeFileName = self.getPropertyFile().getFileName()
        storeFile = open(storeFileName, 'r+b')

        print("writing property id {0} at {1}".format(self.propertyID, self.startOffset + Property.PROPERTY_ID_OFFSET))

        # write property id
        storeFile.seek(self.startOffset + Property.PROPERTY_ID_OFFSET)
        storeFile.write(self.propertyID.to_bytes(Property.propIDByteSize, 
                byteorder = sys.byteorder, signed = True))

        # write key
        storeFile.seek(self.startOffset + Property.KEY_OFFSET)

        # key is not of max size
        if(sys.getsizeof(self.key) != self.MAX_KEY_SIZE):
            # pad key up to max size
            while len(self.key.encode('utf-8')) != self.MAX_KEY_SIZE:
                self.key += ' '

        print("writing key {0} at {1}".format(self.key, self.startOffset + Property.KEY_OFFSET))

        storeFile.write(bytearray(self.key, 'utf8'))

        # write value
        storeFile.seek(self.startOffset + Property.VALUE_OFFSET)

        # value is not of max size
        if(sys.getsizeof(self.value) != self.MAX_VALUE_SIZE):
            # pad value up to max size
            while len(self.value.encode('utf-8')) != self.MAX_VALUE_SIZE:
                self.value += ' '

        print("writing value {0} at {1}".format(self.value, self.startOffset + Property.VALUE_OFFSET))

        storeFile.write(bytearray(self.value, 'utf8'))

        # write next property id
        storeFile.seek(self.startOffset + Property.NEXT_PROPERTY_ID_OFFSET)
        print("next property has index:{0}".format(nextProp.getID()))

        print("writing next property index {0} at {1}".format(nextProp.getID(), self.startOffset + Property.NEXT_PROPERTY_ID_OFFSET))
        storeFile.write(nextProp.getID().to_bytes(Property.propIDByteSize, 
                byteorder = sys.byteorder, signed = True))

        print()



