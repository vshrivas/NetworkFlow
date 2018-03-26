# Class: Property

# Storage: 
# Bytes 1-4: Property ID
# Bytes 5: Property Value Type
# Bytes 6-105: Key
# Bytes 106-205: Value
# Bytes 206-209: Next Property ID
import sys, struct

DEBUG = False

class Property:

    """Property class: representation of a property, which stores a key value pair.

    Storage: Properties are stored as fixed size records which are 208 bytes in
    length. This fixed size storage format makes looking up specific properties
    in the database faster as to look up a property, only the property ID is needed. 
    The ID of the next property of the associated node or relationship is stored so 
    that properties can be traversed in a linked list fashion when reading nodes or 
    relationships.

    Bytes 1-4: Property ID
    Bytes 5-104: Key
    Bytes 105-204: Value
    Bytes 205-208: Next Property ID
    """

    # byte offsets from start of property
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
    # number of properties ever created (used for auto-incrementing the property ID)
    numProperties = 0
    propIDByteLen = 4
    typeByteLen = 1

    # property ID is a list of 2 elements 
    # propertyID[0] = pageID
    # propertyID[1] = propIndex
    def __init__(self, key, value, propertyFile, propertyID, nextPropertyID):
        """Constructor for Property, which sets the key, the value, the property ID, 
        and the file the property is stored in.

        Arguments:
        key: key for property
        value: value for property
        propertyFile: the PropertyFile object that represents the file storing properties
        propertyID: the ID of the Property to be initialized; default propertyID of None 
        means the Property will be assigned an auto-incrementing property ID
        """
        # If propertyFile object passed exists, get number of properties
        if propertyFile != "":
            Property.numProperties = propertyFile.getNumProperties()
            if DEBUG:
                print("****** Num properties = {0} ******".format(Property.numProperties))
        # Note: For reading properties from files, we assume keys and values to be ints.
        # TODO: Support reading keys and values of other types
        # if propertyID is None, use auto-incrementing for property ID
        if propertyID is None:
            propertyID = Property.numProperties
            
        # set key and value
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
        
        # set property ID
        self.propertyID = propertyID

        self.nextPropertyID = nextPropertyID

        # property isn't the null property and is a new property
        if self.getpropertyIndex() != -1 and self.getPropertyIndex() >= self.numProperties:
            Property.numProperties += 1

        # set property file
        self.propertyFile = propertyFile

        # If propertyFile object passed exists
        if self.propertyFile != "":
            # open property file
            storeFilePath = self.propertyFile.getFilePath()
            storeFile = open(storeFilePath, 'r+b')

            # write number of properties to first 4 bytes of property file
            storeFile.write((Property.numProperties).to_bytes(Property.propIDByteLen,
                byteorder = sys.byteorder, signed=True))

        # starting offset for property in property file
        self.startOffset = self.getPropertyIndex() * Property.storageSize + Property.propIDByteLen

    def getPropertyIndex(self):
        return propertyID[1]

    # returns the property pageID
    def getPropertyPage(self):
        return propertyID[0]

    def getKey(self):
        """Return key of property."""
        return self.key

    def getValue(self):
        """Return value of property.""" 
        return self.value

    def getPropertyFile(self):
        """Return property file of property."""
        return self.propertyFile

    def getID(self):
        """Return ID of property."""
        return self.propertyID

    def getType(self):
        return self.type