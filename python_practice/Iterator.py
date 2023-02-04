mytuple = ("apple", "banana", "cherry")
mystr = "abcdefgh"

myit = iter(mytuple)
myit_str = iter(mystr)

print(next(myit))
print(next(myit))
print(next(myit))

for e in myit_str:
    print(next(myit_str))
