import sys

nodeFile = open('trialFile', 'wb')

nodeFile.seek(2)

nodeFile.write((5).to_bytes(4, byteorder = sys.byteorder, signed = True))

nodeFile.close()

nodeFile = open('trialFile', 'rb')

nodeFile.seek(2)

num = int.from_bytes(nodeFile.read(4), byteorder=sys.byteorder, signed=True)

print(num)