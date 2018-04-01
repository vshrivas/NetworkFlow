import threading

# implements read-preferring read/write lock

class RWLock:
	def __init__(self):
		self.lockReadersProtect = threading.Lock()
		self.lockWritersExclude = threading.Lock()
		self.numReaders = 0

	def acquire_read(self):
		self.lockReadersProtect.acquire()

		self.numReaders += 1
		if self.numReaders == 1:
			self.lockWritersExclude.acquire()

		self.lockReadersProtect.release()

	def release_read(self):
		self.lockReadersProtect.acquire()

		self.numReaders -= 1
		if self.numReaders == 0:
			self.lockWritersExclude.release()

		self.lockReadersProtect.release()

	def acquire_write(self):
		self.lockWritersExclude.acquire()

	def release_write(self):
		self.lockWritersExclude.release()