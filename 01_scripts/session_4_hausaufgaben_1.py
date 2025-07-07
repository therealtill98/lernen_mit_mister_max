# Hardmode

# Aufgabe: Schreibe eine Software, die den Nutzer eine Zahl raten lässt. Gleichzeitig denkt sich der Computer eine Zahl aus. Der Computer fragt den Nutzer dann nach einer Zahl und validiert den Input.
# Nach jedem raten wird eine neue random Zahl generiert.
import random
import sys



# generate random number and replay loop
mode = input("Do you want to play normal or hard?").strip().lower()
valid = "normal", "hard"
while mode not in valid:
    mode = input("Please type either 'normal' or 'hard'.")
    if mode == "finish":
        gave_up = True
        print("You gave up before choosing a mode. Goodbye")
        sys.exit()
while True:
    attempts = 0
    secret = random.randint(a=1, b=10)

    # ask user for input, validate it and 5 attempt limit
    gave_up = False
    while attempts < 5:
        raw = input("Guess a number between 1 and 10, you have max. 5 attempts or type 'finish' to quit): ")
        print("Please note you have max. 5 attempts")
        if raw == "finish":
            gave_up = True
            print(f"You gave up after {attempts} attempts. Goodbye")
            sys.exit()
        try:
            guess = int(raw)
            if not 1 <= guess <= 10:
                raise ValueError

    # non-int or out of range
        except ValueError:
            print("Sorry, that's not a number between 1-10. Try again.")
            continue

    # compare input to random number
        attempts += 1
        if guess == secret:
            print(f"Congratulations, you guessed it in {attempts} attempts!")
            break
        elif attempts < 5:
            if mode == "normal":
                print("Sorry, that's the wrong number. Try again.")
                print(f"Attempts remaining: {5- attempts}\n")
            if mode == "hard":
                print(f"Sorry, that's the wrong number. The number was {secret}\n")
                print(f"Attempts remaining: {5 - attempts}\n")
                secret = random.randint(a=1, b=10)
        else:
            print(f"You're out of attempts. The number was {secret}\n")

    # play again loop
    again = input("Would you like to play again? (yes/no): ").strip().lower()
    if again == "yes":
        continue
    else:
        print("Okay, see you next time!")
        break