#Imports
import argparse
import os
import json
import ntpath

#Global vairables
VERSION = "1.0.0"
DEFAULT_BUFFER_SIZE = 10000
DEFAULT_FILENAME = "message"
DEFAULT_EXTENSION = ".pgy"
DEFAULT_CODEBOOK="""
{"0": ["000"], "1": ["001"], "2": ["002"], "3": ["003"], "4": ["004"], "5": ["005"], "6": ["006"], "7": ["007"], "8": ["008"], "9": ["009"], "10": ["010"], "11": ["011"], "12": ["012"], "13": ["013"], "14": ["014"], "15": ["015"], "16": ["016"], "17": ["017"], "18": ["018"], "19": ["019"], "20": ["020"], "21": ["021"], "22": ["022"], "23": ["023"], "24": ["024"], "25": ["025"], "26": ["026"], "27": ["027"], "28": ["028"], "29": ["029"], "30": ["030"], "31": ["031"], "32": ["032"], "33": ["033"], "34": ["034"], "35": ["035"], "36": ["036"], "37": ["037"], "38": ["038"], "39": ["039"], "40": ["040"], "41": ["041"], "42": ["042"], "43": ["043"], "44": ["044"], "45": ["045"], "46": ["046"], "47": ["047"], "48": ["048"], "49": ["049"], "50": ["050"], "51": ["051"], "52": ["052"], "53": ["053"], "54": ["054"], "55": ["055"], "56": ["056"], "57": ["057"], "58": ["058"], "59": ["059"], "60": ["060"], "61": ["061"], "62": ["062"], "63": ["063"], "64": ["064"], "65": ["065"], "66": ["066"], "67": ["067"], "68": ["068"], "69": ["069"], "70": ["070"], "71": ["071"], "72": ["072"], "73": ["073"], "74": ["074"], "75": ["075"], "76": ["076"], "77": ["077"], "78": ["078"], "79": ["079"], "80": ["080"], "81": ["081"], "82": ["082"], "83": ["083"], "84": ["084"], "85": ["085"], "86": ["086"], "87": ["087"], "88": ["088"], "89": ["089"], "90": ["090"], "91": ["091"], "92": ["092"], "93": ["093"], "94": ["094"], "95": ["095"], "96": ["096"], "97": ["097"], "98": ["098"], "99": ["099"], "100": ["100"], "101": ["101"], "102": ["102"], "103": ["103"], "104": ["104"], "105": ["105"], "106": ["106"], "107": ["107"], "108": ["108"], "109": ["109"], "110": ["110"], "111": ["111"], "112": ["112"], "113": ["113"], "114": ["114"], "115": ["115"], "116": ["116"], "117": ["117"], "118": ["118"], "119": ["119"], "120": ["120"], "121": ["121"], "122": ["122"], "123": ["123"], "124": ["124"], "125": ["125"], "126": ["126"], "127": ["127"], "128": ["128"], "129": ["129"], "130": ["130"], "131": ["131"], "132": ["132"], "133": ["133"], "134": ["134"], "135": ["135"], "136": ["136"], "137": ["137"], "138": ["138"], "139": ["139"], "140": ["140"], "141": ["141"], "142": ["142"], "143": ["143"], "144": ["144"], "145": ["145"], "146": ["146"], "147": ["147"], "148": ["148"], "149": ["149"], "150": ["150"], "151": ["151"], "152": ["152"], "153": ["153"], "154": ["154"], "155": ["155"], "156": ["156"], "157": ["157"], "158": ["158"], "159": ["159"], "160": ["160"], "161": ["161"], "162": ["162"], "163": ["163"], "164": ["164"], "165": ["165"], "166": ["166"], "167": ["167"], "168": ["168"], "169": ["169"], "170": ["170"], "171": ["171"], "172": ["172"], "173": ["173"], "174": ["174"], "175": ["175"], "176": ["176"], "177": ["177"], "178": ["178"], "179": ["179"], "180": ["180"], "181": ["181"], "182": ["182"], "183": ["183"], "184": ["184"], "185": ["185"], "186": ["186"], "187": ["187"], "188": ["188"], "189": ["189"], "190": ["190"], "191": ["191"], "192": ["192"], "193": ["193"], "194": ["194"], "195": ["195"], "196": ["196"], "197": ["197"], "198": ["198"], "199": ["199"], "200": ["200"], "201": ["201"], "202": ["202"], "203": ["203"], "204": ["204"], "205": ["205"], "206": ["206"], "207": ["207"], "208": ["208"], "209": ["209"], "210": ["210"], "211": ["211"], "212": ["212"], "213": ["213"], "214": ["214"], "215": ["215"], "216": ["216"], "217": ["217"], "218": ["218"], "219": ["219"], "220": ["220"], "221": ["221"], "222": ["222"], "223": ["223"], "224": ["224"], "225": ["225"], "226": ["226"], "227": ["227"], "228": ["228"], "229": ["229"], "230": ["230"], "231": ["231"], "232": ["232"], "233": ["233"], "234": ["234"], "235": ["235"], "236": ["236"], "237": ["237"], "238": ["238"], "239": ["239"], "240": ["240"], "241": ["241"], "242": ["242"], "243": ["243"], "244": ["244"], "245": ["245"], "246": ["246"], "247": ["247"], "248": ["248"], "249": ["249"], "250": ["250"], "251": ["251"], "252": ["252"], "253": ["253"], "254": ["254"], "255": ["255"], "header": "!p1ge0n", "metadata-seperator": ":", "tail": "!p1ge0n"}
"""

#Classes
class BufferedInput(object): #Buffered command line input
    def __init__(self):
        self.__buffer = ""
        self.__index = 0
        self.EndOfFile = False
        self.Filename = ""

    def IsEmpty(self):
        return len(self.__buffer) == 0

    def Close(self):
        pass

    def Read(self):
        if self.__index >= len(self.__buffer) - 1:
            try:
                self.__buffer = input()
                self.__index = 0
            except (EOFError, KeyboardInterrupt):
                self.EndOfFile = True
                self.__buffer = ""
        if len(self.__buffer) > 0:
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

    def IsEmpty(self):
        return len(self.__buffer) == 0

    def Close(self):
        if self.__write:
            self.Flush()
        self.__file.close()

    def Read(self):
        if self.__index >= len(self.__buffer) - 1:
            self.__buffer = self.__file.read(self.__bufferSize)
            self.__index = 0
            self.EndOfFile = len(self.__buffer) == 0
        if len(self.__buffer) > 0:
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
            FailWith("CodeBookError: Bytes {0} and {1} mapped to the same path!".format(self.Byte, byte), 23)
        if len(code) == 0:
            self.Byte = byte
            return
        character = code[0]
        if character not in self.__children:
            self.__children[character] = SymbolNode(character)
        self.__children[character].Extend(code[1:], byte)

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
        self.Tail = None
        self.MetadataSeperator = None

    def Build(self):
        codebook = json.loads(self.__json)
        for i in range(0, 256):
            codes = codebook[str(i)]
            if len(codes) == 0:
                FailWith("CodeBookError: No codes specified for byte {0}".format(i), 20)
            self.__encoding[i] = codes # build encoding
            for c in codes: # build decoding
                self.__AddDecoder(c, i)
        self.Header = codebook["header"]
        self.Tail = codebook["tail"]
        self.MetadataSeperator = codebook["metadata-seperator"]
        return self

    def __AddDecoder(self, code, byte):
        if len(code) == 0:
            FailWith("CodeBookError: Byte {0} contains an empty code".format(byte), 21)
        if code[0] in self.__decoding and len(code) == 1:
            FailWith("CodeBookError: Byte {0} contains a duplicated codeword".format(byte), 22)
        elif code[0] not in self.__decoding:
            self.__decoding[code[0]] = SymbolNode(code[0])
        self.__decoding[code[0]].Extend(code[1:], byte)

    def Encode(self, bufferIn, bufferOut, count):
        encoded = 0
        byte = bufferIn.Read()
        while not bufferIn.IsEmpty() and encoded < count:
            if not byte in self.__encoding:
                FailWith("EncodingError: No encoding for byte \"{0}\"".format(byte), 30)
            bufferOut.WriteStr(self.__encoding[byte][encoded % len(self.__encoding[byte])])
            encoded += 1
            byte = bufferIn.Read()
        return encoded

    def Decode(self, bufferIn, bufferOut, count):
        decoded = 0
        while not bufferIn.IsEmpty() and decoded < count:
            byte =  bufferIn.Read()
            if not byte in self.__decoding:
                FailWith("DecodingError: No decoding for byte \"{0}\"".format(byte), 40)
            bufferOut.Write(self.__decoding.Decode(byte))
            decoded += 1
        return decoded

#Methods
def UniqueFilename(filename, extension): #Gets a filename that is not currently in use
    ext = extension if len(extension) > 0 else ""
    if not os.path.exists("{0}{1}".format(filename, ext)):
        return "{0}{1}".format(filename, ext)
    i = 1
    while os.path.exists("{0}({1}){2}".format(filename, i, ext)):
        i += 1
    return "{0}({1}){2}".format(filename, i, ext)

def GetInputFile(arguments): #Gets the input file
    if arguments.filein is None:
        return BufferedInput()
    return BufferedFile(arguments.filein, False, DEFAULT_BUFFER_SIZE)

def GetOutputFile(arguments): #Gets the output file
    if arguments.fileout is None:
        filename = UniqueFilename(DEFAULT_FILENAME, DEFAULT_EXTENSION)
    else:
        name, ext = os.path.splitext(arguments.fileout)
        filename = UniqueFilename(name, ext)
    return BufferedFile(filename, True, DEFAULT_BUFFER_SIZE)

def Decode(arguments): #Performs the decoding
    FailWith("Not implemented", 1)
    print("Complete: Encoded data saved in {0}".format(fileOut.Filename))

def Encode(arguments): #Performs the encoding
    codebook = GetCodebook(arguments)
    fileIn = GetInputFile(arguments)
    fileOut = GetOutputFile(arguments)
    try:
        fileOut.WriteStr(codebook.Header)
        fileOut.WriteStr("{0}{1}{0}{2}{0}".format(codebook.MetadataSeperator, VERSION, ntpath.basename(fileIn.Filename)))
        while not fileIn.EndOfFile:
            codebook.Encode(fileIn, fileOut, DEFAULT_BUFFER_SIZE)
        fileOut.WriteStr(codebook.Tail)
    finally:
        fileIn.Close()
        fileOut.Close()
    print("Complete: Encoded data saved in {0}".format(fileOut.Filename))

def FailWith(message, code): #Displays an error message and exits
    print(message)
    exit(code)

def ValidateArguments(arguments): #Validates the command line arguments
    if arguments.filein is not None and not os.path.exists(arguments.filein):
        FailWith("ArgumentError: Input file \"{0}\" does not exist!".format(arguments.filein), 10)
    if arguments.fileout is not None and os.path.exists(arguments.fileout):
        FailWith("ArgumentError: Output file \"{0}\" already exists!".format(arguments.fileout), 11)
    if arguments.codebook is not None and not os.path.exists(arguments.codebook):
        FailWith("ArgumentError: Codebook file \"{0}\" does not exist!".format(arguments.codebook), 12)
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
    return parser.parse_args()

def Main(): #Ye 'ol main
    arguments = ParseArguments()
    ValidateArguments(arguments)
    if arguments.mode.startswith("e"):
        Encode(arguments)
    elif arguments.mode.startswith("d"):
        Decode(arguments)

if __name__ == "__main__":
    Main()
