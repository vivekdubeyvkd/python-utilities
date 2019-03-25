def tripletsToFormTriangle(arr):
    tripletsToFormTriangle = 0
    n = len(arr)
    for first in range(0, n - 1):
        second =  first + 1
        while second < n - 1:
            for third in range(second + 1, n):
                if (arr[first] + arr[second]) > arr[third] :
                    print(arr[first] , arr[second], arr[third])
                    tripletsToFormTriangle += 1
                    
            second += 1  
    
    
    return tripletsToFormTriangle
    
    
arr = [10, 21, 22, 100, 101, 200, 300] # output 6
arr.sort()
print("++++++++++++++++++++++++")
print("number of traingles : ", tripletsToFormTriangle(arr))
print("++++++++++++++++++++++++")
arr = [7, 3, 6, 4] # output 3
arr.sort()
print("++++++++++++++++++++++++")
print("number of traingles : ", tripletsToFormTriangle(arr))
print("++++++++++++++++++++++++")
arr = [2, 3, 4, 5, 6, 7] # output 13
arr.sort()
print("++++++++++++++++++++++++")
print("number of traingles : ", tripletsToFormTriangle(arr))
print("++++++++++++++++++++++++")
arr = [4, 22, 7, 5, 10] # output 3
arr.sort()
print("++++++++++++++++++++++++")
print("number of traingles : ", tripletsToFormTriangle(arr))
print("++++++++++++++++++++++++")
