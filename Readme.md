# Pigeon
A single-file python command line application for transferring files via plain-text.

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

## Project Structure
  * pigeon.py    The single-file command line application.
  * build.ps1    Builds the codebook files in /encodings.
  * clean.ps1    Deletes temporary build files and test data.
  * tests.ps1    Runs unit tests then tests encoding and decoding of test files.
  * build-and-test.ps1    Runs clean.ps1, then build.ps1 , then tests.ps1.
  * /encodings    Contains codebook generators.
  * /test
    * /data Contains    test data for encoding and decoding tests.
    * /unit-tests    Contains python unit tests.

## Disclaimer
Use Pigeon at your own risk. The author(s) take no responsibility for damage or injury incurred through usage of Pigeon.

# License
Simon Jones, hereby disclaims all copyright interest in the program “Pigeon” written by Simon Jones.  
6 June 2021  
Simon Jones, Lone Programmer  
Distribute under GPL-3.0 see _LICENSE.txt_.
