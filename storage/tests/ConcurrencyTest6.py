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

# Creates a more complex deadlock condition, involving read locks and write locks, with
# multiple paths, and detects it.

##### Expected Result #########
'''
.....
inside detect deadlock for Thread0
for thread Thread0: owners are [<UserThread2(Thread2, started 123145318068224)>]
for thread Thread0: owner: Thread2
inside detect deadlock for Thread0
for thread Thread0: owners are [<UserThread0(Thread0, started 123145307557888)>]
for thread Thread0: owner: Thread0
Deadlock detected!
Deadlock detected!
Exception in thread Thread0:
Traceback (most recent call last):
  File "/Users/vshrivas/anaconda3/lib/python3.6/threading.py", line 916, in _bootstrap_inner
    self.run()
  File "ConcurrencyTest6.py", line 46, in run
    raise Exception('Deadlock detected!')
Exception: Deadlock detected!
'''

'''
This is just the bottom snippet of one example run through.
The top lines can vary depending on what order the threads execute in, but test should end with
an exception being thrown when deadlock condition is detected. The test also pauses for a while, this
doesn't mean the test is broken, just wait for a few seconds. This happens because threads are 
made to sleep to create a deadlock condition.
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
		time.sleep(10)
		nodeFile = NodeFile(0)
		page0 = self.args[0]
		page1 = self.args[1]

		UserThread0.waiting = page0
		print('thread 0 waiting on page {0} for read access'.format(UserThread0.waiting.pageID[1]))
		if LockManager.detectRWDeadlock(self, self):
			raise Exception('Deadlock detected!')

		page0.pageLock.acquire_read()
		LockManager.makePageOwner(self, page0)
		print('thread 0 got page 0 for reading')

		UserThread0.waiting = page1
		print('thread 0 waiting on page {0} for write access'.format(UserThread0.waiting.pageID[1]))
		if LockManager.detectRWDeadlock(self, self):
			raise Exception('Deadlock detected!')

		time.sleep(10)

		page1.pageLock.acquire_write()
		LockManager.makePageOwner(self, page1)
		print('thread 0 got page 1 for writing')

		threading.currentThread().waiting = None

		page1.pageLock.release_write()
		LockManager.removePageOwner(self, page1)
		page0.pageLock.release_read()
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
		page0 = self.args[0]
		page1 = self.args[1]

		UserThread1.waiting = page0
		print('thread 1 waiting on page {0} for read access'.format(UserThread1.waiting.pageID[1]))
		if LockManager.detectRWDeadlock(self, self):
			raise Exception('Deadlock detected!')

		page0.pageLock.acquire_read()
		LockManager.makePageOwner(self, page0)
		print('thread 1 got page 0 for reading')

		UserThread1.waiting = page1
		print('thread 1 waiting on page {0} for read access'.format(UserThread1.waiting.pageID[1]))
		if LockManager.detectRWDeadlock(self, self):
			raise Exception('Deadlock detected!')

		page1.pageLock.acquire_read()
		LockManager.makePageOwner(self, page1)
		print('thread 1 got page 1 for reading')

		threading.currentThread().waiting = None

		page1.pageLock.release_read()
		LockManager.removePageOwner(self, page1)

		page0.pageLock.release_read()
		LockManager.removePageOwner(self, page0)

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
		time.sleep(10)
		nodeFile = NodeFile(0)
		page0 = self.args[0]
		page1 = self.args[1]

		UserThread2.waiting = page1
		print('thread 2 waiting on page {0} for read access'.format(UserThread2.waiting.pageID[1]))
		if LockManager.detectRWDeadlock(self, self):
			raise Exception('Deadlock detected!')

		page1.pageLock.acquire_read()
		LockManager.makePageOwner(self, page1)
		print('thread 2 got page 1 for reading')

		UserThread2.waiting = page0
		print('thread 2 waiting on page {0} for write access'.format(UserThread2.waiting.pageID[1]))
		if LockManager.detectRWDeadlock(self, self):
			raise Exception('Deadlock detected!')

		time.sleep(20)

		page0.pageLock.acquire_write()
		LockManager.makePageOwner(self, page0)
		print('thread 2 got page 0 for writing')

		threading.currentThread().waiting = None

		page0.pageLock.release_write()
		LockManager.removePageOwner(self, page0)

		page1.pageLock.release_read()
		LockManager.removePageOwner(self, page1)

NodeStorageManager()

nodeFile = NodeFile(0)

page0 = nodeFile.createPage()
page1 = nodeFile.createPage()

u0 = UserThread0(args=(page0, page1,), name='Thread0')
u1 = UserThread1(args=(page0, page1,), name='Thread1')
u2 = UserThread2(args=(page0, page1,), name='Thread2')

print('page0 page ID:{0}'.format(page0.pageID[1]))
print('page1 page ID:{0}'.format(page1.pageID[1]))

u0.start()
u1.start()
u2.start()
