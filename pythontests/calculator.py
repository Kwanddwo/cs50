

try:
    x = int(input("x: "))
except:
    print("That is not an int!")
    exit()

try:
    y = int(input("y: "))
except:
    print("that is not an int!")
    exit()

print(x + y)