import random

targetnumber=random.randint(1,100)
guess=0

def main():
    while True:
        if (guess != targetnumber):
            guess=int(input("Guess a number from 1 to 100 "))
            if (guess == targetnumber):
                print("You guessed correctly, congratulations!")
                break
            if (guess > targetnumber):
                print("You guessed too high")
            if (guess < targetnumber):
                print("You guessed too low")
