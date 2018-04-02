from .NodePage import NodePage
from .RelationshipPage import RelationshipPage
import random


''' BufferManager handles shared cache of in-memory pages of all data types.
All pages accesses go through the buffer manager. '''
class BufferManager(object):
    # dictionary of buffered pages (shared across pages of nodes, relationships, properties, and labels)
    # key: tuple(pageID)
    # value: dataPage
    cachedPages = {}

    # size of buffer
    numPages = 0

    # maximum number of pages allowed in buffer
    MAX_PAGES = 3

    # takes in node page index, returns node page
    def getNodePage(pageIndex, datafile):
        # check if page is in cache
        for key in BufferManager.cachedPages:
            if key[0] == 0 and key[1] == pageIndex:
                return BufferManager.cachedPages[key]

        # evict if cache is full
        if BufferManager.cacheFull():
            BufferManager.evictPage()

        # load page into memory
        nodePage = NodePage(pageIndex, datafile, False)

        BufferManager.cachedPages[tuple(nodePage.pageID)] = nodePage

        BufferManager.numPages += 1

        return nodePage

    # takes in relationship page index, returns relationship page
    def getRelationshipPage(pageIndex, datafile):
        # check if page is in cache
        for key in BufferManager.cachedPages:
            if key[0] == 1 and key[1] == pageIndex:
                return BufferManager.cachedPages[key]

        # evict page if cache is full
        if BufferManager.cacheFull():
            BufferManager.evictPage()

        # load page into memory
        relPage = RelationshipPage(pageIndex, datafile, False)

        BufferManager.cachedPages[tuple(relPage.pageID)] = relPage

        BufferManager.numPages += 1

        return relPage

    # takes in property page index, returns property page
    def getPropertyPage(pageIndex, datafile):
        # check if page is in cache
        for key in BufferManager.cachedPages:
            if key[0] == 2 and key[1] == pageIndex:
                return BufferManager.cachedPages[key]

        # evict page if cache is full
        if BufferManager.cacheFull():
            BufferManager.evictPage()

        # load page into memory
        propPage = PropertyPage(pageIndex, datafile, False)

        BufferManager.cachedPages[tuple(propPage.pageID)] = relPage

        BufferManager.numPages += 1

        return relPage

    # takes in label page index, returns label page
    def getLabelPage(pageIndex, datafile):
        # check if page is in cache
        for key in BufferManager.cachedPages:
            if key[0] == 3 and key[1] == pageIndex:
                return BufferManager.cachedPages[key]

        # evict page if cache is full
        if BufferManager.cacheFull():
            BufferManager.evictPage()

        # load page into memory
        labelPage = LabelPage(pageIndex, datafile, False)

        BufferManager.cachedPages[tuple(labelPage.pageID)] = relPage

        BufferManager.numPages += 1

        return relPage

    # evicts a page from buffer
    def evictPage():
        # runs a random eviction algorithm
        randomPageID = random.choice(list(BufferManager.cachedPages.keys()))

        randomPage = BufferManager.cachedPages[tuple(randomPageID)]

        randomPage.writePageData()

        del BufferManager.cachedPages[tuple(randomPageID)]

        BufferManager.numPages -= 1

    # returns true if buffer cache is full
    def cacheFull():
        return BufferManager.numPages == BufferManager.MAX_PAGES