from NodePage import NodePage
from RelationshipPage import RelationshipPage
import random
import threading

class LockManager:
	# dictionary of pageID and owner(s) 
	pageOwners = {} # key: tuple(pageID), value: list of owners
	pageOwnersLock = threading.Lock()

	def detectRWDeadlock(userThread, startThread):
		print('inside detect deadlock for {0}'.format(startThread.name))
		#LockManager.pageOwnersLock.acquire()

		# user thread isn't trying to wait for any page, no deadlock
		if userThread.waiting is None:
			print('thread not waiting for any page')
			#LockManager.pageOwnersLock.release()
			return False

		pageWaiting = tuple(userThread.waiting.pageID)

		# page user thread is waiting on has no owners
		if LockManager.pageOwners.get(pageWaiting) is None:
			print('page not in keys, page has no owner')
			#LockManager.pageOwnersLock.release()
			return False

		# owner(s) of the page
		# can have multiple if they are reading page
		# only one if writing to page
		owners = LockManager.pageOwners.get(pageWaiting)
		print('for thread {0}: owners are {1}'.format(startThread.name, owners))

		#if owners is None:
			#return False

		for owner in owners:
			print('for thread {0}: owner: {1}'.format(startThread.name, owner.name))
			# found cycle back to starting thread
			if owner.name == startThread.name:
				#LockManager.pageOwnersLock.release()
				print('Deadlock detected!')
				return True

			# check if cycle can be found in future levels of this owner
			isDeadLocked = LockManager.detectRWDeadlock(owner, startThread)
			
			# found cycle at some future level
			if isDeadLocked:
				#LockManager.pageOwnersLock.release()
				print('Deadlock detected!')
				return True

		#LockManager.pageOwnersLock.release()
		return False

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
		print('making {0} owner of page {1}'.format(thread.name, page.pageID[1]))
		LockManager.pageOwnersLock.acquire()

		pageKey = tuple(page.pageID)

		if LockManager.pageOwners.get(pageKey) is None:
			print('page key was not in owner keys')
			LockManager.pageOwners[pageKey] = [thread]
		else:
			LockManager.pageOwners[pageKey].append(thread)

		print('owners are: {0}'.format(LockManager.pageOwners))

		LockManager.pageOwnersLock.release()

	def removePageOwner(thread, page):
		print('removing {0} owner of page {1}'.format(thread.name, page.pageID[1]))
		LockManager.pageOwnersLock.acquire()

		pageKey = tuple(page.pageID)

		if LockManager.pageOwners.get(pageKey) is None:
			return

		print('owners are for {0}: {1}'.format(thread.name, LockManager.pageOwners))

		LockManager.pageOwners[pageKey].remove(thread)

		if len(LockManager.pageOwners.get(pageKey)) == 0:
			del LockManager.pageOwners[pageKey]

		print('owners are: {0}'.format(LockManager.pageOwners))

		LockManager.pageOwnersLock.release()