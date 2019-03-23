def onePlus(digits):
    n = len(digits)
    number = 1
    outcome = []
    for i in range(n):
        number = number + digits[i] * 10 ** (n-1-i)
    
    for i in str(number):
        outcome.append(int(i))
        
    return outcome


a = [1,2,3]
# numer 123
# outcome 123 + 1 = 124 in [1,2,4] format
print(onePlus(a))
a = [2,9,9]
# numer 299
# outcome 299 + 1 = 300 in [3,0,0] format
print(onePlus(a))
a = [1,9,9,9]
# number 1999
# outcome 1999 + 1 = 2000 in [2,0,0,0] format
print(onePlus(a))
