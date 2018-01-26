# Data pages are 4KB divisions of files that store a fixed number of records.
import threading 

class DataPage(object):
	# static variables
	# max page size is 4KB 
	MAX_PAGE_SIZE = 4000

	def __init__(self, pageID, datafile):
		self.pageID = pageID 
		self.pageLock = Lock()
		self.dirty = true
		self.file = datafile
		self.page_size = 0
		self.numEntries = 0
		self.ownerID = -1

	# read data object method

	# write data object method

	# create data object method

	# checks if page is empty
	def isEmpty(self):
		return (MAX_PAGE_SIZE - curr_page_size) > ENTRY_SIZE

	# acquire lock for given thread
	def lockPage(self, ownerID):
		self.pageLock.acquire()
		self.ownerID = ownerID

	# writes page to disk
	def syncPage():