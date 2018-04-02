from .Node import Node
from .NodePage import NodePage
from .Property import Property
from .Relationship import Relationship
from .Label import Label
from .NodeFile import NodeFile
from .BufferManager import BufferManager
from .RelationshipStorageManager import RelationshipStorageManager
from .DataPage import DataPage
from .LockManager import LockManager
import threading
import sys, struct, os


''' PropertyStorageManager is responsible for handling the top level methods for creating, reading,
and writing properties. Creates new property pages and files when necessary. Has a meta data file
to keep track of number of property files. '''
class PropertyStorageManager():
    numPropFiles = 0
    directory = "propstore"

    def __init__(self):
        # open property storage meta data file
        # read number of node files 
        self.fileName = "metadata"
        self.filePath = os.path.join(PropertyStorageManager.directory, self.fileName)

        # storage manager metadata file exists
        if os.path.exists(self.filePath):
            metadataFile = open(self.filePath, 'r+b')
            PropertyStorageManager.numPropFiles = int.from_bytes(metadataFile.read(Property.propIDByteLen), sys.byteorder, signed=True)

        # storage manager metadata file does not exist
        else:
            # property store directory does not exist, make it
            if not os.path.exists(self.directory):
                os.makedirs(PropertyStorageManager.directory)

            # open metadata file    
            metadataFile = open(self.filePath, 'wb')
            # write number of node files to first 3 bytes of node storage metadata file
            metadataFile.write((0).to_bytes(Property.propIDByteLen,
                byteorder = sys.byteorder, signed=True))

        # there are no property files
        if PropertyStorageManager.numPropFiles == 0:
            # make a new one 
            PropertyFile(0)
            PropertyStorageManager.numPropFiles += 1

            metadataFile = open(self.filePath, 'r+b')
            metadataFile.write((PropertyStorageManager.numPropFiles).to_bytes(Property.propIDByteLen,
                byteorder = sys.byteorder, signed=True))

    # takes in property ID, reads and returns property
    def readProperty(propertyID):
        pageID = propertyID[0]
        propertyIndex = propertyID[1]

        pageIndex = pageID[1]

        fileID = pageIndex / PropertyFile.MAX_PAGES

        # use buffer manager to retrieve page from memory
        # will load page into memory if wasn't there
        propertyPage = BufferManager.getPropertyPage(pageIndex, PropertyFile(int(fileID)))

        # detect potential deadlock
        threading.currentThread().waiting = propertyPage
        if LockManager.detectRWDeadlock(threading.currentThread(), threading.currentThread()):
            raise Exception('Deadlock detected!')

        # acquire read lock
        propertyPage.pageLock.acquire_read()
        threading.currentThread().waiting = None
        LockManager.makePageOwner(threading.currentThread(), propertyPage)

        property = propertyPage.readNode(nodeIndex)

        # release lock
        propertyPage.pageLock.release_read()
        LockManager.removePageOwner(threading.currentThread(), propertyPage)
        return property

    # takes in property to write or create, returns same property
    def writeProperty(property, create):
        propID = property.getID()
        pageID = propID[0]           # pageID[0] = 0, pageID[1] = pageIndex

        pageIndex = pageID[1]        

        fileID = pageIndex / PropertyFile.MAX_PAGES

        # use buffer manager to retrieve page from memory
        # will load page into memory if wasn't there
        propPage = BufferManager.getPropertyPage(pageIndex, PropertyFile(int(fileID)))

        # check for potential deadlock 
        threading.currentThread().waiting = propPage
        if LockManager.detectRWDeadlock(threading.currentThread(), threading.currentThread()):
            raise Exception('Deadlock detected!')

        # acquire write lock
        propPage.pageLock.acquire_write()
        threading.currentThread().waiting = None
        LockManager.makePageOwner(threading.currentThread(), propPage)

        propPage.writeProperty(property, create)

        # release write lock
        propPage.pageLock.release_write()
        LockManager.removePageOwner(threading.currentThread(), propPage)
        return property

    # returns list of linked properties based on first property ID
    def getPropertyChain(firstPropID):
        nextPropID = firstPropID
        chainedProperties = []

        # while there is a next property
        while nextPropID[1] != -1:
            prop = PropertyStorageManager.readProperty(nextPropID)
            chainedProperties.append(prop)

            nextPropID = prop.nextPropertyID

        return chainedProperties

    # creates a property based on a given key and value
    def createProperty(key, value):
        # get prop file
        lastFileID = PropertyStorageManager.numPropFiles - 1
        lastFile = PropertyFile(lastFileID)

        if lastFile.numPages == 0:
            lastFile.createPage()

        # get last property page
        lastPage = BufferManager.getPropertyPage(lastFile.numPages - 1, lastFile)
        
        propPage = lastPage
        propFile = lastFile

        # if last page is full
        if lastPage.numEntries == DataPage.MAX_PAGE_ENTRIES:
            # if file is at max pages
            if lastFile.numPages == PropertyFile.MAX_PAGES:
                # make a new file
                newLastFile = PropertyFile(lastFileID + 1)
                PropertyStorageManager.numPropFiles += 1

                metadataFile = open(self.filePath, 'r+b')
                metadataFile.write((PropertyStorageManager.numPropFiles).to_bytes(Property.propIDByteLen,
                byteorder = sys.byteorder, signed=True))

                propFile = newLastFile

                # make a new page in the file
                newLastFile.createPage()
                propPage = BufferManager.getPropertyPage(newLastFile.numPages - 1, newLastFile)

            # else make new page
            else:
                lastFile.createPage()
                propPage = BufferManager.getPropertyPage(lastFile.numPages - 1, lastFile)

        propID = [[2, propPage.pageID[1]], propPage.numEntries]
        prop = Property(key, value, propFile, propID, [[2, 0], -1])
        
        print('creating prop {0} in page {1}'.format(propPage.numEntries, propPage.pageID[1]))

        PropertyStorageManager.writeProperty(prop, True)

        return prop