# Python program for implementation of Bubble Sort
arr = [64, 34, 25, 12, 22, 11, 90]

def bubbleSort(arr):
    n = len(arr)
    for i in range(n):
        for j in range(i+1, n):
            if arr[i] < arr[j]:
                arr[j], arr[i] = arr[i], arr[j]


bubbleSort(arr)
print(arr)
for i in range(len(arr)):
    print("%d" %arr[i])
