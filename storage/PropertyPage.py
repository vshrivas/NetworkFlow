class PropertyPage(DataPage):
	def __init__(self, pageIndex, datafile):
		# 2 indicates that this is a property page
		pageID = [2, pageIndex]
		super().__init__(pageID, datafile)

		self.propertyData = []  # list of property objects the page contains
		# read in all page data
		readPageData()

	# reads in all of the property objects stored in this page
	# stores them in self.propertyData
	def readPageData(self):
		# open property file
		filePath = ((DataFile) self.file).getFilePath()
		propertyFile = open(filePath, 'rb')

		# read in number of entries
		propertyFile.seek(self.pageStart + NUM_ENTRIES_OFFSET)
		self.numEntries = int.from_bytes(propertyFile.read(DataPage.NUM_ENTRIES_SIZE), sys.byteorder, signed=True)

		# read in owner of page
		propertyFile.seek(self.pageStart + OWNER_ID_OFFSET)
		self.ownerID = int.from_bytes(propertyFile.read(DataPage.OWNER_ID_SIZE), sys.byteorder, signed=True)

		# read in all data items
		for propertyIndex in range(0, self.numEntries):
			property = readPropertyData(propertyIndex)
			propertyData.append(property)

	def readPropertyData(self, propertyIndex):
		filePath = ((PropertyFile) self.file).getFilePath()
		propertyStore = open(filePath, 'rb')

		propertyStartOffset = self.pageStart + DATA_OFFSET  + propertyIndex * Property.storageSize
		# find ID
        propertyStore.seek(propertyStartOffset)

        if DEBUG:
            print("seek to {0} for ID". format(propertyStartOffset))

        propID = int.from_bytes(propertyStore.read(Property.propIDByteLen), sys.byteorder, signed=True)

        if DEBUG:
            print('id: {0}'.format(ID))

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
        nextPropID = int.from_bytes(propertyStore.read(Property.propIDByteLen), sys.byteorder, signed=True)
        # initialize property object with key and value and add to relationship
        prop = Property(key, value, datafile, propID, nextPropID)

        return prop

    def readProperty(self, propertyIndex):
    	return propertyData[propertyIndex]

	def writeProperty(currProp, nextProp):
        """Write property to disk using specified next property."""
        if DEBUG:
            print() 

        # open property file
        storeFilePath = ((PropertyFile)self.file).getFilePath()
        storeFile = open(storeFilePath, 'r+b')

        if DEBUG:
            print("writing property id {0} at {1}".format(currProp.propertyID, currProp.startOffset + Property.PROPERTY_ID_OFFSET))

        # write property id
        storeFile.seek(self.pageStart + currProp.startOffset + Property.PROPERTY_ID_OFFSET)
        storeFile.write(currProp.propertyID.to_bytes(Property.propIDByteLen, 
                byteorder = sys.byteorder, signed = True))

        # write property value type
        storeFile.seek(self.pageStart + currProp.startOffset + Property.TYPE_OFFSET)
        storeFile.write(currProp.type.to_bytes(Property.typeByteLen, 
                byteorder = sys.byteorder, signed = True))

        # write key
        storeFile.seek(self.pageStart + currProp.startOffset + Property.KEY_OFFSET)

        # key is not of max size
        if(sys.getsizeof(currProp.key) != currProp.MAX_KEY_SIZE):
            # pad key up to max size
            while len(currProp.key.encode('utf-8')) != currProp.MAX_KEY_SIZE:
                currProp.key += ' '

        if DEBUG:
            print("writing key {0} at {1}".format(currProp.key, self.pageStart + currProp.startOffset + Property.KEY_OFFSET))

        storeFile.write(bytearray(currProp.key, 'utf8'))

        # write value
        storeFile.seek(self.pageStart + currProp.startOffset + Property.VALUE_OFFSET)
        
        if DEBUG:
            print("writing value {0} at {1}".format(currProp.value, currProp.startOffset + Property.VALUE_OFFSET))

        # Write property values of different types (strings, ints, floats, and booleans)
        if currProp.type == Property.TYPE_STRING:
            # value is not of max size
            if(sys.getsizeof(currProp.value) != currProp.MAX_VALUE_SIZE):
                # pad value up to max size
                while len(currProp.value.encode('utf-8')) != currProp.MAX_VALUE_SIZE:
                    currProp.value += ' '
            storeFile.write(bytearray(currProp.value, 'utf8'))
        elif currProp.type == Property.TYPE_INT:
            storeFile.write(currProp.value.to_bytes(4, byteorder=sys.byteorder, signed = True))
        elif currProp.type == Property.TYPE_FLOAT:
            storeFile.write(bytearray(struct.pack("d", currProp.value)))
        else:
            if currProp.value:
                storeFile.write((1).to_bytes(1, byteorder=sys.byteorder, signed = True))
            else:
                storeFile.write((0).to_bytes(1, byteorder=sys.byteorder, signed = True))

        # write next property id
        storeFile.seek(self.pageStart + currProp.startOffset + Property.NEXT_PROPERTY_ID_OFFSET)
        if DEBUG:
            print("next property has index:{0}".format(nextProp.getID()))

            print("writing next property index {0} at {1}".format(nextProp.getID(), currProp.startOffset + Property.NEXT_PROPERTY_ID_OFFSET))
        storeFile.write(nextProp.getID().to_bytes(Property.propIDByteLen, 
                byteorder = sys.byteorder, signed = True))

        if DEBUG:
            print()
