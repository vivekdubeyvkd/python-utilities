# you can add elements till Z and assign respective numbers against them in initialMap Dict, for now it has been initialized till d
initialMap = {
    'a' : 1,
    'b' : 2,
    'c' : 3,
    'd' : 4
}

def getValue(strIn, position, inputLength):
    return (initialMap[strIn] * 26 ** (inputLength - position))
  
def mapStringToNumber(inputStr):
    inputLength = len(inputStr)
    finalNumber = 0
    if inputLength == 0:
        return   
    elif inputLength == 1:
        return initialMap[inputStr]
    else:
        values = list(inputStr)
        for i in range(len(values)):
            value = values[i]
            finalNumber = finalNumber + getValue(value, i + 1, inputLength)
        
        #return (values[0] * 26 ** 1) + (values[1] * 26 ** 0) when it has two chars like aa or ab
        return finalNumber
        
        
# You can call mapStringToNumber function as shown below
print(mapStringToNumber('a'))
print(mapStringToNumber('aa'))
print(mapStringToNumber('ab'))
print(mapStringToNumber('abc'))
