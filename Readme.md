# Pigeon
A single-file **python** command line application for transferring files via plain-text.

## Basic Usage
Oh no! The university administrators added a rule that disallows email attachments!  
Luckily you can transfer `document.pdf` from your work computer to your personal computer using pigeon.

### 1. Acquire Pigeon
Acquire `pigeon.py` on your work computer and personal computer. (As if anyone would ever use this :joy:)  
Install _python3_ on your work computer and personal computer.

### 2. Encode
`python pigeon.py encode --fin document.pdf --fout document-encoded.txt`  
Copy the contents of `document-encoded.txt` into the email body then send the email.

### 3. Decode
Create `document-encoded.txt` on your personal computer.  
Copy the contents of the email body into `document-encoded.txt`  
`python pigeon.py decode --fin document-encoded.txt`

**Done!** You will now have a copy of `document.pdf` on your personal computer.

## Advanced Usage

### Parameters
Parameter|Type|Optional|Notes
---------|----|---------|-----
mode|String|No|Sets the program operation mode. Either ("encode", "e") or ("decode", "d")
--fin|String|Yes|Input file. Uses stdin if not defined. **Caution**, stdin input is not recommended as command line encoding may mangle files or cause outright failure.
--fout|String|Yes|Output file. Automatically set if not defined.
--buffer|Integer|Yes|Sets the input/output buffer size. Defaults to 10000. Larger numbers may improve performance when processing large files.
--codebook|String|Yes|Selects a codebook file for use in encoding/decoding. See _Codebooks_ below.

### Codebooks
A codebook supplies the encoding information for each byte, along with several control tags.  
The codebook is supplied in json format.  
The following fields must be provided:
  * Encoding for bytes 0-255 `"0": ["x0"]`
  * Header tag `"header": "!!!pigeon"`
  * Metadata separator `"metadata-separator": ":"`

_/encoding_ provides some python files that generates several codebooks. _build.ps1_ generates these files.  
_basic.json_ is embedded in _pigeon.py_ and is used as the default codebook.

## Project Structure
  * _pigeon.py_ →The single-file command line application.
  * _build.ps1_ →Builds the codebook files in /encodings.
  * _clean.ps1_ →Deletes temporary build files and test data.
  * _tests.ps1_ →Runs unit tests then tests encoding and decoding of test files.
  * _build-and-test.ps1_ →Runs clean.ps1, then build.ps1 , then tests.ps1.
  * _/encodings_ →Contains codebook generators.
  * _/test_
    * _/data Contains_ →Test data for encoding and decoding tests.
    * _/unit-tests_ →Contains python unit tests.

## Disclaimer
Use Pigeon at your own risk. The author(s) take no responsibility for damage or injury incurred through usage of Pigeon.

# License
Simon Jones, hereby disclaims all copyright interest in the program “Pigeon” written by Simon Jones.  
6 June 2021  
Simon Jones, Lone Programmer  
Distribute under GPL-3.0 ~ See _LICENSE.txt_.
