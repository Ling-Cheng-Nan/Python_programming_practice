'''
Question12 Description:
    Write a program, which will find all such numbers between 1000 and 3000 (both included) such that each digit of the number is an even number.
    The numbers obtained should be printed in a comma-separated sequence on a single line.
    
    Hints:
        In case of input data being supplied to the question, it should be assumed to be a console input.
'''
l=[]
for num in range(1000,3001):
    s = str(num)
    if (int(s[0]) %2 == 0 ):
        if(int(s[1]) %2 == 0 ):
            if(int(s[2]) %2 == 0 ):
                if(int(s[3]) %2 == 0 ):
                    l.append(num)
    else :
        continue;

print(l)

