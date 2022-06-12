inputStr1 = "abacdec"
inputStr2 = "aaaa"

def findMinSubstring(inpStr):
	counter = 0
	uniqueSubStringCount = 1
	uniqueCountSet = set()
	
	while counter < len(inpStr):
		if inpStr[counter] not in uniqueCountSet:
			uniqueCountSet.add(inpStr[counter])
		else:
			uniqueCountSet = set()
			uniqueCountSet.add(inpStr[counter])
			uniqueSubStringCount += 1

		counter += 1	
	return 	uniqueSubStringCount
	

print(findMinSubstring(inputStr1))			
print(findMinSubstring(inputStr2))		
