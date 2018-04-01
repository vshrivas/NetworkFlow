from NodePage import NodePage
from RelationshipPage import RelationshipPage
import random
import threading

class LockManager(Object):
	# dictionary of pageID and owner 
	pageOwners = {}

	# checks if there is a potential for deadlock
	# returns false if there isn't deadlock
	# returns true if there is deadlock
	def detectDeadlock(userThread):
		# userThread is requesting lock on this page

		# we will trace back the chain of threads waiting on pages
		# where t1 is the current thread that we want to check will cause deadlock on the system
		# if t1 -> t2 -> t3 ... t1, where -> takes us to the thread holding the lock we need, then
		# letting t1 wait on the lock will cause deadlock in the system

		nextThread = LockManager.pageOwners[tuple(userThread.waiting.pageID)]

		# while nextThread isn't none (chain ends)
		# or chain circles back to userThread
		# there is no other end possibility, since if we circled back to some other thread, deadlock
		# would have existed in the system 
		while(nextThread != None or nextThread != userThread) {
			# nextThread is the thread we 
			nextThread = LockManager.pageOwners[tuple(nextThread.waiting.pageID)]
		}

		if nextThread == None:
			return False

		else:
			return True


	def makePageOwner(thread, page):
		LockManager.pageOwners[tuple(page.pageID)] = thread

	def removePageOwner(page):
		del LockManager.pageOwners[tuple(page.pageID)]