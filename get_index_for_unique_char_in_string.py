outputDict = {}

def getUniqueCharacter(s):
    # Write your code here
    for i in range(len(s)):
        charVal = s[i]
        if charVal not in outputDict.keys():
            outputDict[charVal] = i + 1
        else:
            outputDict[charVal] = -1


    for key in outputDict.keys():
        if outputDict[key] != -1:
            return outputDict[key]
    
    return -1        

 
getUniqueCharacter("madam")
getUniqueCharacter("falafal")
getUniqueCharacter("hackthegame")
