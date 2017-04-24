# Class: Property

# Storage: 
# Bytes 1-4: Property ID
# Bytes 5-8: Key
# Bytes 9-12: Value
# Bytes 13-16: Next Property ID

class Property:
	PROPERTY_ID_OFFSET = 0
	KEY_OFFSET = 4
	VALUE_OFFSET = 8
	NEXT_PROPERTY_ID_OFFSET = 12

	storageSize = 16
	numProperties = 0

	def _init_(self, propertyID=numProperties, key, value, propertyFile):
		self.key = key
		self.value = value

		self.propertyID = numProperties
		numProperties += 1

		self.propertyFile = propertyFile

		self.startOffset = self.propertyID * Property.storageSize

	def getKey():
		return self.key

	def getValue():
		return self.value

	def getPropertyFile():
		return self.propertyFile

	def getID():
		return self.propertyID

	def writeProperty(nextProp):
		# open property file
		storeFileName = propertyFile.getName()
		storeFile = open(storeFileName, 'a')

		# write property id
		storeFile.seek(self.startOffset + PROPERTY_ID_OFFSET)
		storeFile.write(self.propertyID)

		# write key
		storeFile.seek(self.startOffset + KEY_OFFSET)
		storeFile.write(self.key)

		# write value
		storeFile.seek(self.startOffset + VALUE_OFFSET)
		storeFile.write(self.value)

		# write next property id
		storeFile.seek(self.startOffset + NEXT_PROPERTY_ID_OFFSET)
		storeFile.write(nextProp.getID())



