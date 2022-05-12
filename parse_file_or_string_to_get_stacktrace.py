import json

str_one = """main, workloop
main, workloop, select
main, workloop, parseargs, parse_item
main, select, parse_args
main2, wk2, select2"""

outputDict = {}
str_one_lines_list = str_one.split('\n')

def checkAndAddElement(elementName, values):
  subValues = []
  valuesLen = len(values)
  if valuesLen == 1:
    subValues.append({"name": elementName + "." + values[0].strip(), "count" : 1})    
  else:
    for x in range(len(values)):
      value = values[x]
      if x == 0:
        subValues.append({"name": elementName + "." + value.strip(), "count" : 1})
      else:
        newElementName = subValues[-1]["name"]
        subValues.append({"name": newElementName + "." + value.strip(), "count" : 1})    

  outputDict[elementName] = {
  "count" : 1, 
  "stacktrace" : subValues
 } 

for i in str_one_lines_list:
    if ',' in i:
        values = i.split(',') # ['main', 'workshop']
        topLevelElement = values[0].strip()
        subroutine = values[1:]
        if topLevelElement in outputDict.keys():
          topLevelValue = outputDict[topLevelElement]
          topLevelValue["count"] += 1
          nextValues = topLevelValue["stacktrace"]
          newElementName = topLevelElement
          for n in range(len(subroutine)):
            j = subroutine[n]
            newElementName = newElementName + "." + j.strip()
            valueFlag = 0
            for k in nextValues:
              if newElementName == k["name"]:
                k["count"] += 1
                valueFlag = 1

            if valueFlag == 0:  
                nextValues.append({"name": newElementName, "count" : 1})
        else:
          checkAndAddElement(topLevelElement, subroutine)


print(json.dumps(outputDict, indent = 3)) 
