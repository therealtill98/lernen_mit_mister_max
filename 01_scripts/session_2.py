# Conditions
coinflip= True #Heads ist True
if coinflip:
    print("coinresult=head")
else:
    print("coinresult=tail")

coinflip2 = 1  #Heads ist 1
if coinflip2==1:
    print("coinresult=head")
else:
    print("coinresult=tail")

coinflip3 = "Häd"  #Heads ist Head
if coinflip3=="Head":
    print("coinresult=head")
else:
    print("coinresult=tail")

available_credits = 500
required_credits = 501
if available_credits-required_credits>=0:
    print("Allowed")
else:
    print("Denied")

name="Max"
if (name.startswith("M") and len(name)>5) or len(name)>=3:
    print("Name is cool")
else:
    print("Name is not cool")

name="Max"
if (name.startswith("M") and len(name) > 5):
    if len(name) >= 3:
        print("Name is cool")
    else:
        print("Name is not cool")
else:
    print("Name is not cool v2")

# Loops
    # Es gibt For-Loops und While-Loops
    # Ein For-Loop macht eine Task x-häufig

for Auto in range(5):
    print(Auto)

# In Python iteriere ich mit For-Loop über Iterables (e.g. Listen, Dicts)

for Auto in [0,1,2,3,4,"Till"]:
    print(Auto)

# while loops sind "solange" loops

i=5
while i>0:
    print(i)
    i=i-1

i=5
while i>0:
    print(i)
    i=i+1
    if i>1000:
        break

for i in range(100):
    if i%2==0:
        continue
    print(i)

# Modulo Operator; e.g. 10%5=0, 11%5=1; 12%5=2. Wenn es 0 ist, macht er weiter, also werden nur Ungerade Zahlen von 0-99 geprinted

# Primzahlen Sieb
target=1000
primes=[]
start=2
while start<=target:
    is_prime=True
    for known_prime in primes:
        if start%known_prime==0:
            is_prime=False
            break
    if is_prime:
        primes.append(start)
    start=start+1
print(primes)

def sieve_of_eratosthenes(limit):
    primes = [True] * (limit + 1)
    # Für limit=12: primes =[True, True, True, True, True, True, True, True, True, True, True, True, True]
    #                        0     1     2     3     4     5     6     7     8     9     10    11    12
    primes[0] = primes[1] = False
    # Für limit=12: primes =[False, False, True, True, True, True, True, True, True, True, True, True, True]
    #                        0     1     2     3     4     5     6     7     8     9     10    11    12

    #             range (2,4)
    #             [2,3] --> bei range ist links including und rechts excluding
    for number in range(2, int(limit ** 0.5) + 1): #bei for loop muss kein +1 rein, er geht durch Liste
        if primes[number]:
            #für2              range(4, 13, 2) --> fangen bei 4 an, gehen bis 12, gehen in 2er steps. Schmeißen alle vielfachen von 2 raus, daher effizienzer als unser script
            #für2               [4,6,8,10,12]
            for multiple in range(number * number, limit + 1, number):
                primes[multiple] = False
            # Für limit=12: primes =[False, False, True, True, False, True, False, True, False, True, False, True, False]
            #für2                       0      1      2     3      4     5      6      7    8     9       10    11    12

    # Für limit=12: primes =[False, False, True, True, False, True, False, True, False, False, False, True, False]
    # für [2,3]                       0      1      2     3      4     5      6      7    8     9       10    11    12

    for i, is_prime in enumerate(primes):
        if is_prime:
            print(i)

# Run the function
sieve_of_eratosthenes(10000000)


