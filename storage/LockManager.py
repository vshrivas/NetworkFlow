class LockManager(Object):
	# dictionary of pageID and owner 
	pageOwners = {}

	def detectDeadlock(userThread, pageID):
		# userThread is requesting lock on this page

		# we will trace back the chain of threads waiting on pages
		# where t1 is the current thread that we want to check will cause deadlock on the system
		# if t1 -> t2 -> t3 ... t1, where -> takes us to the thread holding the lock we need, then
		# letting t1 wait on the lock will cause deadlock in the system

		nextThread = pageOwners[pageID]

		# while nextThread isn't none (chain ends)
		# or chain circles back to userThread
		# there is no other end possibility, since if we circled 
		while(nextThread != None or nextThread != userThread) > 0) {

		}