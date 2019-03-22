x = {'a':3, 'g' : 1, 'c': 3, 't' : 1, 'e': 2, 'd' : 1}

# one way to sort is
tmp = list(x.keys())
tmp.sort()
# print sorted values
print(" sorted value : ", tmp)
# print in reverse order
print(" sorted reverse values ", tmp[::-1])

# print max key
print("max key : ", max(x.keys()))
# print max value
print("max value : ", max(x.values()))


# another way to sort is
tmp = sorted(x.keys())
print("sorted way 2 :", tmp)
# sort in reverse order
tmp = sorted(x.keys(), reverse=True)
print("sorted way to in reverse order :", tmp)
