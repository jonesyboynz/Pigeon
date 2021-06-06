# Pigeon
A single-file python command line application for transferring files via plain-text.

## Basic Usage
Oh no! The university administrators added a rule that disallows email attachments!
Given you have a file _document.pdf_ that you need to transfer from your work computer to your personal computer.

### 1. Acquire Pigeon
Acquire _pigeon.py_ on your work computer and personal computer.

### 2. Encode
`python pigeon.py encode --fin document.pdf --fout document-encoded.txt`
Copy the contents of _document-encoded.txt_ into the email body then send the email.

### 3. Decode
Create _document-encoded.txt_ on your personal computer.
Copy the contents of the email body into _document-encoded.txt_
`python pigeon.py decode --fin document-encoded.txt`

**Done!** You will now have a copy of _document.pdf_ on your personal computer.

## Project Structure
  * pigeon.py
    The single-line command line application.
  * build.ps1
    Builds the codebook files in /encodings.
  * clean.ps1
    Deletes temporary build files and test data.
  * tests.ps1
    Runs unit tests then tests encoding and decoding of test files.
  * build-and-test.ps1
    Runs clean.ps1, then build.ps1 , then tests.ps1.
  * /encodings
    Contains codebook generators.
  * /test
    * /data
      Contains test data for encoding and decoding tests.
    * /unit-tests
      Contains python unit tests.
