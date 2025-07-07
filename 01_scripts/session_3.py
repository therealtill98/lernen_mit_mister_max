repeats=5
def print_greeting(name:str,name2:str,n:int):
    for i in range(n):
        print(f"{name} vs. {name2}")


print_greeting("9","Alcaraz",repeats)
print_greeting("Zverev","Djoker",9)
print_greeting(name="Zverev",name2="Djoker",n=9)
print_greeting(name2="Djoker",n=9,name="Zverev")