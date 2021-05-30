import json

encoding = {}
for i in range(0, 256): #G1
    encoding[i] = ["{0:0>3}".format(i)]

#metadata
encoding["header"] = "!!!414307"
encoding["metadata-seperator"] = ":"
encoding["description"] = "Numeric. All bytes are encoded as 3-digit numbers."

with open("numeric.json", "w") as f:
    f.write(json.dumps(encoding))
