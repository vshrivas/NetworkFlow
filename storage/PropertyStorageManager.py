class PropertyStorageManager(StorageManager):
	def readProperty(propertyID):
		pageID = propertyID[0]
        propertyIndex = propertyID[1]

        pageIndex = pageID[1]

        # use buffer manager to retrieve page from memory
		# will load page into memory if wasn't there
        propertyPage = BufferManager.getPropertyPage(pageIndex, self)
        return propertyPage.readNode(nodeIndex)

	def writeProperties(properties):
		# write properties to property file
        for propIndex in range(0, len(properties)):
            prop = properties[propIndex]
            if DEBUG:
                print("writing {0} property ".format(prop.getID()))

            # write last property
            if propIndex == len(properties) - 1:
                if DEBUG:
                    print("no next property")
                # A placeholder property since there is no next property
                nullProperty = Property("", "", "", -1)
                self.writeProperty(prop, nullProperty)
            # write property that's not last property
            else:
                self.writeProperty(prop, properties[propIndex + 1])

	def openFile(pageID):
		pass

	def writeProperty(property, nextProperty):
		pageID = (property.getID())[0] 			# pageID[0] = 0, pageID[1] = pageIndex
		propIndex = (property.getID())[1]

		fileNo = pageID / DataFile.MAX_FILE_PAGES
		propertyFile = propertyFiles[fileNo]

		propertyFile.writeProperty()


	def getProperty(propID, propertyStore, propertyStartOffset):
		# find ID
        propertyStore.seek(propertyStartOffset)

        if DEBUG:
            print("seek to {0} for ID". format(propertyStartOffset))

        ID = int.from_bytes(propertyStore.read(Property.propIDByteLen), sys.byteorder, signed=True)
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

        # initialize property object with key and value and add to relationship
        prop = Property(key, value, propertyFile, nextPropID)

	def getPropertyChain(firstPropID):
		chainedProperties = []

        if DEBUG:
        	print ('Reading in properties for rel {0}...'.format(nextRelID))

	    # while there is a next property for the relationship
	    while nextPropID != -1:
	        if DEBUG:
	            print()
	            print('for rel: {0}'.format(nextRelID))
	            print('first prop id: {0}'. format(firstRelPropID))
	            print(nextPropID)
	        
	        pageID = propID[0]
        	propIndex = propID[1]

    		# find starting offset of property
        	propertyStartOffset = propIndex * Property.storageSize + Property.propIDByteLen

	        propertyStore = openFile(pageID)

	        prop = getProperty(nextPropID, propertyStore)

	        chainedProperties.append(prop)

	        # find next property id
	        propertyStore.seek(propertyStartOffset + Property.NEXT_PROPERTY_ID_OFFSET)

	        if DEBUG:
	            print("seek to {0} for next property id". format(propertyStartOffset + Property.NEXT_PROPERTY_ID_OFFSET))
	        nextPropID = int.from_bytes(propertyStore.read(Property.propIDByteLen), sys.byteorder, signed=True)
	        if DEBUG:
	            print("next prop id is {0}".format(nextPropID)) 


	     return chainedProperties