import random

def gen_psw(len):
  car = ['q', 'w', 'e', 'r', 't', 'y', 'u', 'i', 'o', 'p', 'a', 's', 'd', 'f', 'g', 'h', 'j', 'k', 'l', 'z', 'x', 'c', 'v', 'b', 'n', 'm', '1', '2', '3', '4', '5', '6', '7', '8', '9', '0', '_', '-']
  password = ''
  if len > 100:
    print('MUIS_ERROR: Password to long')
  else:
    for i in range(1,len):
      password = password + car[random.randint(0, 37)]
    return password