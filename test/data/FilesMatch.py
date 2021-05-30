import argparse
import os

def FilesMatch(file1, file2):
    with open(file1, "rb") as f1:
        f1Data = f1.read()
    with open(file2, "rb") as f2:
        f2Data = f2.read()
    if len(f1Data) !=len(f2Data):
        print("FileDoNotMatch: {0} [{1} bytes] and {2} [{3} bytes] are diferent lengths.".format(file1, len(f1Data), file2, len(f2Data)))
        return False
    for i in range(0, len(f1Data)):
        if f1Data[i] != f2Data[i]:
            print("FileDoNotMatch: {0} and {1} do not match at byte {3} [{4}!={5}].".format(file1, file2, i, f1Data[i], f2Data[i]))
            return False
    return True

def FilesExist(self, *files):
    for f in files:
        if not os.path.exists(f):
            print("FileDoNotMatch: {0} does not exist.".format(f))
            return False
    return True

def ParseArguments():
    parser = argparse.ArgumentParser(description='Checks if files match')
    parser.add_argument("file1", type=str, help="The first file")
    parser.add_argument("file2", type=str, help="The second file")
    return parser.parse_args()

def main():
    arguments = ParseArguments()
    if not FilesExist(arguments.file1, arguments.file2):
        exit(1)
    if not FilesMatch(arguments.file1, arguments.file2):
        exit(1)
    exit(0)

if __name__ == "__main__":
    main()
