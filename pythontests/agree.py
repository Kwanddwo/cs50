

answer = input("Do you agree? ").upper()

if answer in ["N", "NO", "NON"] :
    print("Not agreed")
elif answer in ["Y", "YES", "OUI"] :
    print("Agreed")
