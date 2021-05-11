# This programs counts consecutive occurences of a word in a string and creates a compressed message digest e.g.
# If input string is aabcdrsss, then output will be a2bcdrs3
# If input string is abc, then output will be abc
# If input string is abbbac, then output will be ab3ac
# If input string is abbbacdssssb, then output will be ab3acds4b

def createCompressedMessageDigestFromAString(message):
    compressedString = ""
    msgList = list(message)
    for i in range(len(msgList)):
        counter = 1
        for j in range(i + 1, len(msgList)):
            if msgList[i] == msgList[j]:
                    counter = counter + 1
            else:
                break
         
        if counter == 1:
            if msgList[i] not in compressedString[-2:]:
                compressedString = compressedString + msgList[i]
        else:
            if msgList[i] not in compressedString:  
                compressedString = compressedString + msgList[i] + str(counter)
        
    print(compressedString)    
    
createCompressedMessageDigestFromAString("aabcdrsss") 
createCompressedMessageDigestFromAString("abc") 
createCompressedMessageDigestFromAString("abbbac") 
createCompressedMessageDigestFromAString("abbbacdssssb") 
