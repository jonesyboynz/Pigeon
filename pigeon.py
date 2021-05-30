#Imports
import argparse
import os
import json
import ntpath
import sys

#Global vairables
VERSION = "1.0.0"
DEFAULT_BUFFER_SIZE = 10000
DEFAULT_FILENAME = "message"
DEFAULT_EXTENSION = ".pgy"
DEFAULT_CODEBOOK="""
{"0": ["+z"], "1": ["+y"], "2": ["+x"], "3": ["+w"], "4": ["+v"], "5": ["+u"], "6": ["+t"], "7": ["+s"], "8": ["+r"], "9": ["+q"], "10": ["+p"], "11": ["+o"], "12": ["+n"], "13": ["+m"], "14": ["+l"], "15": ["+k"], "16": ["+j"], "17": ["+i"], "18": ["+h"], "19": ["+g"], "20": ["+f"], "21": ["+e"], "22": ["+d"], "23": ["+c"], "24": ["+b"], "25": ["+a"], "26": ["+9"], "27": ["+8"], "28": ["+7"], "29": ["+6"], "30": ["+5"], "31": ["+4"], "32": ["+3"], "33": ["+2"], "34": ["+1"], "35": ["+0"], "36": ["+Z"], "37": ["+Y"], "38": ["+X"], "39": ["+W"], "40": ["+V"], "41": ["+U"], "42": ["+T"], "43": ["+S"], "44": ["+R"], "45": ["+Q"], "46": ["+P"], "47": ["+O"], "48": ["z"], "49": ["y"], "50": ["x"], "51": ["w"], "52": ["v"], "53": ["u"], "54": ["t"], "55": ["s"], "56": ["r"], "57": ["q"], "58": ["+N"], "59": ["+M"], "60": ["+L"], "61": ["+K"], "62": ["+J"], "63": ["+I"], "64": ["+H"], "65": ["p"], "66": ["o"], "67": ["n"], "68": ["m"], "69": ["l"], "70": ["k"], "71": ["j"], "72": ["i"], "73": ["h"], "74": ["g"], "75": ["f"], "76": ["e"], "77": ["d"], "78": ["c"], "79": ["b"], "80": ["a"], "81": ["9"], "82": ["8"], "83": ["7"], "84": ["6"], "85": ["5"], "86": ["4"], "87": ["3"], "88": ["2"], "89": ["1"], "90": ["0"], "91": ["+G"], "92": ["+F"], "93": ["+E"], "94": ["+D"], "95": ["+C"], "96": ["+B"], "97": ["Z"], "98": ["Y"], "99": ["X"], "100": ["W"], "101": ["V"], "102": ["U"], "103": ["T"], "104": ["S"], "105": ["R"], "106": ["Q"], "107": ["P"], "108": ["O"], "109": ["N"], "110": ["M"], "111": ["L"], "112": ["K"], "113": ["J"], "114": ["I"], "115": ["H"], "116": ["G"], "117": ["F"], "118": ["E"], "119": ["D"], "120": ["C"], "121": ["B"], "122": ["A"], "123": ["-z"], "124": ["-y"], "125": ["-x"], "126": ["-w"], "127": ["-v"], "128": ["-u"], "129": ["-t"], "130": ["-s"], "131": ["-r"], "132": ["-q"], "133": ["-p"], "134": ["-o"], "135": ["-n"], "136": ["-m"], "137": ["-l"], "138": ["-k"], "139": ["-j"], "140": ["-i"], "141": ["-h"], "142": ["-g"], "143": ["-f"], "144": ["-e"], "145": ["-d"], "146": ["-c"], "147": ["-b"], "148": ["-a"], "149": ["-9"], "150": ["-8"], "151": ["-7"], "152": ["-6"], "153": ["-5"], "154": ["-4"], "155": ["-3"], "156": ["-2"], "157": ["-1"], "158": ["-0"], "159": ["-Z"], "160": ["-Y"], "161": ["-X"], "162": ["-W"], "163": ["-V"], "164": ["-U"], "165": ["-T"], "166": ["-S"], "167": ["-R"], "168": ["-Q"], "169": ["-P"], "170": ["-O"], "171": ["-N"], "172": ["-M"], "173": ["-L"], "174": ["-K"], "175": ["-J"], "176": ["-I"], "177": ["-H"], "178": ["-G"], "179": ["-F"], "180": ["-E"], "181": ["-D"], "182": ["-C"], "183": ["-B"], "184": ["-A"], "185": ["=z"], "186": ["=y"], "187": ["=x"], "188": ["=w"], "189": ["=v"], "190": ["=u"], "191": ["=t"], "192": ["=s"], "193": ["=r"], "194": ["=q"], "195": ["=p"], "196": ["=o"], "197": ["=n"], "198": ["=m"], "199": ["=l"], "200": ["=k"], "201": ["=j"], "202": ["=i"], "203": ["=h"], "204": ["=g"], "205": ["=f"], "206": ["=e"], "207": ["=d"], "208": ["=c"], "209": ["=b"], "210": ["=a"], "211": ["=9"], "212": ["=8"], "213": ["=7"], "214": ["=6"], "215": ["=5"], "216": ["=4"], "217": ["=3"], "218": ["=2"], "219": ["=1"], "220": ["=0"], "221": ["=Z"], "222": ["=Y"], "223": ["=X"], "224": ["=W"], "225": ["=V"], "226": ["=U"], "227": ["=T"], "228": ["=S"], "229": ["=R"], "230": ["=Q"], "231": ["=P"], "232": ["=O"], "233": ["=N"], "234": ["=M"], "235": ["=L"], "236": ["=K"], "237": ["=J"], "238": ["=I"], "239": ["=H"], "240": ["=G"], "241": ["=F"], "242": ["=E"], "243": ["=D"], "244": ["=C"], "245": ["=B"], "246": ["=A"], "247": ["?z"], "248": ["?y"], "249": ["?x"], "250": ["?w"], "251": ["?v"], "252": ["?u"], "253": ["?t"], "254": ["?s"], "255": ["?r"], "header": "!!!p1ge0n", "metadata-seperator": ":", "description": "Basic encoding. Provides a single symbol for each byte and the max symbol length is 2. All symbols should be permitted in emails."}
"""

#Classes
class PigeonError(Exception): #Custom exception
    def __init__(self, type, code, message):
        self.Type = type
        self.Code = code #Used as the exit code
        self.Message = message
        super().__init__(self.Message)

    def ExitWithMessage(self):
        print("{0}: {1}".format(self.Type, self.Message))
        exit(self.Code)

class ProgressDisplay(object): #For displaying encoding/decoding progress
    def __init__(self, target):
        self.__target = target
        self.__count = 0

    def Begin(self):
        print("Bytes processed: ", end="")
        return self

    def Update(self, count):
        self.__count += count
        if self.__count >= self.__target:
            print("{0}... ".format(self.__target), end="" if count % 4 == 0 else "\n")
            sys.stdout.flush()
            self.__target = self.__target * 2

    def End(self):
        print("[{0}]".format(self.__count))
        return self

class BufferedInput(object): #Buffered command line input
    def __init__(self):
        self.__buffer = ""
        self.__index = 0
        self.EndOfFile = False
        self.Filename = ""

    def Close(self):
        self.EndOfFile = True

    def __PopulateBuffer(self):
        self.__buffer = input()
        self.__index = 0

    def Read(self):
        if self.__index >= len(self.__buffer):
            try:
                self.__PopulateBuffer()
            except (EOFError, KeyboardInterrupt):
                self.EndOfFile = True
                self.__buffer = ""
        if not self.EndOfFile:
            value = ord(self.__buffer[self.__index])
            self.__index += 1
            return value
        return None

class BufferedFile(object): #Buffered file input and output
    def __init__(self, filename, write, bufferSize):
        self.Filename = filename
        self.__write = write
        self.__file = open(filename, "wb" if self.__write else "rb")
        self.__buffer = bytearray()
        self.__index = 0
        self.__bufferSize = bufferSize
        self.EndOfFile = False

    def Close(self):
        if self.__write:
            self.Flush()
        self.__file.close()
        self.EndOfFile = True

    def __PopulateBuffer(self):
        self.__buffer = self.__file.read(self.__bufferSize)
        self.__index = 0
        self.EndOfFile = len(self.__buffer) == 0

    def Read(self):
        if self.__index >= len(self.__buffer):
            self.__PopulateBuffer()
        if not self.EndOfFile:
            value = self.__buffer[self.__index]
            self.__index += 1
            return value
        return None

    def Flush(self):
        if len(self.__buffer) > 0:
            self.__file.write(self.__buffer)
            self.__buffer = bytearray()
            self.__index = 0

    def Write(self, byte):
        if len(self.__buffer) == self.__bufferSize:
            self.Flush()
        self.__buffer.append(byte)

    def WriteStr(self, string):
        byteArray = bytes([ord(x) for x in string])
        for b in byteArray:
            self.Write(b)

class SymbolNode(object): #Node in the decoding state-machine
    def __init__(self, char):
        self.Char = char
        self.__children = {}
        self.Byte = None

    def Extend(self, code, byte):
        if self.Byte is not None:
            raise PigeonError("CodeBookError", 23, "Bytes {0} and {1} mapped to the same path!".format(self.Byte, byte))
        if len(code) == 0:
            self.Byte = byte
            return
        character = code[0]
        if character not in self.__children:
            self.__children[character] = SymbolNode(character)
        self.__children[character].Extend(code[1:], byte)

    def Decode(self, bufferIn):
        if self.Byte is not None:
            return (self.Byte, 1)
        byte = bufferIn.Read()
        if byte is None:
            raise PigeonError("DecodingError", 43, "Unable to parse file")
        char = chr(byte)
        if char not in self.__children:
            raise PigeonError("DecodingError", 44, "Unable to decode {0} from {1}".format(char, self.Char))
        decodedByte, count = self.__children[char].Decode(bufferIn)
        return (decodedByte, count + 1)

    def __str__(self): #Useful for debugging
        if self.Byte is not None:
            return "{0}->B{1}".format(self.Char, self.Byte)
        return "{0}->({1})".format(self.Char, ",".join([str(self.__children[x]) for x in self.__children.keys()]))

class CodeBook(object): #Codebook for encoding and decoding
    def __init__(self, json):
        self.__json = json
        self.__encoding = {}
        self.__decoding = {}
        self.Header = None
        self.MetadataSeperator = None

    def Build(self):
        codebook = json.loads(self.__json)
        for i in range(0, 256):
            if str(i) not in codebook:
                raise PigeonError("CodeBookError", 21, "Byte {0} not in codebook".format(i))
            codes = codebook[str(i)]
            if len(codes) == 0:
                raise PigeonError("CodeBookError", 22, "No codes specified for byte {0}".format(i))
            self.__encoding[i] = codes # build encoding
            for c in codes: # build decoding
                self.__AddDecoder(c, i)
        self.Header = codebook["header"]
        self.MetadataSeperator = codebook["metadata-seperator"]
        return self

    def __AddDecoder(self, code, byte):
        if len(code) == 0:
            raise PigeonError("CodeBookError", 23, "Byte {0} contains an empty code".format(byte))
        if code[0] in self.__decoding and len(code) == 1:
            raise PigeonError("CodeBookError", 24, "Byte {0} contains a duplicated codeword".format(byte))
        elif code[0] not in self.__decoding:
            self.__decoding[code[0]] = SymbolNode(code[0])
        self.__decoding[code[0]].Extend(code[1:], byte)

    def __EncodeWrite(self, byte, bufferOut, encoded):
        bufferOut.WriteStr(self.__encoding[byte][encoded % len(self.__encoding[byte])])

    def Encode(self, bufferIn, bufferOut, count):
        encoded = 0
        byte = bufferIn.Read()
        while not bufferIn.EndOfFile and encoded < count:
            self.__EncodeWrite(byte, bufferOut, encoded)
            encoded += 1
            byte = bufferIn.Read()
        return encoded

    def Decode(self, bufferIn, bufferOut, count):
        decoded = 0
        while not bufferIn.EndOfFile and decoded < count:
            char = chr(bufferIn.Read())
            if char == self.MetadataSeperator:
                decoded += 1
                bufferIn.EndOfFile = True
                return decoded
            if not char in self.__decoding:
                raise PigeonError("DecodingError", 40, "No decoding for byte \"{0}\"".format(char))
            byte, count = self.__decoding[char].Decode(bufferIn)
            bufferOut.Write(byte)
            decoded += count
        return decoded

    def SeekMetadata(self, bufferIn):
        string = ""
        index = 0
        while True:
            string += chr(bufferIn.Read())
            if self.Header in string:
                break
            if bufferIn.EndOfFile or len(string) >= DEFAULT_BUFFER_SIZE * 10: #Just in case someone inputs the wrong file (and it is massive)
                raise PigeonError("DecodingError", 41, "Unable to locate header \"{0}\"".format(self.Header))
        metadataString = ""
        while True:
            metadataString += chr(bufferIn.Read())
            if metadataString.count(self.MetadataSeperator) == 3:
                break
            if bufferIn.EndOfFile or len(string) >= DEFAULT_BUFFER_SIZE * 10: #Just in case someone inputs the wrong file (and it is massive)
                raise PigeonError("DecodingError", 42, "Unable to locate metadata")
        components = metadataString.split(self.MetadataSeperator)
        return (components[1], components[2])

#Methods
def UniqueFilename(filename, extension): #Gets a filename that is not currently in use
    ext = extension if len(extension) > 0 else ""
    if not os.path.exists("{0}{1}".format(filename, ext)):
        return "{0}{1}".format(filename, ext)
    i = 1
    while os.path.exists("{0}({1}){2}".format(filename, i, ext)):
        i += 1
    return "{0}({1}){2}".format(filename, i, ext)

def GetInputFile(filenameOverride, buffer): #Gets the input file
    if filenameOverride is None:
        return BufferedInput()
    return BufferedFile(filenameOverride, False, buffer)

def GetOutputFile(filenameOverride, buffer): #Gets the output file
    if filenameOverride is None:
        filename = UniqueFilename(DEFAULT_FILENAME, DEFAULT_EXTENSION)
    else:
        name, ext = os.path.splitext(filenameOverride) #Need to ensure filename is unique for decoding
        filename = UniqueFilename(name, ext)
    return BufferedFile(filename, True, buffer)

def Decode(arguments): #Performs the decoding
    codebook = GetCodebook(arguments)
    fileIn = GetInputFile(arguments.filein, arguments.buffer)
    version, filename = codebook.SeekMetadata(fileIn)
    fileOut = GetOutputFile(arguments.fileout or filename, arguments.buffer)
    display = ProgressDisplay(arguments.buffer).Begin()
    try:
        while not fileIn.EndOfFile:
            count = codebook.Decode(fileIn, fileOut, arguments.buffer)
            display.Update(count)
        display.End()
    finally:
        fileIn.Close()
        fileOut.Close()
    print("Complete: Decoded file saved as \"{0}\"".format(fileOut.Filename))

def Encode(arguments): #Performs the encoding
    codebook = GetCodebook(arguments)
    fileIn = GetInputFile(arguments.filein, arguments.buffer)
    fileOut = GetOutputFile(arguments.fileout, arguments.buffer)
    display = ProgressDisplay(arguments.buffer).Begin()
    try:
        fileOut.WriteStr(codebook.Header)
        fileOut.WriteStr("{0}{1}{0}{2}{0}".format(codebook.MetadataSeperator, VERSION, ntpath.basename(fileIn.Filename)))
        while not fileIn.EndOfFile:
            count = codebook.Encode(fileIn, fileOut, arguments.buffer)
            display.Update(count)
        fileOut.WriteStr("{0}{1}".format(codebook.MetadataSeperator, codebook.Header))
        display.End()
    finally:
        fileIn.Close()
        fileOut.Close()
    print("Complete: Encoded data saved in \"{0}\"".format(fileOut.Filename))

def FailWith(message, code): #Displays an error message and exits
    print(message)
    exit(code)

def ValidateArguments(arguments): #Validates the command line arguments
    if arguments.filein is not None and not os.path.exists(arguments.filein):
        raise PigeonError("ArgumentError", 10, "Input file \"{0}\" does not exist!".format(arguments.filein))
    if arguments.fileout is not None and os.path.exists(arguments.fileout):
        raise PigeonError("ArgumentError", 11, "Output file \"{0}\" already exists!".format(arguments.fileout))
    if arguments.codebook is not None and not os.path.exists(arguments.codebook):
        raise PigeonError("ArgumentError", 12, "Codebook file \"{0}\" does not exist!".format(arguments.codebook))
    if arguments.mode.startswith("e") and arguments.filein is None:
        print("Warning: Text input is not reccomended for file input. Command line encoding may not support the file's content.")

def GetCodebook(arguments): #Gets the codebook for encoding/decoding
    if arguments.codebook is None:
        return CodeBook(DEFAULT_CODEBOOK).Build()
    else:
        with open(arguments.codebook) as f:
            return CodeBook(f.read()).Build()

def ParseArguments(): #Parses the command line arguments
    parser = argparse.ArgumentParser(description='Pidgeon arguments.')
    parser.add_argument("mode", type=str, choices=["encode", "e", "decode", "d"], help="Encode/Decode data.")
    parser.add_argument("--filein", type=str, help="Input file. Consumes stdin if not specified.")
    parser.add_argument("--fileout", type=str, help="Overrides the name of the output file.")
    parser.add_argument("--codebook", type=str, help="Supplies a codebook for encoding/decoding.")
    parser.add_argument("--buffer", default=DEFAULT_BUFFER_SIZE, type=lambda x: 1000 if x < 1000 else x, help="Sets the input/output buffer size.")
    return parser.parse_args()

def Main(): #Ye 'ol main
    arguments = ParseArguments()
    try:
        ValidateArguments(arguments)
        if arguments.mode.startswith("e"):
            Encode(arguments)
        elif arguments.mode.startswith("d"):
            Decode(arguments)
    except PigeonError as e:
        e.ExitWithMessage()

if __name__ == "__main__":
    Main()
