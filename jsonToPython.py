import json

# a json string
x = '{"arr": "3", "gcr" : "1", "cdr": "3", "das" : "1", "err": "2", "atr" : "1"}'

# parse json x
jsonObject = json.loads(x)

#print json Object
print(jsonObject)
print(jsonObject["arr"])
