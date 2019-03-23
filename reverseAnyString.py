def reverseAnyString(str):
    listStr = list(str)
    n = len(listStr)
    for i in range(int(n / 2)):
        listStr[i], listStr[n-1-i] = listStr[n-1-i], listStr[i]
    
    return "".join(listStr)
    
    
str = "vivek"
# output keviv
print(reverseAString(str))
str = "hello world"
# output dlrow olleh 
print(reverseAString(str))
