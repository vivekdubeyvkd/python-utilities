inList1 = [1,1,2,2,2,3,4,4,4]
inList2 = [10,10,10]
inList3 = [1,1,3,4,4,4]

def minOperations(inputList):
	myMap = dict.fromkeys(inputList, 0)
	minMoves = 0
	listLen = len(inputList)
	for i in range(listLen):
		myMap[inputList[i]] += 1		
	print(myMap)

	for key, value in myMap.items():
		x = key 
		freq = value 
		if x <= freq: 
			minMoves += (freq- x)
		else:
			if (x - freq) <= (x / 2):
				minMoves += ( x - freq)	
			else:
				minMoves +=  freq

	return minMoves


print(minOperations(inList1))
print(minOperations(inList2))
print(minOperations(inList3))
