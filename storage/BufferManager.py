class BufferManager(object):
    # dictionary of buffered pages (shared across pages of nodes, relationships, properties, and labels)
    # pageID: dataPage
    cachedPages = {}

    numPages = n

    # maximum size of cache is 1 MB, or 250 4 KB pages
    MAX_PAGES = 250

    # takes in pageID 
    # returns page if found, None if not found
    def getPage(pageID):
        # uses dictionary to find page corresponding to pageID
        # returns the page object associated with it
        for key in cachedPages:
            if key == pageID:
                return cachedPages[key]

        return None


    def addPage(pageID):
        # can read from disk to get page specific to pageID
        # may need to evict page if no space
        if cacheFull():
            evictPage()
            


    def evictPage():
        # runs an eviction algorithm to evict a page from cache
        # do not evict locked pages

    def cacheFull():
        return numPages == MAX_PAGES