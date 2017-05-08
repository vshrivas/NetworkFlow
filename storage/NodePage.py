class NodePage:
	# node pages will be 1000 bytes
	PAGE_SIZE = 1000

	# NodePages will be instantiated through NodeFiles
	# which will pass in the pageNum
	def __init__(self, pageNum):
		self.pageNum = pageNum
