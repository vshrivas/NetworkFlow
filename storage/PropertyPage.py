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

    def writePageData(self):
        filePath = ((PropertyFile) self.datafile).getFilePath()
        propFile = open(filePath, 'rb')

        # write number of entries
        propFile.seek(self.pageStart + NUM_ENTRIES_OFFSET)
        propFile.write((self.numEntries).to_bytes(Property.nodeIDByteLen,
            byteorder = sys.byteorder, signed=True))

        # write owner ID
        propFile.seek(self.pageStart + OWNER_ID_OFFSET)
        propFile.write((self.ownerID).to_bytes(Property.nodeIDByteLen,
            byteorder = sys.byteorder, signed=True))

        for prop in propertyData:
            writePropertyData(prop, propertyFile)

	def writePropertyData(self, prop, storeFile):
        propertyStartOffset = self.pageStart + DATA_OFFSET  + propertyIndex * Property.storageSize

        if DEBUG:
        # write property id
        storeFile.seek(propertyStartOffset + Property.PROPERTY_ID_OFFSET)
        storeFile.write(prop.getID().to_bytes(Property.propIDByteLen, 
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

        if DEBUG:
            print("writing key {0} at {1}".format(prop.key, propertyStartOffset + Property.KEY_OFFSET))

        storeFile.write(bytearray(prop.key, 'utf8'))

        # write value
        storeFile.seek(propertyStartOffset + Property.VALUE_OFFSET)
        
        if DEBUG:
            print("writing value {0} at {1}".format(prop.value, propertyStartOffset + Property.VALUE_OFFSET))

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
        if DEBUG:
            print("next property has index:{0}".format(prop.nextPropertyID))

            print("writing next property index {0} at {1}".format(prop.nextPropertyID, propertyStartOffset + Property.NEXT_PROPERTY_ID_OFFSET))
        storeFile.write(prop.nextPropertyID.to_bytes(Property.propIDByteLen, 
                byteorder = sys.byteorder, signed = True))

        if DEBUG:
            print()
