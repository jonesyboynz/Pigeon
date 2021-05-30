import json

plainTextSymbols = [chr(i) for i in range(122, 96, -1)] \
    + [chr(i) for i in range(57, 47, -1)] \
    + [chr(i) for i in range(90, 64, -1)]

encoding = {}
for i in range(0, 48): #G1
    encoding[i] = ["+"+plainTextSymbols[i-0]]

for i in range(48, 58): #0-9
    encoding[i] = [plainTextSymbols[i-48]]

for i in range(58, 65): #G2
    encoding[i] = ["+"+plainTextSymbols[i-58+48]]

for i in range(65, 91): #A-Z
    encoding[i] = [plainTextSymbols[i-65+10]]

for i in range(91, 97): #G3
    encoding[i] = ["+"+plainTextSymbols[i-91+48+7]]

for i in range(97, 123): #a-z
    encoding[i] = [plainTextSymbols[i-97+10+26]]

for i in range(123, 185): #G4
    encoding[i] = ["-"+plainTextSymbols[i-123]]

for i in range(185, 247): #G5
    encoding[i] = ["="+plainTextSymbols[i-185]]

for i in range(247, 256): #G6
    encoding[i] = ["?"+plainTextSymbols[i-247]]

#metadata
encoding["header"] = "!!!p1ge0n"
encoding["metadata-seperator"] = ":"
encoding["description"] = "Basic encoding. Provides a single symbol for each byte and the max symbol length is 2. All symbols should be permitted in emails."

with open("basic.json", "w") as f:
    f.write(json.dumps(encoding))
