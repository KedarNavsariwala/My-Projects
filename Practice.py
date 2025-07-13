def age_define():
    
    age = int(input("Enter your Age: "))

    if age >= 18:
        print("You are an adult.")
    else:
        print("You are a minor.")

def simpleloop():

    i = int(input("Enter a number: "))

    for i in range(5):
        print(i)


def stringcounter(S, s):
    
    return S.count(s)
