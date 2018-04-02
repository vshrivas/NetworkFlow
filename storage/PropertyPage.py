from .Node import Node
from .Property import Property
from .Relationship import Relationship
from .Label import Label
from .DataPage import DataPage
import sys, struct, os

# Property Page handles the byte-level reads and writes of relationships from files
class PropertyPage(DataPage):
    PAGES_OFFSET = 100

    # constructor for PropertyPage
    # takes in 
    # pageIndex: index of page 
    # datafile: propertyFile containing page
    # create: true if creating new page
    def __init__(self, pageIndex, datafile, create):
        # 2 indicates that this is a property page
        pageID = [2, pageIndex]
        super().__init__(pageID, datafile)

        self.propertyData = []  # list of property objects the page contains
        
        self.pageStart = self.getPageIndex() * (self.MAX_PAGE_ENTRIES * Property.storageSize + DataPage.DATA_OFFSET) + self.PAGES_OFFSET

        if create == False:
          # read in all page data
            self.readPageData()
        else:
            self.writePageData()

    # reads in all of the property objects stored in this page
    # stores them in self.propertyData
    def readPageData(self):
        # open property file
        filePath = (self.file).getFilePath()
        propertyFile = open(filePath, 'rb')

        # read in number of entries
        propertyFile.seek(self.pageStart + DataPage.NUM_ENTRIES_OFFSET)
        self.numEntries = int.from_bytes(propertyFile.read(DataPage.NUM_ENTRIES_SIZE), sys.byteorder, signed=True)

        # read in owner of page
        propertyFile.seek(self.pageStart + DataPage.OWNER_ID_OFFSET)
        self.ownerID = int.from_bytes(propertyFile.read(DataPage.OWNER_ID_SIZE), sys.byteorder, signed=True)

        # read in all data items
        for propertyIndex in range(0, self.numEntries):
            property = self.readPropertyData(propertyIndex)
            self.propertyData.append(property)

    # reads data for single property
    def readPropertyData(self, propertyIndex):
        filePath = (self.file).getFilePath()
        propertyStore = open(filePath, 'rb')

        propertyStartOffset = self.pageStart + self.DATA_OFFSET  + propertyIndex * Property.storageSize
        # find ID
        propertyStore.seek(propertyStartOffset + PROPERTY_ID_OFFSET)

        if DEBUG:
            print("seek to {0} for ID". format(propertyStartOffset))

        absPropID = int.from_bytes(propertyStore.read(Property.propIDByteLen), sys.byteorder, signed=True)
        propPageIndex = int(absPropID / DataPage.MAX_PAGE_ENTRIES)
        propIndex = int(((absPropID / DataPage.MAX_PAGE_ENTRIES) - propPageIndex) *  DataPage.MAX_PAGE_ENTRIES)
        propID = [[2, propPageIndex], propIndex]

        # find type
        propertyStore.seek(propertyStartOffset + Property.TYPE_OFFSET)
        print("seek to {0} for type". format(propertyStartOffset + Property.TYPE_OFFSET))
        type = int.from_bytes(propertyStore.read(Property.typeByteLen), sys.byteorder, signed=True)
        #key = int.from_bytes(propertyStore.read(4), sys.byteorder, signed=True)
        print('type: {0}'.format(type))

        # find key
        propertyStore.seek(propertyStartOffset + Property.KEY_OFFSET)
        if DEBUG:
            print("seek to {0} for key". format(propertyStartOffset + Property.KEY_OFFSET))
        key = propertyStore.read(Property.MAX_KEY_SIZE).decode("utf-8")
        # strip padding from key
        key = key.rstrip(' ')
        if DEBUG:
            print('key: {0}'.format(key))

        # find value
        propertyStore.seek(propertyStartOffset + Property.VALUE_OFFSET)
        if DEBUG:
            print("seek to {0} for value". format(propertyStartOffset + Property.VALUE_OFFSET))
        # read value (way value is read depends on its type)
        if type == Property.TYPE_STRING:
            value = propertyStore.read(Property.MAX_VALUE_SIZE).decode("utf-8")
            value = value.rstrip(' ')
        elif type == Property.TYPE_INT:
            value = int.from_bytes(propertyStore.read(4), sys.byteorder, signed=True)
        elif type == Property.TYPE_FLOAT:
            value = struct.unpack('d', propertyStore.read(8))[0]
        else:
            value = bool(int.from_bytes(propertyStore.read(1), sys.byteorder, signed=True))
        if DEBUG:
            print('value: {0}'.format(value))

        propertyStore.seek(propertyStartOffset + NEXT_PROPERTY_ID_OFFSET)
        absNextPropID = int.from_bytes(propertyStore.read(Property.propIDByteLen), sys.byteorder, signed=True)
        if absNextPropID == -1:
            nextPropID = [[2, 0], -1]
        else:
            nextPropPageIndex = int(absNextPropID / DataPage.MAX_PAGE_ENTRIES)
            nextPropIndex = int(((absNextPropID / DataPage.MAX_PAGE_ENTRIES) - nextPropPageIndex) *  DataPage.MAX_PAGE_ENTRIES)
            nextPropID = [[2, nextPropPageIndex], nextPropIndex]

        # initialize property object with key and value and add to relationship
        prop = Property(key, value, datafile, propID, nextPropID)

        return prop

    # returns property given index
    def readProperty(self, propertyIndex):
        return self.propertyData[propertyIndex]

    # writes or creates property given property
    def writeProperty(self, property, create):
        propID = property.getID()

        propIndex = propID[1]

        if create:
            self.propertyData.append(property)
        else:
            self.propertyData[propIndex] = property

        self.writePageData()

    # writes data for full page
    def writePageData(self):
        filePath = (self.file).getFilePath()
        propFile = open(filePath, 'r+b')

        # write number of entries
        propFile.seek(self.pageStart + DataPage.NUM_ENTRIES_OFFSET)
        propFile.write((self.numEntries).to_bytes(DataPage.NUM_ENTRIES_SIZE,
            byteorder = sys.byteorder, signed=True))

        # write owner ID
        propFile.seek(self.pageStart + DataPage.OWNER_ID_OFFSET)
        propFile.write((self.ownerID).to_bytes(DataPage.OWNER_ID_SIZE,
            byteorder = sys.byteorder, signed=True))

        for prop in propertyData:
            self.writePropertyData(prop, propertyFile)

    # writes data for single property
    def writePropertyData(self, prop, storeFile):
        propertyIndex = prop.getID()[1]

        propertyStartOffset = self.pageStart + DataPage.DATA_OFFSET  + propertyIndex * Property.storageSize

        # write property id
        storeFile.seek(propertyStartOffset + Property.PROPERTY_ID_OFFSET)
        absPropID = self.getPageIndex() * DataPage.MAX_PAGE_ENTRIES + propertyIndex
        storeFile.write(absPropID.to_bytes(Property.propIDByteLen, 
                byteorder = sys.byteorder, signed = True))

        # write property value type
        storeFile.seek(propertyStartOffset + Property.TYPE_OFFSET)
        storeFile.write(prop.type.to_bytes(Property.typeByteLen, 
                byteorder = sys.byteorder, signed = True))

        # write key
        storeFile.seek(propertyStartOffset + Property.KEY_OFFSET)

        # key is not of max size
        if(sys.getsizeof(prop.key) != prop.MAX_KEY_SIZE):
            # pad key up to max size
            while len(prop.key.encode('utf-8')) != prop.MAX_KEY_SIZE:
                prop.key += ' '

        storeFile.write(bytearray(prop.key, 'utf8'))

        # write value
        storeFile.seek(propertyStartOffset + Property.VALUE_OFFSET)

        # Write property values of different types (strings, ints, floats, and booleans)
        if prop.type == Property.TYPE_STRING:
            # value is not of max size
            if(sys.getsizeof(prop.value) != prop.MAX_VALUE_SIZE):
                # pad value up to max size
                while len(prop.value.encode('utf-8')) != prop.MAX_VALUE_SIZE:
                    prop.value += ' '
            storeFile.write(bytearray(prop.value, 'utf8'))
        elif prop.type == Property.TYPE_INT:
            storeFile.write(prop.value.to_bytes(4, byteorder=sys.byteorder, signed = True))
        elif prop.type == Property.TYPE_FLOAT:
            storeFile.write(bytearray(struct.pack("d", prop.value)))
        else:
            if prop.value:
                storeFile.write((1).to_bytes(1, byteorder=sys.byteorder, signed = True))
            else:
                storeFile.write((0).to_bytes(1, byteorder=sys.byteorder, signed = True))

        # write next property id
        storeFile.seek(propertyStartOffset + Property.NEXT_PROPERTY_ID_OFFSET)
        if prop.nextPropertyID[1] == -1:
            absNextPropID = -1
        else:
            absNextPropID = prop.nextPropertyID[0][1] * DataPage.MAX_PAGE_ENTRIES + prop.nextPropertyID[1]

        print("writing next property ID {0} at {1}".format(absNextPropID, propertyStartOffset + Property.NEXT_PROPERTY_ID_OFFSET))
        storeFile.write(absNextPropID.to_bytes(Property.propIDByteLen, 
                byteorder = sys.byteorder, signed = True))

