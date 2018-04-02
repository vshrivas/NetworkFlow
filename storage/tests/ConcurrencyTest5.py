import threading 
import time
from storage.Node import Node
from storage.Property import Property
from storage.Relationship import Relationship
from storage.Label import Label
from storage.NodeStorageManager import NodeStorageManager
from storage.RelationshipStorageManager import RelationshipStorageManager
from storage.NodeFile import NodeFile
from storage.BufferManager import BufferManager
from storage.LockManager import LockManager

# Creates a deadlock condition, and detects it, using read/write deadlock detection.

###### Expected Result Example ############
'''
inside detect deadlock for Thread-3
for thread Thread-3: owners are [<UserThread2(Thread-3, started 123145318068224)>]
for thread Thread-3: owner: Thread-3
Deadlock detected!
Deadlock detected!
Deadlock detected!
Exception in thread Thread-3:
Traceback (most recent call last):
  File "/Users/vshrivas/anaconda3/lib/python3.6/threading.py", line 916, in _bootstrap_inner
    self.run()
  File "ConcurrencyTest5.py", line 134, in run
    raise Exception('Deadlock detected!')
Exception: Deadlock detected!
'''
'''
This is just the bottom snippet of one example run through.
The top lines can vary depending on what order the threads execute in, but test should end with
an exception being thrown when deadlock condition is detected. 
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
		if LockManager.detectRWDeadlock(self, self):
			raise Exception('Deadlock detected!')

		page0.pageLock.acquire_write()
		LockManager.makePageOwner(self, page0)
		print('thread 0 got page 0')

		UserThread0.waiting = page1
		print('thread 0 waiting on page {0}'.format(threading.currentThread().waiting.pageID[1]))
		if LockManager.detectRWDeadlock(self, self):
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
		if LockManager.detectRWDeadlock(self, self):
			raise Exception('Deadlock detected!')

		page1.pageLock.acquire_write()
		LockManager.makePageOwner(self, page1)
		print('thread 1 got page 1')

		UserThread1.waiting = page2
		print('thread 1 waiting on page {0}'.format(UserThread1.waiting.pageID[1]))
		if LockManager.detectRWDeadlock(self, self):
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
		if LockManager.detectRWDeadlock(self, self):
			raise Exception('Deadlock detected!')

		page2.pageLock.acquire_write()
		LockManager.makePageOwner(self, page2)
		print('thread 2 got page 2')

		UserThread2.waiting = page0
		print('thread 2 waiting on page {0}'.format(threading.currentThread().waiting.pageID[1]))
		if LockManager.detectRWDeadlock(self, self):
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