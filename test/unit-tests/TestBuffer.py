'''
A buffer for use in unit tests
'''

class TestBuffer(object):
    def __init__(self, bytesOut):
        self.BytesOut = bytesOut
        self.Index = 0

    def Read(self):
        if self.Index >= len(self.BytesOut):
            return None
        byte = self.BytesOut[self.Index]
        self.Index += 1
        return byte
