'''
A buffer for use in unit tests
'''

class TestBuffer(object):
    def __init__(self, bytesOut):
        self.BytesOut = bytesOut
        self.BytesIn = []
        self.EndOfFile = False
        self.Index = 0

    def Read(self):
        if self.Index >= len(self.BytesOut):
            self.EndOfFile = True
            return None
        byte = self.BytesOut[self.Index]
        self.Index += 1
        return byte

    def Write(self, byte):
        self.BytesIn.append(byte)

    def WriteStr(self, string):
        byteArray = bytes([ord(x) for x in string])
        for b in byteArray:
            self.Write(b)

    def __repr__(self): #Useful for debugging
        return "EOF: {0}, Index: {1}\n{2} Bytes In: {3}\n{4} Bytes Out: {5}" \
            .format(self.EndOfFile, self.Index, len(self.BytesIn), self.BytesIn, len(self.BytesOut), self.BytesOut)
