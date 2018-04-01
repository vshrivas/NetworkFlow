from NodePage import NodePage
from RelationshipPage import RelationshipPage
import random
import threading

class LockManager:
	# dictionary of pageID and owner 
	pageOwners = {}
	pageOwnersLock = threading.Lock()

	# checks if there is a potential for deadlock
	# returns false if there isn't deadlock
	# returns true if there is deadlock
	def detectDeadlock(userThread):
		# userThread is requesting lock on this page

		# we will trace back the chain of threads waiting on pages
		# where t1 is the current thread that we want to check will cause deadlock on the system
		# if t1 -> t2 -> t3 ... t1, where -> takes us to the thread holding the lock we need, then
		# letting t1 wait on the lock will cause deadlock in the system

		if userThread.waiting is None:
			return False

		pageOwnerKey = tuple(userThread.waiting.pageID)

		# page has an owner
		if pageOwnerKey in LockManager.pageOwners.keys():
			nextThread = LockManager.pageOwners[tuple(userThread.waiting.pageID)]
			if nextThread.waiting is None:
				return False
		# page has no owner
		else:
			return False

		# while nextThread isn't none (chain ends)
		# or chain circles back to userThread
		# there is no other end possibility, since if we circled back to some other thread, deadlock
		# would have existed in the system 
		while(nextThread is not None and nextThread.name != userThread.name):
			pageOwnerKey = tuple(nextThread.waiting.pageID)

			# nextThread is the thread we 
			if nextThread.waiting is None:
				nextThread = None
			elif pageOwnerKey in LockManager.pageOwners.keys():
				nextThread = LockManager.pageOwners[tuple(nextThread.waiting.pageID)]
			else:
				nextThread = None

		if nextThread is None:
			print('No deadlock detected')
			return False

		elif nextThread.name == userThread.name:
			print('Deadlock condition detected!')
			userThread.waiting = None
			return True

		else:
			print('next thread name: {0}'.format(nextThread.name))
			print('user thread name: {0}'.format(userThread.name))
			print('Error: should never reach this!')
			return True


	def makePageOwner(thread, page):
		LockManager.pageOwnersLock.acquire()
		LockManager.pageOwners[tuple(page.pageID)] = thread
		LockManager.pageOwnersLock.release()

	def removePageOwner(page):
		LockManager.pageOwnersLock.acquire()
		del LockManager.pageOwners[tuple(page.pageID)]
		LockManager.pageOwnersLock.release()