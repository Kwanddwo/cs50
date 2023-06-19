

def main():
    while(True):
        try:
            n = int(input("Times : "))
            if n > 0 :
                break
            elif n <= 0 :
                print("Please input a positive integer")
        except ValueError :
            print("Please input a positive integer")
    meow(n)

def meow(n):
    for i in range(n):
        print("meow")

main()