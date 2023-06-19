import re

while True:
    numberstring = input("Number: ")
    try:
        number = int(numberstring)
    except ValueError:
        number = 0

    if number > 0:
        break

sum = 0
k = 10


for i in range(8):
    j = k * 10
    c = k / 10
    var1 = 2 * (number // k - (number // j) * 10)
    var2 = number // c - (number // k) * 10

    sum += var1 + var2

    if var1 > 9:
        sum += - 9

    k = k * 100


correct = (sum % 10 == 0)

length = len(numberstring)

if length == 16:
    mastercard = re.search("^5[1-5]", numberstring)
    visa = re.search("^4", numberstring)

    if mastercard and correct:
        print("MASTERCARD")
    elif visa and correct:
        print("VISA")
    else:
        print("INVALID")

elif length == 15:
    amex = re.search("^3[47]", numberstring)

    if amex and correct:
        print("AMEX")
    else:
        print("INVALID")

elif length == 13:
    visa = re.search("^4", numberstring)

    if visa and correct:
        print("VISA")
    else:
        print("INVALID")

else:
    print("INVALID")

