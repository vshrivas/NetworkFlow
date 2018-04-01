# Data pages are 4KB divisions of files that store a fixed number of records.
# Pages should record the number of records, page owner, and other metadata 
# at the beginning of the page

# page IDs are unique across files, and allow storage managers to determine which file a page is in 
import threading 
from .RWLock import RWLock

class DataPage(object):
	# static variables
	# max page size is 4KB 
	MAX_PAGE_ENTRIES = 1

	# meta data includes:
		# number of entries in this page
		# owner of the page
	NUM_ENTRIES_SIZE = 50
	OWNER_ID_SIZE = 50
	METADATA_SIZE = 100 

	NUM_ENTRIES_OFFSET = 0
	OWNER_ID_OFFSET = NUM_ENTRIES_SIZE
	DATA_OFFSET = OWNER_ID_OFFSET + OWNER_ID_SIZE

	def __init__(self, pageID, datafile):
		# pageID[0] 
			# 0 Node
			# 1 Relationship
			# 2 Property
			# 3 Label
		self.pageID = pageID
		self.pageLock = RWLock()
		self.dirty = True
		self.file = datafile
		self.pageSize = 0
		self.numEntries = 0
		self.ownerID = -1

	# read data object method

	# write data object method

	# create data object method

	# checks if page is empty
	def isEmpty(self):
		return (MAX_PAGE_SIZE - curr_page_size) > ENTRY_SIZE

		def getPageIndex():
			return pageID[1]

	# acquire lock for given thread
	def lockPage(self, ownerID):
		self.pageLock.acquire()
		self.ownerID = ownerID

	def getPageIndex(self):
		return self.pageID[1]