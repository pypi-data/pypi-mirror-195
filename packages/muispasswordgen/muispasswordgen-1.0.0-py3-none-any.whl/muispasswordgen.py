# Imports the `random` module, this is needed
import random

# Defines the command to generate a password
def gen_psw(len):
  # Makes a list with every possible character used
  car = ['q', 'w', 'e', 'r', 't', 'y', 'u', 'i', 'o', 'p', 'a', 's', 'd', 'f', 'g', 'h', 'j', 'k', 'l', 'z', 'x', 'c', 'v', 'b', 'n', 'm', '1', '2', '3', '4', '5', '6', '7', '8', '9', '0', '_', '-']
  # Makes a empty variable named `password`
  password = ''

  # Loops the addition of a character for the `len` number, defined earlier
  for i in range(1,len):
    password = password + car[random.randint(0, 37)]

  # Returns the `password` value
  return password

  # Example of usage:
  # passwordexample = muispasswordgen.gen_psw(10)
  # Outcome: a random password with length 10!