import random
import sys

words = {"Italy", "Maya Climate","Pankow","Maximilian","London","Petersilie","Kohlensäure"}
max_attempts = 3

def exit_game():
    "Beendet Programm sofort"
    print("Spiel beendet")
    sys.exit()
def play_buchstabensalat():
    print("Willkommen zu Buchstabensalat")
    for secret_word in words:
        letters = list(secret_word)
        random.shuffle(letters)
        scrambled = "-".join(letters)
        print (f"Buchstabensalat: {scrambled}")

        attempts = 0
        while attempts < max_attempts:
            guess = input("Was meinste?").strip()
            if guess.lower()== "exit":
                exit_game()
            attempts += 1

            if guess.lower() == secret_word.lower():
                print(f"Schlauer Bursche, in {attempts} erraten")
                break
            else:
                remaining = max_attempts - attempts
                if remaining > 0:
                    print(f"Nö, {max_attempts-attempts} verbleiben")
                else:
                    print(f"Nö, das Word war {secret_word}")

    print("Hau rein")

play_buchstabensalat()