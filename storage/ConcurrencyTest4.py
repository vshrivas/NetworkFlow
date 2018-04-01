import threading 
import time
from Node import Node
from Property import Property
from Relationship import Relationship
from Label import Label
from NodeStorageManager import NodeStorageManager
from RelationshipStorageManager import RelationshipStorageManager
from NodeFile import NodeFile
from BufferManager import BufferManager
from LockManager import LockManager

# creates a deadlock condition and then detects it 
'''
This test is now deprecated. 
Was used to test LockManager.detectDeadlock method when LockManager
only detected deadlock for write locks. Now we have transitioned to using the
LockManager.detectRWDeadlock to detect multi-path deadlock where each page can have multiple
owners due to reads, and the LockManager.detectDeadlock method is deprecated. The test is included
just to provide a progression for concurrency testing.
'''

class UserThread0(threading.Thread):
	waiting = None

	def __init__(self, group=None, target=None, name=None,
                 args=(), kwargs=None):
		super(UserThread0,self).__init__(group=group, target=target, 
			              name=name)
		self.args = args
		self.kwargs = kwargs
		return

	# 'name' of threads is used to specify what page they're waiting for
	# has lock on page 0, wants lock on page 1
	def run(self):
		nodeFile = NodeFile(0)
		page0 = self.args[0]
		page1 = self.args[1]

		UserThread0.waiting = page0
		print('thread 0 waiting on page {0}'.format(UserThread0.waiting.pageID[1]))
		if LockManager.detectDeadlock(self):
			raise Exception('Deadlock detected!')

		page0.pageLock.acquire_write()
		LockManager.makePageOwner(self, page0)
		print('thread 0 got page 0')

		UserThread0.waiting = page1
		print('thread 0 waiting on page {0}'.format(threading.currentThread().waiting.pageID[1]))
		if LockManager.detectDeadlock(self):
			raise Exception('Deadlock detected!')

		time.sleep(10)

		page1.pageLock.acquire_write()
		LockManager.makePageOwner(self, page1)
		print('thread 0 got page 1')

		threading.currentThread().waiting = None

		page1.pageLock.release_write()
		LockManager.removePageOwner(self, page1)
		page0.pageLock.release_write()
		LockManager.removePageOwner(self, page0)

class UserThread1(threading.Thread):
	waiting = None

	def __init__(self, group=None, target=None, name=None,
                 args=(), kwargs=None):
		super(UserThread1,self).__init__(group=group, target=target, 
			              name=name)
		self.args = args
		self.kwargs = kwargs
		return

	# has lock on page 1, wants lock on page 2
	def run(self):
		nodeFile = NodeFile(0)
		page1 = self.args[0]
		page2 = self.args[1]

		UserThread1.waiting = page1
		print('thread 1 waiting on page {0}'.format(UserThread1.waiting.pageID[1]))
		if LockManager.detectDeadlock(self):
			raise Exception('Deadlock detected!')

		page1.pageLock.acquire_write()
		LockManager.makePageOwner(self, page1)
		print('thread 1 got page 1')

		UserThread1.waiting = page2
		print('thread 1 waiting on page {0}'.format(UserThread1.waiting.pageID[1]))
		if LockManager.detectDeadlock(self):
			raise Exception('Deadlock detected!')

		time.sleep(10)

		page2.pageLock.acquire_write()
		LockManager.makePageOwner(self, page2)
		print('thread 1 got page 2')

		threading.currentThread().waiting = None

		page2.pageLock.release_write()
		LockManager.removePageOwner(self, page2)

		page1.pageLock.release_write()
		LockManager.removePageOwner(self, page2)

class UserThread2(threading.Thread):
	waiting = None

	def __init__(self, group=None, target=None, name=None,
                 args=(), kwargs=None):
		super(UserThread2,self).__init__(group=group, target=target, 
			              name=name)
		self.args = args
		self.kwargs = kwargs
		return

	# has lock on page 2, wants lock on page 0
	def run(self):
		nodeFile = NodeFile(0)
		page0 = self.args[1]
		page2 = self.args[0]

		UserThread2.waiting = page2
		print('thread 2 waiting on page {0}'.format(threading.currentThread().waiting.pageID[1]))
		if LockManager.detectDeadlock(self):
			raise Exception('Deadlock detected!')

		page2.pageLock.acquire_write()
		LockManager.makePageOwner(self, page2)
		print('thread 2 got page 2')

		UserThread2.waiting = page0
		print('thread 2 waiting on page {0}'.format(threading.currentThread().waiting.pageID[1]))
		if LockManager.detectDeadlock(self):
			raise Exception('Deadlock detected!')

		time.sleep(10)

		page0.pageLock.acquire_write()
		LockManager.makePageOwner(self, page0)
		print('thread 2 got page 0')

		threading.currentThread().waiting = None

		page0.pageLock.release_write()
		LockManager.removePageOwner(self, page0)

		page2.pageLock.release_write()
		LockManager.removePageOwner(self, page2)

NodeStorageManager()

nodeFile = NodeFile(0)

page0 = nodeFile.createPage()
page1 = nodeFile.createPage()
page2 = nodeFile.createPage()

u0 = UserThread0(args=(page0, page1,))
u1 = UserThread1(args=(page1, page2,))
u2 = UserThread2(args=(page2, page0,))

print('page0 page ID:{0}'.format(page0.pageID[1]))
print('page1 page ID:{0}'.format(page1.pageID[1]))
print('page2 page ID:{0}'.format(page2.pageID[1]))

u0.start()
u1.start()
u2.start()