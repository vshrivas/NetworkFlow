from .NodePage import NodePage
from .RelationshipPage import RelationshipPage
import random

class BufferManager(object):
    # dictionary of buffered pages (shared across pages of nodes, relationships, properties, and labels)
    # pageID: dataPage
    cachedPages = {}

    # size of buffer
    numPages = 0

    # maximum size of cache is 1 MB, or 250 4 KB pages
    MAX_PAGES = 3

    # takes in pageID 
    # returns page if found, None if not found
    def getNodePage(pageIndex, datafile):
        # uses dictionary to find page corresponding to pageID
        # returns the page object associated with it
        for key in BufferManager.cachedPages:
            if key[0] == 0 and key[1] == pageIndex:
                return BufferManager.cachedPages[key]

        if BufferManager.cacheFull():
            BufferManager.evictPage()

        nodePage = NodePage(pageIndex, datafile, False)

        BufferManager.cachedPages[tuple(nodePage.pageID)] = nodePage

        BufferManager.numPages += 1

        return nodePage

    def getRelationshipPage(pageIndex, datafile):
        # uses dictionary to find page corresponding to pageID
        # returns the page object associated with it
        for key in BufferManager.cachedPages:
            if key[0] == 1 and key[1] == pageIndex:
                return BufferManager.cachedPages[key]

        if BufferManager.cacheFull():
            BufferManager.evictPage()

        relPage = RelationshipPage(pageIndex, datafile, False)

        BufferManager.cachedPages[tuple(relPage.pageID)] = relPage

        BufferManager.numPages += 1

        return relPage

    def getPropertyPage(pageIndex, datafile):
        # uses dictionary to find page corresponding to pageID
        # returns the page object associated with it
        for key in BufferManager.cachedPages:
            if key[0] == 2 and key[1] == pageIndex:
                return BufferManager.cachedPages[key]

        if BufferManager.cacheFull():
            BufferManager.evictPage()

        propPage = PropertyPage(pageIndex, datafile, False)

        BufferManager.cachedPages[tuple(propPage.pageID)] = relPage

        BufferManager.numPages += 1

        return relPage

    def getLabelPage(pageIndex, datafile):
        # uses dictionary to find page corresponding to pageID
        # returns the page object associated with it
        for key in BufferManager.cachedPages:
            if key[0] == 3 and key[1] == pageIndex:
                return BufferManager.cachedPages[key]

        if BufferManager.cacheFull():
            BufferManager.evictPage()

        labelPage = LabelPage(pageIndex, datafile, False)

        BufferManager.cachedPages[tuple(labelPage.pageID)] = relPage

        BufferManager.numPages += 1

        return relPage


    def evictPage():
        # runs a random eviction algorithm
        randomPageID = random.choice(list(BufferManager.cachedPages.keys()))

        randomPage = BufferManager.cachedPages[tuple(randomPageID)]

        randomPage.writePageData()

        del BufferManager.cachedPages[tuple(randomPageID)]

        BufferManager.numPages -= 1


    def cacheFull():
        return BufferManager.numPages == BufferManager.MAX_PAGES