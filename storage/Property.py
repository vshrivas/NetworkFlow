# Class: Property

# Storage: 
# Bytes 1-4: Property ID
# Bytes 5: Property Value Type
# Bytes 6-105: Key
# Bytes 106-205: Value
# Bytes 206-209: Next Property ID
import sys, struct

class Property:
    PROPERTY_ID_OFFSET = 0
    TYPE_OFFSET = 4
    KEY_OFFSET = 5
    VALUE_OFFSET = 105
    NEXT_PROPERTY_ID_OFFSET = 205
    MAX_KEY_SIZE = 100
    MAX_VALUE_SIZE = 100

    TYPE_STRING = 0
    TYPE_INT = 1
    TYPE_FLOAT = 2
    TYPE_BOOL = 3

    storageSize = 209
    numProperties = 0
    propIDByteLen = 4
    typeByteLen = 1

    def __init__(self, key, value, propertyFile, propertyID=None):
        if propertyFile != "":
            Property.numProperties = propertyFile.getNumProperties()
            print("****** Num properties = {0} ******".format(Property.numProperties))
        # Note: For reading properties from files, we assume keys to be strings and
        # values to be strings, ints, floats, or booleans.
        if propertyID is None:
            propertyID = Property.numProperties
            
        self.key = key
        self.value = value

        if isinstance(value, str):
            self.type = Property.TYPE_STRING
        elif isinstance(value, bool):
            self.type = Property.TYPE_BOOL
        elif isinstance(value, int):
            self.type = Property.TYPE_INT
        else:
            self.type = Property.TYPE_FLOAT
        

        self.propertyID = propertyID

        # property isn't the null property and is a new property
        if self.propertyID != -1 and self.propertyID >= self.numProperties:
            Property.numProperties += 1

        self.propertyFile = propertyFile

        if self.propertyFile != "":
            # open property file
            storeFileName = self.propertyFile.getFileName()
            storeFile = open(storeFileName, 'r+b')

            # write number of properties to first 4 bytes of property file
            storeFile.write((Property.numProperties).to_bytes(Property.propIDByteLen,
                byteorder = sys.byteorder, signed=True))

        self.startOffset = self.propertyID * Property.storageSize + Property.propIDByteLen

    def getKey(self):
        return self.key

    def getValue(self):
        return self.value

    def getPropertyFile(self):
        return self.propertyFile

    def getID(self):
        return self.propertyID

    def getType(self):
        return self.type

    def writeProperty(self, nextProp):
        print() 

        # open property file
        storeFileName = self.getPropertyFile().getFileName()
        storeFile = open(storeFileName, 'r+b')

        print("writing property id {0} at {1}".format(self.propertyID, self.startOffset + Property.PROPERTY_ID_OFFSET))

        # write property id
        storeFile.seek(self.startOffset + Property.PROPERTY_ID_OFFSET)
        storeFile.write(self.propertyID.to_bytes(Property.propIDByteLen, 
                byteorder = sys.byteorder, signed = True))

        # write property value type
        storeFile.seek(self.startOffset + Property.TYPE_OFFSET)
        storeFile.write(self.type.to_bytes(Property.typeByteLen, 
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

        print("writing value {0} at {1}".format(self.value, self.startOffset + Property.VALUE_OFFSET))

        # Write property values of different types (strings, ints, floats, and booleans)
        if self.type == Property.TYPE_STRING:
            # value is not of max size
            if(sys.getsizeof(self.value) != self.MAX_VALUE_SIZE):
                # pad value up to max size
                while len(self.value.encode('utf-8')) != self.MAX_VALUE_SIZE:
                    self.value += ' '
            storeFile.write(bytearray(self.value, 'utf8'))
        elif self.type == Property.TYPE_INT:
            storeFile.write(self.value.to_bytes(4, byteorder=sys.byteorder, signed = True))
        elif self.type == Property.TYPE_FLOAT:
            storeFile.write(bytearray(struct.pack("d", self.value)))
        else:
            if self.value:
                storeFile.write((1).to_bytes(1, byteorder=sys.byteorder, signed = True))
            else:
                storeFile.write((0).to_bytes(1, byteorder=sys.byteorder, signed = True))

        # write next property id
        storeFile.seek(self.startOffset + Property.NEXT_PROPERTY_ID_OFFSET)
        print("next property has index:{0}".format(nextProp.getID()))

        print("writing next property index {0} at {1}".format(nextProp.getID(), self.startOffset + Property.NEXT_PROPERTY_ID_OFFSET))
        storeFile.write(nextProp.getID().to_bytes(Property.propIDByteLen, 
                byteorder = sys.byteorder, signed = True))

        print()



