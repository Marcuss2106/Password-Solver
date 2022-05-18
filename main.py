import string
from time import time
from itertools import product
from functools import lru_cache
from sys import stdout
from pwinput import pwinput

CHARACTERS = string.ascii_letters + string.digits + "!" + "_"
user_password = ""
print_attempts = False
start = 0.0


class InvalidPassword(Exception):
    pass


@lru_cache(maxsize=None)
def brute():
    """Iterates through all combinations of the valid characters
    until it matches the user's password
    """
    for i in range(19):
        for combination in product(CHARACTERS, repeat=i):  # -> Tuple
            if print_attempts == True:
                combination = "".join(combination)
                stdout.write(f"  {combination}             \r")
                stdout.flush()
            if combination == tuple(user_password):
                end = time()
                combination = "".join(combination)
                print("Password Found")
                print(f"Is your password: '{combination}'?")
                print(f"{round(end - start,5)}s to find")
                if input("Test again? [y/n]: ").lower() == "y":
                    choose_password()
                break


@lru_cache(maxsize=None)
def search_list():
    """Iterates through every line in Password-List.txt until it 
    matches the user's password
    """
    global start
    start = time()
    # Access password database file
    with open("Password-List.txt") as f:
        print("Searching through password list...")
        # Sort through each line in the file until it matches
        for i, line in enumerate(f):
            if print_attempts:
                stdout.write(f"  {line[:-1]}             \r")
                stdout.flush()
            if user_password == line[:-1]:  # line[:-1] - slice off '\n'
                end = time()
                print("Your password is within the password list!")
                print(f"Is your password: '{line[:-1]}'?")
                print(f"{round(end - start,5)}s to find \n")
                if input("Test again? [y/n]: ").lower() == "y":
                    choose_password()
                break
        else:
            print("Your password was not within the password list!")
            print("Starting brute-force method...")
            brute()


def choose_password():
    """Sets the user password to the hidden input given and checks if
    it has characters not generally allowed in passwords as well as a
    character limit. Any higher character limit can not be cracked within
    a reasonable time frame.
    """
    global user_password, print_attempts
    try:
        user_password = pwinput()  # Hidden password input
        for letter in user_password:
            if letter not in CHARACTERS:
                raise InvalidPassword()
        if len(user_password) > 18:  # Max len to reduce time
            raise InvalidPassword()

        do_print = input(
            "Do you want to print each attempt? (Really Slow) [y/n]: ")
        if do_print.lower() == 'y':
            print_attempts = True

        search_list()

    except InvalidPassword:
        print("""Please choose a password with valid characters and
a length less than 19!
(letters + digits + '!' + '_')""")
        choose_password()


choose_password()
