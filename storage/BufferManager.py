from NodePage import NodePage
from RelationshipPage import RelationshipPage

class BufferManager(object):
    # dictionary of buffered pages (shared across pages of nodes, relationships, properties, and labels)
    # pageID: dataPage
    cachedPages = {}

    numPages = 10

    # maximum size of cache is 1 MB, or 250 4 KB pages
    MAX_PAGES = 250

    # takes in pageID 
    # returns page if found, None if not found
    def getNodePage(pageIndex, datafile):
        # uses dictionary to find page corresponding to pageID
        # returns the page object associated with it
        '''for key in cachedPages:
            if key == pageID:
                return cachedPages[key]

        return None'''
        return NodePage(0, datafile, False)


    def getRelationshipPage(pageIndex, datafile):
        return RelationshipPage(0, datafile, False)


    def addPage(pageID):
        # can read from disk to get page specific to pageID
        # may need to evict page if no space
        if cacheFull():
            evictPage()
            


    def evictPage():
        # runs an eviction algorithm to evict a page from cache
        # do not evict locked pages
        pass

    def cacheFull():
        return numPages == MAX_PAGES