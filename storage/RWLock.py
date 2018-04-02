import threading

# implements read-preferring read/write lock
class RWLock:
	def __init__(self):
		# lock to make sure numReaders is not corrupted
		self.lockReadersProtect = threading.Lock()
		# lock to make sure writers have exclusion
		self.lockWritersExclude = threading.Lock()
		# number of readers 
		self.numReaders = 0

	# acquires the read lock
	# lock can have multiple readers
	def acquire_read(self):
		self.lockReadersProtect.acquire()

		self.numReaders += 1
		# if have a single reader, acquire write lock
		# so no writers can have lock
		if self.numReaders == 1:
			self.lockWritersExclude.acquire()

		self.lockReadersProtect.release()

	# release the read lock
	def release_read(self):
		self.lockReadersProtect.acquire()

		self.numReaders -= 1
		# no more readers, release lock for writers
		if self.numReaders == 0:
			self.lockWritersExclude.release()

		self.lockReadersProtect.release()

	# acquire the write lock
	def acquire_write(self):
		self.lockWritersExclude.acquire()

	# release the write lock
	def release_write(self):
		self.lockWritersExclude.release()